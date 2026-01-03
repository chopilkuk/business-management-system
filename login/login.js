document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById('loginBtn');
    const idBox = document.getElementById('idBox');
    const pwBox = document.getElementById('pwBox');
    const findId = document.getElementById('findId');
    const findPw = document.getElementById('findPw');
    const join = document.getElementById('join');

    // 로그인 버튼 이벤트
    if (loginBtn) {
        loginBtn.addEventListener('click', function() {
            const username = idBox.value.trim();
            const password = pwBox.value.trim();

            // 입력값 검증
            if (!username) {
                showNotification('아이디를 입력해주세요.', 'error');
                idBox.focus();
                return;
            }

            if (!password) {
                showNotification('비밀번호를 입력해주세요.', 'error');
                pwBox.focus();
                return;
            }

            // 로그인 요청
            performLogin(username, password);
        });
    }

    // Enter 키 로그인
    [idBox, pwBox].forEach(input => {
        if (input) {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    loginBtn.click();
                }
            });
        }
    });

    // 아이디 찾기
    if (findId) {
        findId.addEventListener('click', function() {
            showFindIdModal();
        });
    }

    // 비밀번호 찾기
    if (findPw) {
        findPw.addEventListener('click', function() {
            showFindPwModal();
        });
    }

    // 회원가입
    if (join) {
        join.addEventListener('click', function() {
            window.location.href = '/회원가입/';
        });
    }
});

// 로그인 수행 함수
function performLogin(username, password) {
    const loginBtn = document.getElementById('loginBtn');
    const originalText = loginBtn.value;
    
    // 버튼 상태 변경
    loginBtn.value = '로그인 중...';
    loginBtn.disabled = true;

    // CSRF 토큰 가져오기
    const csrfToken = getCookie('csrftoken');

    fetch('/login/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('로그인 성공!', 'success');
            setTimeout(() => {
                window.location.href = '/home/';
            }, 1000);
        } else {
            showNotification(data.message || '로그인에 실패했습니다.', 'error');
            loginBtn.value = originalText;
            loginBtn.disabled = false;
            pwBox.value = '';
            pwBox.focus();
        }
    })
    .catch(error => {
        console.error('Login error:', error);
        showNotification('서버 연결 오류가 발생했습니다.', 'error');
        loginBtn.value = originalText;
        loginBtn.disabled = false;
    });
}

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

// 아이디 찾기 모달
function showFindIdModal() {
    const modal = createModal('아이디 찾기', `
        <div class="form-group">
            <label>이메일:</label>
            <input type="email" id="findIdEmail" placeholder="가입한 이메일을 입력하세요">
        </div>
        <div class="form-group">
            <label>이름:</label>
            <input type="text" id="findIdName" placeholder="이름을 입력하세요">
        </div>
    `, '아이디 찾기', () => {
        const email = document.getElementById('findIdEmail').value;
        const name = document.getElementById('findIdName').value;
        
        if (!email || !name) {
            showNotification('모든 필드를 입력해주세요.', 'error');
            return;
        }
        
        // 아이디 찾기 API 호출
        findUserId(email, name);
    });
    
    document.body.appendChild(modal);
}

// 비밀번호 찾기 모달
function showFindPwModal() {
    const modal = createModal('비밀번호 찾기', `
        <div class="form-group">
            <label>아이디:</label>
            <input type="text" id="findPwId" placeholder="아이디를 입력하세요">
        </div>
        <div class="form-group">
            <label>이메일:</label>
            <input type="email" id="findPwEmail" placeholder="가입한 이메일을 입력하세요">
        </div>
    `, '비밀번호 재설정', () => {
        const username = document.getElementById('findPwId').value;
        const email = document.getElementById('findPwEmail').value;
        
        if (!username || !email) {
            showNotification('모든 필드를 입력해주세요.', 'error');
            return;
        }
        
        // 비밀번호 재설정 API 호출
        resetPassword(username, email);
    });
    
    document.body.appendChild(modal);
}

// 모달 생성 함수
function createModal(title, content, buttonText, onConfirm) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal">
            <div class="modal-header">
                <h3>${title}</h3>
                <button class="modal-close">&times;</button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
            <div class="modal-footer">
                <button class="modal-cancel">취소</button>
                <button class="modal-confirm">${buttonText}</button>
            </div>
        </div>
        <style>
            .modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
            }
            .modal {
                background: white;
                padding: 20px;
                border-radius: 8px;
                min-width: 300px;
                max-width: 500px;
            }
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }
            .modal-close {
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
            }
            .form-group {
                margin-bottom: 15px;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            .form-group input {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .modal-footer {
                display: flex;
                justify-content: flex-end;
                gap: 10px;
                margin-top: 20px;
            }
            .modal-cancel, .modal-confirm {
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .modal-cancel {
                background: #f5f5f5;
            }
            .modal-confirm {
                background: #007bff;
                color: white;
            }
        </style>
    `;
    
    // 이벤트 리스너
    modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
    modal.querySelector('.modal-cancel').addEventListener('click', () => modal.remove());
    modal.querySelector('.modal-confirm').addEventListener('click', onConfirm);
    
    // 오버레이 클릭 시 닫기
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
    
    return modal;
}

// 아이디 찾기 API 호출
function findUserId(email, name) {
    fetch('/login/api/find-id/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ email, name })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(`아이디: ${data.username}`, 'success');
            document.querySelector('.modal-overlay').remove();
        } else {
            showNotification(data.message || '아이디를 찾을 수 없습니다.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('서버 오류가 발생했습니다.', 'error');
    });
}

// 비밀번호 재설정 API 호출
function resetPassword(username, email) {
    fetch('/login/api/reset-password/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ username, email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('비밀번호 재설정 이메일을 발송했습니다.', 'success');
            document.querySelector('.modal-overlay').remove();
        } else {
            showNotification(data.message || '비밀번호 재설정에 실패했습니다.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('서버 오류가 발생했습니다.', 'error');
    });
}
