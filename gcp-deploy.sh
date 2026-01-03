#!/bin/bash

# GCP 배포 스크립트
# 사용법: ./gcp-deploy.sh [프로젝트ID] [환경]

set -e

PROJECT_ID=${1:-your-gcp-project-id}
ENVIRONMENT=${2:-production}
REGION=${3:-asia-northeast3}

# 색상 출력
print_info() {
    echo -e "\033[34m[INFO] $1\033[0m"
}

print_success() {
    echo -e "\033[32m[SUCCESS] $1\033[0m"
}

print_warning() {
    echo -e "\033[33m[WARNING] $1\033[0m"
}

print_error() {
    echo -e "\033[31m[ERROR] $1\033[0m"
}

# GCP 인증
authenticate_gcp() {
    print_info "GCP 인증 중..."
    
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
        print_warning "GCP 로그인이 필요합니다."
        gcloud auth login
    fi
    
    gcloud config set project $PROJECT_ID
    gcloud config set compute/region $REGION
    
    print_success "GCP 인증 완료"
}

# 리소스 생성
create_resources() {
    print_info "GCP 리소스 생성 중..."
    
    # VPC 네트워크
    gcloud compute networks create business-network --subnet-mode=custom
    
    # 서브넷
    gcloud compute networks subnets create business-subnet \
        --network=business-network \
        --range=10.0.0.0/24 \
        --region=$REGION
    
    # 방화벽 규칙
    gcloud compute firewall-rules create allow-http \
        --allow=tcp:80 \
        --network=business-network \
        --source-ranges=0.0.0.0/0 \
        --target-tags=http-server
    
    gcloud compute firewall-rules create allow-https \
        --allow=tcp:443 \
        --network=business-network \
        --source-ranges=0.0.0.0/0 \
        --target-tags=https-server
    
    gcloud compute firewall-rules create allow-ssh \
        --allow=tcp:22 \
        --network=business-network \
        --source-ranges=0.0.0.0/0
    
    print_success "네트워크 리소스 생성 완료"
}

# Cloud SQL 생성
create_database() {
    print_info "Cloud SQL 데이터베이스 생성 중..."
    
    # Cloud SQL 인스턴스
    gcloud sql instances create business-db \
        --database-version=POSTGRES_15 \
        --tier=db-f1-micro \
        --region=$REGION \
        --network=business-network \
        --no-assign-ip
    
    # 데이터베이스 생성
    gcloud sql databases create business_management --instance=business-db
    
    # 사용자 생성
    DB_PASSWORD=$(openssl rand -base64 32)
    gcloud sql users create postgres --instance=business-db --password=$DB_PASSWORD
    
    print_success "Cloud SQL 생성 완료"
    echo "데이터베이스 비밀번호: $DB_PASSWORD"
}

# GKE 클러스터 생성
create_cluster() {
    print_info "GKE 클러스터 생성 중..."
    
    gcloud container clusters create business-cluster \
        --num-nodes=2 \
        --machine-type=e2-medium \
        --region=$REGION \
        --network=business-network \
        --subnetwork=business-subnet \
        --enable-autoscaling \
        --min-nodes=1 \
        --max-nodes=5 \
        --enable-autorepair \
        --enable-autoupgrade
    
    # 인증 정보 가져오기
    gcloud container clusters get-credentials business-cluster --region=$REGION
    
    print_success "GKE 클러스터 생성 완료"
}

# Docker 이미지 빌드 및 푸시
build_and_push_image() {
    print_info "Docker 이미지 빌드 및 푸시 중..."
    
    # Artifact Registry 레포지토리 생성
    gcloud artifacts repositories create business-repo \
        --repository-format=docker \
        --location=$REGION \
        --description="Business management Docker images"
    
    # Docker 인증
    gcloud auth configure-docker $REGION-docker.pkg.dev
    
    # 이미지 빌드
    IMAGE_TAG="$REGION-docker.pkg.dev/$PROJECT_ID/business-repo/business-management:latest"
    docker build -t $IMAGE_TAG .
    
    # 이미지 푸시
    docker push $IMAGE_TAG
    
    print_success "Docker 이미지 푸시 완료: $IMAGE_TAG"
}

# Kubernetes 매니페스트 적용
deploy_kubernetes() {
    print_info "Kubernetes 배포 중..."
    
    # ConfigMap 생성
    kubectl create configmap app-config \
        --from-literal=DEBUG=False \
        --from-literal=DB_HOST=$(gcloud sql instances describe business-db --format='value(ipAddresses[0].ipAddress)') \
        --from-literal=DB_NAME=business_management \
        --from-literal=DB_USER=postgres \
        --dry-run=client -o yaml | kubectl apply -f -
    
    # Secret 생성
    kubectl create secret generic app-secrets \
        --from-literal=SECRET_KEY=$(openssl rand -hex 32) \
        --from-literal=DB_PASSWORD=$DB_PASSWORD \
        --dry-run=client -o yaml | kubectl apply -f -
    
    # 배포
    envsubst < k8s/deployment.yaml | kubectl apply -f -
    
    # 서비스
    kubectl apply -f k8s/service.yaml
    
    # Ingress
    kubectl apply -f k8s/ingress.yaml
    
    print_success "Kubernetes 배포 완료"
}

# 모니터링 설정
setup_monitoring() {
    print_info "모니터링 설정 중..."
    
    # Cloud Monitoring 에이전트 설치
    kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/k8s-stackdriver/master/custom-metrics-stackdriver-adapter/deploy/stable/stackdriver-adapter.yaml
    
    print_success "모니터링 설정 완료"
}

# 헬스 체크
health_check() {
    print_info "헬스 체크 중..."
    
    # 외부 IP 가져오기
    EXTERNAL_IP=$(kubectl get service business-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    
    if [ -n "$EXTERNAL_IP" ]; then
        print_success "외부 IP: $EXTERNAL_IP"
        
        # 헬스 체크
        for i in {1..30}; do
            if curl -f -s "http://$EXTERNAL_IP/health/" > /dev/null; then
                print_success "애플리케이션 정상 실행 중"
                break
            fi
            echo "헬스 체크 대기... ($i/30)"
            sleep 10
        done
    else
        print_error "외부 IP를 가져올 수 없습니다"
        exit 1
    fi
}

# 메인 함수
main() {
    print_info "GCP 배포 시작: $PROJECT_ID ($ENVIRONMENT)"
    
    authenticate_gcp
    create_resources
    create_database
    create_cluster
    build_and_push_image
    deploy_kubernetes
    setup_monitoring
    health_check
    
    print_success "GCP 배포 완료! 🎉"
    print_info "애플리케이션 URL: http://$EXTERNAL_IP"
}

# 스크립트 실행
main "$@"
