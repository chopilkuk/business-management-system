/**
 * 실시간 데이터 연동 JavaScript 모듈
 * 
 * 이 모듈은 실시간 데이터 업데이트, AJAX 요청 처리,
 * WebSocket 연결 등을 관리합니다.
 * 
 * 주요 기능:
 * - 실시간 공지사항 업데이트
 * - 실시간 알림 시스템
 * - AJAX 기반 데이터 처리
 * - WebSocket 연결 관리
 */

// 전역 변수
let websocket = null;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

/**
 * WebSocket 연결 초기화
 */
function initWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;
    
    try {
        websocket = new WebSocket(wsUrl);
        
        websocket.onopen = function(event) {
            console.log('WebSocket 연결 성공');
            reconnectAttempts = 0;
            showNotification('실시간 연결이 성공적으로 설정되었습니다.', 'success');
        };
        
        websocket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            handleRealtimeUpdate(data);
        };
        
        websocket.onclose = function(event) {
            console.log('WebSocket 연결 종료');
            attemptReconnect();
        };
        
        websocket.onerror = function(error) {
            console.error('WebSocket 오류:', error);
            showNotification('실시간 연결에 오류가 발생했습니다.', 'error');
        };
    } catch (error) {
        console.error('WebSocket 초기화 오류:', error);
    }
}

/**
 * WebSocket 재연결 시도
 */
function attemptReconnect() {
    if (reconnectAttempts < maxReconnectAttempts) {
        reconnectAttempts++;
        console.log(`WebSocket 재연결 시도 ${reconnectAttempts}/${maxReconnectAttempts}`);
        
        setTimeout(() => {
            initWebSocket();
        }, 5000 * reconnectAttempts); // 점진적 지연
    } else {
        console.log('WebSocket 재연결 최대 시도 초과');
        showNotification('실시간 연결을 다시 시도해주세요.', 'warning');
    }
}

/**
 * 실시간 업데이트 처리
 */
function handleRealtimeUpdate(data) {
    switch (data.type) {
        case 'notice_created':
            handleNewNotice(data.payload);
            break;
        case 'notice_updated':
            handleUpdatedNotice(data.payload);
            break;
        case 'notice_deleted':
            handleDeletedNotice(data.payload);
            break;
        case 'notification':
            handleNotification(data.payload);
            break;
        default:
            console.log('알 수 없는 실시간 업데이트 타입:', data.type);
    }
}

/**
 * 새 공지사항 처리
 */
function handleNewNotice(notice) {
    showNotification(`새 공지사항: ${notice.title}`, 'info');
    
    // 공지사항 목록이 있는 경우 즉시 업데이트
    if (window.location.pathname.includes('/공지사항/')) {
        updateNoticeList();
    }
    
    // 알림 목록 업데이트
    updateNotificationList();
}

/**
 * 공지사항 업데이트 처리
 */
function handleUpdatedNotice(notice) {
    showNotification(`공지사항이 업데이트되었습니다: ${notice.title}`, 'info');
    
    // 상세 페이지인 경우 즉시 업데이트
    if (window.location.pathname.includes('/공지사항/') && 
        window.location.pathname.split('/').length > 2) {
        updateNoticeDetail(notice.id);
    }
}

/**
 * 공지사항 삭제 처리
 */
function handleDeletedNotice(notice) {
    showNotification(`공지사항이 삭제되었습니다: ${notice.title}`, 'warning');
    
    // 목록 페이지인 경우 즉시 업데이트
    if (window.location.pathname.includes('/공지사항/')) {
        updateNoticeList();
    }
    
    // 상세 페이지인 경우 목록으로 리다이렉트
    if (window.location.pathname.split('/').length > 2) {
        window.location.href = '/공지사항/';
    }
}

/**
 * 알림 처리
 */
function handleNotification(notification) {
    showNotification(notification.message, notification.level);
    updateNotificationList();
}

/**
 * 공지사항 목록 업데이트 (AJAX)
 */
function updateNoticeList() {
    fetch('/공지사항/api/list/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            renderNoticeList(data.notices);
        }
    })
    .catch(error => {
        console.error('공지사항 목록 업데이트 오류:', error);
    });
}

/**
 * 공지사항 상세 업데이트 (AJAX)
 */
