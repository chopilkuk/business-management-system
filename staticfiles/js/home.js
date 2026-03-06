document.addEventListener('DOMContentLoaded', function() {
    // 출근 버튼 기능
    const goBtn = document.querySelector('.goBtn');
    if (goBtn) {
        goBtn.addEventListener('click', function() {
            const currentTime = new Date().toLocaleTimeString('ko-KR', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
            this.value = currentTime;
            
            // 서버에 출근 시간 전송
            fetch('/commute/check-in/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    time: currentTime,
                    type: 'check_in'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('출근이 완료되었습니다.', 'success');
                } else {
                    showNotification('오류가 발생했습니다.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('서버 연결 오류', 'error');
            });
        });
    }

    // 퇴근 버튼 기능
    const outBtn = document.querySelector('.outBtn');
    if (outBtn) {
        outBtn.addEventListener('click', function() {
            const currentTime = new Date().toLocaleTimeString('ko-KR', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
            this.value = currentTime;
            
            // 서버에 퇴근 시간 전송
            fetch('/commute/check-out/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    time: currentTime,
                    type: 'check_out'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('퇴근이 완료되었습니다.', 'success');
                } else {
                    showNotification('오류가 발생했습니다.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('서버 연결 오류', 'error');
            });
        });
    }

    // 로그아웃 버튼 기능
    const logoutBtn = document.querySelector('.logout');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            if (confirm('로그아웃 하시겠습니까?')) {
                window.location.href = '/login/';
            }
        });
    }

    // 알림 기능
    const allBtn = document.querySelector('.allBtn');
    const metionBtn = document.querySelector('.metionBtn');
    
    if (allBtn) {
        allBtn.addEventListener('click', function() {
            loadNotifications('all');
        });
    }
    
    if (metionBtn) {
        metionBtn.addEventListener('click', function() {
            loadNotifications('mention');
        });
    }

    // 알림 박스 토글
    const alarmBox = document.querySelector('.alarmBox');
    const alarmImg = document.querySelector('.alarmImg');
    
    if (alarmImg && alarmBox) {
        alarmImg.addEventListener('click', function() {
            alarmBox.style.display = alarmBox.style.display === 'none' ? 'block' : 'none';
        });
    }
});

// CSRF 토큰 가져오기
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 알림 표시 함수
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// 알림 로드 함수
function loadNotifications(type) {
    fetch(`/api/notifications/${type}/`)
        .then(response => response.json())
        .then(data => {
            updateNotificationBox(data.notifications);
        })
        .catch(error => {
            console.error('Error loading notifications:', error);
        });
}

// 알림 박스 업데이트
function updateNotificationBox(notifications) {
    const alarmCon = document.querySelector('.alarmCon');
    if (!alarmCon) return;
    
    alarmCon.innerHTML = '';
    
    if (notifications.length === 0) {
        alarmCon.innerHTML = '<span class="alarmSub">새로운 알림이 없습니다.</span>';
        return;
    }
    
    notifications.forEach(notification => {
        const notificationEl = document.createElement('div');
        notificationEl.className = 'notification-item';
        notificationEl.innerHTML = `
            <span class="alarmName">${notification.title}</span>
            <span class="alarmWirter">${notification.author}</span><br>
            <span class="alarmSub">${notification.content}</span><br>
        `;
        alarmCon.appendChild(notificationEl);
    });
}