function updateNoticeDetail(noticeId) {
    fetch(`/공지사항/api/${noticeId}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            renderNoticeDetail(data.notice);
        }
    })
    .catch(error => {
        console.error('공지사항 상세 업데이트 오류:', error);
    });
}

/**
 * 알림 목록 업데이트 (AJAX)
 */
function updateNotificationList() {
    fetch('/api/notifications/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            renderNotifications(data.notifications);
        }
    })
    .catch(error => {
        console.error('알림 목록 업데이트 오류:', error);
    });
}

/**
 * 공지사항 목록 렌더링
 */
function renderNoticeList(notices) {
    const container = document.querySelector('.notice-list');
    if (container) {
        container.innerHTML = notices.map(notice => `
            <div class="notice-item" data-id="${notice.id}">
                <div class="notice-header">
                    <span class="notice-title">${notice.title}</span>
                    <span class="notice-importance importance-${notice.importance}">${notice.importance_display}</span>
                </div>
                <div class="notice-meta">
                    <span class="notice-author">${notice.author}</span>
                    <span class="notice-date">${formatDate(notice.created_at)}</span>
                    <span class="notice-views">조회: ${notice.view_count}</span>
                </div>
                <div class="notice-preview">
                    ${notice.content.substring(0, 100)}${notice.content.length > 100 ? '...' : ''}
                </div>
                <div class="notice-actions">
                    <a href="/공지사항/${notice.id}/" class="btn btn-primary btn-sm">상세보기</a>
                </div>
            </div>
        `).join('');
    }
}

/**
 * 공지사항 상세 렌더링
 */
function renderNoticeDetail(notice) {
    const container = document.querySelector('.notice-detail');
    if (container) {
        container.innerHTML = `
            <div class="notice-header">
                <h1>${notice.title}</h1>
                <div class="notice-meta">
                    <span class="notice-importance importance-${notice.importance}">${notice.importance_display}</span>
                    <span class="notice-status status-${notice.status}">${notice.status_display}</span>
                    <span class="notice-author">작성자: ${notice.author}</span>
                    <span class="notice-date">${formatDate(notice.created_at)}</span>
                    <span class="notice-views">조회수: ${notice.view_count}</span>
                </div>
            </div>
            <div class="notice-content">
                ${notice.content.replace(/\n/g, '<br>')}
            </div>
            <div class="notice-actions">
                ${notice.can_edit ? `<a href="/공지사항/${notice.id}/edit/" class="btn btn-warning">수정</a>` : ''}
                ${notice.can_delete ? `<a href="/공지사항/${notice.id}/delete/" class="btn btn-danger">삭제</a>` : ''}
                ${notice.can_publish ? `<a href="/공지사항/${notice.id}/publish/" class="btn btn-success">게시</a>` : ''}
                ${notice.can_archive ? `<a href="/공지사항/${notice.id}/archive/" class="btn btn-secondary">보관</a>` : ''}
            </div>
        `;
    }
}

/**
 * 알림 목록 렌더링
 */
function renderNotifications(notifications) {
    const container = document.querySelector('.alarmCon');
    if (container) {
        if (notifications.length === 0) {
            container.innerHTML = '<span class="alarmSub">새로운 알림이 없습니다.</span>';
        } else {
            container.innerHTML = notifications.map(notification => `
                <div class="notification-item">
                    <span class="notification-title">${notification.title}</span>
                    <span class="notification-author">${notification.author}</span><br>
                    <span class="notification-content">${notification.content}</span><br>
                </div>
            `).join('');
        }
    }
}

/**
 * 날짜 포맷팅
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * 알림 표시
 */
function showNotification(message, type = 'info') {
    // 기존 메시지 시스템 사용
    if (typeof showMessage === 'function') {
        showMessage(message, type);
    } else {
        // 커스텀 알림 생성
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show`;
        notification.style.cssText = `
            position: fixed;
            top: 70px;
            right: 20px;
            z-index: 1050;
            max-width: 400px;
            padding: 12px 16px;
            margin-bottom: 10px;
            border: 1px solid transparent;
            border-radius: 8px;
            animation: slideInRight 0.3s ease-out;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        `;
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()">×</button>
        `;
        
        document.body.appendChild(notification);
        
        // 5초 후 자동 제거
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }
}

/**
 * AJAX 폼 제출
 */
function submitFormAjax(form, successCallback, errorCallback) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    // 제출 버튼 비활성화
    submitButton.disabled = true;
    submitButton.textContent = '처리 중...';
    
    fetch(form.action, {
        method: form.method,
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (successCallback) successCallback(data);
            showNotification(data.message || '처리가 완료되었습니다.', 'success');
        } else {
            if (errorCallback) errorCallback(data);
            showNotification(data.message || '처리 중 오류가 발생했습니다.', 'error');
        }
    })
    .catch(error => {
        console.error('AJAX 폼 제출 오류:', error);
        showNotification('네트워크 오류가 발생했습니다.', 'error');
        if (errorCallback) errorCallback({ error: '네트워크 오류' });
    })
    .finally(() => {
        // 제출 버튼 복원
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    });
}

/**
 * 실시간 검색
 */
function setupRealtimeSearch(searchInput, resultsContainer, searchUrl) {
    let searchTimeout;
    
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        const query = e.target.value;
        
        if (query.length < 2) {
            resultsContainer.innerHTML = '';
            return;
        }
        
        searchTimeout = setTimeout(() => {
            fetch(`${searchUrl}?q=${encodeURIComponent(query)}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    renderSearchResults(data.results, resultsContainer);
                }
            })
            .catch(error => {
                console.error('실시간 검색 오류:', error);
            });
        }, 300);
    });
}

/**
 * 검색 결과 렌더링
 */
function renderSearchResults(results, container) {
    if (results.length === 0) {
        container.innerHTML = '<div class="no-results">검색 결과가 없습니다.</div>';
        return;
    }
    
    container.innerHTML = results.map(result => `
        <div class="search-result" data-id="${result.id}">
            <div class="result-title">${result.title}</div>
            <div class="result-preview">${result.preview}</div>
            <div class="result-meta">
                <span class="result-type">${result.type}</span>
                <span class="result-date">${formatDate(result.date)}</span>
            </div>
        </div>
    `).join('');
}

// 페이지 로드 시점에서 WebSocket 초기화
document.addEventListener('DOMContentLoaded', function() {
    initWebSocket();
    
    // 실시간 검색 설정
    const searchInputs = document.querySelectorAll('[data-realtime-search]');
    searchInputs.forEach(input => {
        const resultsContainer = document.getElementById(input.dataset.resultsContainer);
        if (resultsContainer) {
            setupRealtimeSearch(input, resultsContainer, input.dataset.searchUrl);
        }
    });
    
    // AJAX 폼 설정
    const ajaxForms = document.querySelectorAll('[data-ajax-form]');
    ajaxForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            submitFormAjax(form);
        });
    });
});

// 페이지 언로드 시점에서 WebSocket 연결 종료
window.addEventListener('beforeunload', function() {
    if (websocket) {
        websocket.close();
    }
});
