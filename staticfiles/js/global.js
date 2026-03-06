/**
 * 글로벌 JavaScript - 세계적인 기능 구현
 * 실시간 통신, 테마 관리, 글로벌 검색, 알림 시스템
 */

// 글로벌 설정
const GlobalConfig = {
    apiBaseUrl: '/api/v1',
    wsUrl: 'ws://127.0.0.1:8000/ws',
    theme: localStorage.getItem('theme') || 'light',
    language: localStorage.getItem('language') || 'ko',
    notifications: {
        enabled: true,
        sound: true,
        desktop: true
    }
};

// 글로벌 유틸리티 함수
class GlobalUtils {
    static formatDate(date, format = 'YYYY-MM-DD') {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        const seconds = String(d.getSeconds()).padStart(2, '0');
        
        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day)
            .replace('HH', hours)
            .replace('mm', minutes)
            .replace('ss', seconds);
    }
    
    static formatNumber(number, decimals = 0) {
        return new Intl.NumberFormat('ko-KR', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(number);
    }
    
    static formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    static throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    static getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
    
    static setCookie(name, value, days) {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
    }
    
    static deleteCookie(name) {
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/`;
    }
    
    static sanitizeHtml(html) {
        const div = document.createElement('div');
        div.textContent = html;
        return div.innerHTML;
    }
    
    static generateId() {
        return Math.random().toString(36).substr(2, 9);
    }
    
    static copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            showGlobalAlert('success', '클립보드에 복사되었습니다.');
        }).catch(err => {
            console.error('클립보드 복사 실패:', err);
            showGlobalAlert('error', '클립보드 복사에 실패했습니다.');
        });
    }
    
    static downloadFile(url, filename) {
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    static validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    static validatePhone(phone) {
        const re = /^[\d-]+$/;
        return re.test(phone);
    }
    
    static validateUrl(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }
}

// 글로벌 알림 시스템
class GlobalAlert {
    static show(type, message, duration = 5000) {
        const alertContainer = document.getElementById('globalAlerts');
        if (!alertContainer) return;
        
        const alertId = GlobalUtils.generateId();
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${type} alert-dismissible`;
        alertElement.id = `alert-${alertId}`;
        
        const icon = this.getIcon(type);
        alertElement.innerHTML = `
            <div class="alert-content">
                <i class="fas ${icon}"></i>
                <span class="alert-message">${message}</span>
                <button class="alert-close" onclick="GlobalAlert.close('${alertId}')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        alertContainer.appendChild(alertElement);
        
        // 자동 제거
        if (duration > 0) {
            setTimeout(() => {
                this.close(alertId);
            }, duration);
        }
        
        // 사운드 알림
        if (GlobalConfig.notifications.sound) {
            this.playSound(type);
        }
        
        // 데스크톱 알림
        if (GlobalConfig.notifications.desktop && Notification.permission === 'granted') {
            this.showDesktopNotification(type, message);
        }
    }
    
    static close(alertId) {
        const alertElement = document.getElementById(`alert-${alertId}`);
        if (alertElement) {
            alertElement.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                alertElement.remove();
            }, 300);
        }
    }
    
    static getIcon(type) {
        const icons = {
            'success': 'fa-check-circle',
            'warning': 'fa-exclamation-triangle',
            'error': 'fa-exclamation-circle',
            'info': 'fa-info-circle'
        };
        return icons[type] || icons['info'];
    }
    
    static playSound(type) {
        const sounds = {
            'success': 'success.mp3',
            'warning': 'warning.mp3',
            'error': 'error.mp3',
            'info': 'info.mp3'
        };
        
        const audio = new Audio(`/static/sounds/${sounds[type] || sounds['info']}`);
        audio.volume = 0.3;
        audio.play().catch(e => console.log('사운드 재생 실패:', e));
    }
    
    static showDesktopNotification(type, message) {
        const titles = {
            'success': '성공',
            'warning': '경고',
            'error': '오류',
            'info': '정보'
        };
        
        new Notification(titles[type] || titles['info'], {
            body: message,
            icon: '/static/images/favicon.ico'
        });
    }
}

// 글로벌 검색 시스템
class GlobalSearch {
    constructor() {
        this.searchInput = document.getElementById('globalSearch');
        this.searchResults = document.getElementById('globalSearchResults');
        this.searchContent = document.getElementById('searchResultsContent');
        this.isSearching = false;
        this.searchTimeout = null;
        
        this.init();
    }
    
    init() {
        if (this.searchInput) {
            this.searchInput.addEventListener('input', GlobalUtils.debounce(this.handleSearch.bind(this), 300));
            this.searchInput.addEventListener('keypress', this.handleKeyPress.bind(this));
        }
        
        // ESC 키로 검색 닫기
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.close();
            }
        });
    }
    
    handleSearch(event) {
        const query = event.target.value.trim();
        
        if (query.length < 2) {
            this.close();
            return;
        }
        
        this.search(query);
    }
    
    handleKeyPress(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            this.search(event.target.value.trim());
        }
    }
    
    async search(query) {
        if (this.isSearching) return;
        
        this.isSearching = true;
        this.showLoading();
        
        try {
            const response = await fetch(`${GlobalConfig.apiBaseUrl}/search/?q=${encodeURIComponent(query)}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayResults(data.data.results);
            } else {
                this.showError(data.message || '검색에 실패했습니다.');
            }
        } catch (error) {
            console.error('검색 오류:', error);
            this.showError('검색에 실패했습니다.');
        } finally {
            this.isSearching = false;
        }
    }
    
    displayResults(results) {
        if (!this.searchContent) return;
        
        if (results.length === 0) {
            this.searchContent.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search"></i>
                    <p>검색 결과가 없습니다.</p>
                </div>
            `;
        } else {
            this.searchContent.innerHTML = results.map(result => `
                <div class="search-result-item" onclick="GlobalSearch.navigateToResult('${result.type}', '${result.id}', '${result.url}')">
                    <div class="result-icon">
                        <i class="fas ${this.getResultIcon(result.type)}"></i>
                    </div>
                    <div class="result-content">
                        <div class="result-title">${result.title}</div>
                        <div class="result-preview">${result.preview}</div>
                        <div class="result-meta">
                            <span class="result-type">${this.getResultType(result.type)}</span>
                            <span class="result-date">${GlobalUtils.formatDate(result.date)}</span>
                        </div>
                    </div>
                </div>
            `).join('');
        }
        
        this.show();
    }
    
    showLoading() {
        if (!this.searchContent) return;
        
        this.searchContent.innerHTML = `
            <div class="search-loading">
                <div class="loading-spinner"></div>
                <p>검색 중...</p>
            </div>
        `;
        
        this.show();
    }
    
    showError(message) {
        if (!this.searchContent) return;
        
        this.searchContent.innerHTML = `
            <div class="search-error">
                <i class="fas fa-exclamation-circle"></i>
                <p>${message}</p>
            </div>
        `;
        
        this.show();
    }
    
    show() {
        if (this.searchResults) {
            this.searchResults.classList.add('show');
        }
    }
    
    close() {
        if (this.searchResults) {
            this.searchResults.classList.remove('show');
        }
        if (this.searchInput) {
            this.searchInput.value = '';
        }
    }
    
    navigateToResult(type, id, url) {
        window.location.href = url;
    }
    
    getResultIcon(type) {
        const icons = {
            'notice': 'fa-bullhorn',
            'technology': 'fa-code',
            'client': 'fa-building',
            'user': 'fa-user',
            'project': 'fa-project-diagram',
            'document': 'fa-file-alt'
        };
        return icons[type] || icons['document'];
    }
    
    getResultType(type) {
        const types = {
            'notice': '공지사항',
            'technology': '기술',
            'client': '거래처',
            'user': '사용자',
            'project': '프로젝트',
            'document': '문서'
        };
        return types[type] || types['document'];
    }
}

// 실시간 통신 시스템
class RealtimeManager {
    constructor() {
        this.connections = new Map();
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        
        this.init();
    }
    
    init() {
        this.connectNotifications();
        this.connectSystemStatus();
        
        // 페이지 가시성 변경 시 연결 관리
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.disconnectAll();
            } else {
                this.reconnectAll();
            }
        });
    }
    
    connectNotifications() {
        this.connect('notifications', '/ws/notifications/', (data) => {
            this.handleNotification(data);
        });
    }
    
    connectSystemStatus() {
        this.connect('system-status', '/ws/system-status/', (data) => {
            this.handleSystemStatus(data);
        });
    }
    
    connect(name, endpoint, onMessage) {
        if (this.connections.has(name)) {
            this.disconnect(name);
        }
        
        try {
            const ws = new WebSocket(`${GlobalConfig.wsUrl}${endpoint}`);
            
            ws.onopen = () => {
                console.log(`${name} WebSocket 연결 성공`);
                this.reconnectAttempts = 0;
            };
            
            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    onMessage(data);
                } catch (error) {
                    console.error(`${name} WebSocket 메시지 파싱 오류:`, error);
                }
            };
            
            ws.onclose = () => {
                console.log(`${name} WebSocket 연결 종료`);
                this.connections.delete(name);
                this.attemptReconnect(name, endpoint, onMessage);
            };
            
            ws.onerror = (error) => {
                console.error(`${name} WebSocket 오류:`, error);
            };
            
            this.connections.set(name, ws);
        } catch (error) {
            console.error(`${name} WebSocket 연결 실패:`, error);
        }
    }
    
    disconnect(name) {
        const ws = this.connections.get(name);
        if (ws) {
            ws.close();
            this.connections.delete(name);
        }
    }
    
    disconnectAll() {
        this.connections.forEach((ws, name) => {
            this.disconnect(name);
        });
    }
    
    reconnectAll() {
        this.connectNotifications();
        this.connectSystemStatus();
    }
    
    attemptReconnect(name, endpoint, onMessage) {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.log(`${name} WebSocket 재연결 시도 초과`);
            return;
        }
        
        setTimeout(() => {
            this.reconnectAttempts++;
            console.log(`${name} WebSocket 재연결 시도 ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
            this.connect(name, endpoint, onMessage);
        }, this.reconnectDelay * this.reconnectAttempts);
    }
    
    handleNotification(data) {
        if (data.type === 'notification') {
            const notification = data.notification;
            
            // 알림 표시
            GlobalAlert.show(notification.level, notification.message);
            
            // 알림 카운트 업데이트
            this.updateNotificationCount(data.unread_count);
            
            // 알림 목록 새로고침
            if (typeof loadNotifications === 'function') {
                loadNotifications();
            }
        }
    }
    
    handleSystemStatus(data) {
        if (data.type === 'system_status') {
            this.updateSystemStatus(data.status);
        }
    }
    
    updateNotificationCount(count) {
        const badge = document.getElementById('notificationCount');
        if (badge) {
            if (count > 0) {
                badge.textContent = count > 99 ? '99+' : count;
                badge.style.display = 'block';
            } else {
                badge.style.display = 'none';
            }
        }
    }
    
    updateSystemStatus(status) {
        const statusIndicator = document.getElementById('systemStatus');
        if (statusIndicator) {
            statusIndicator.className = `status-indicator status-${status}`;
            statusIndicator.title = `시스템 상태: ${status}`;
        }
    }
    
    send(name, data) {
        const ws = this.connections.get(name);
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(data));
        }
    }
}

// 테마 관리 시스템
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }
    
    init() {
        this.applyTheme(this.currentTheme);
        this.setupThemeToggle();
        
        // 시스템 테마 감지
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            if (!localStorage.getItem('theme')) {
                this.applyTheme('dark');
            }
        }
        
        // 시스템 테마 변경 감지
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
    
    applyTheme(theme) {
        document.body.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
        
        // 테마 아이콘 업데이트
        this.updateThemeIcons(theme);
        
        // 테마 변경 이벤트 발생
        document.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
    }
    
    toggle() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    }
    
    updateThemeIcons(theme) {
        const icons = document.querySelectorAll('#themeIcon, #footerThemeIcon');
        icons.forEach(icon => {
            if (theme === 'dark') {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        });
    }
    
    setupThemeToggle() {
        const themeButtons = document.querySelectorAll('.theme-btn');
        themeButtons.forEach(button => {
            button.addEventListener('click', () => {
                this.toggle();
            });
        });
    }
}

// 글로벌 함수들
function showGlobalAlert(type, message, duration) {
    GlobalAlert.show(type, message, duration);
}

function closeGlobalSearch() {
    if (window.globalSearch) {
        window.globalSearch.close();
    }
}

function toggleTheme() {
    if (window.themeManager) {
        window.themeManager.toggle();
    }
}

function getCookie(name) {
    return GlobalUtils.getCookie(name);
}

function setCookie(name, value, days) {
    GlobalUtils.setCookie(name, value, days);
}

function deleteCookie(name) {
    GlobalUtils.deleteCookie(name);
}

// 초기화
document.addEventListener('DOMContentLoaded', function() {
    // 글로벌 검색 초기화
    window.globalSearch = new GlobalSearch();
    
    // 실시간 통신 초기화
    window.realtimeManager = new RealtimeManager();
    
    // 테마 관리 초기화
    window.themeManager = new ThemeManager();
    
    // 데스크톱 알림 권한 요청
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
    
    // 글로벌 이벤트 리스너
    document.addEventListener('click', function(e) {
        // 외부 클릭으로 드롭다운 닫기
        if (!e.target.closest('.notification-bell')) {
            document.getElementById('notificationDropdown')?.classList.remove('show');
        }
        
        if (!e.target.closest('.user-menu')) {
            document.getElementById('userDropdown')?.classList.remove('show');
        }
        
        if (!e.target.closest('.global-search-results')) {
            closeGlobalSearch();
        }
    });
    
    // 키보드 단축키
    document.addEventListener('keydown', function(e) {
        // Ctrl+K 또는 Cmd+K로 글로벌 검색 열기
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('globalSearch');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Ctrl+/로 테마 토글
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            toggleTheme();
        }
    });
});

// 전역 변수들
window.GlobalUtils = GlobalUtils;
window.GlobalAlert = GlobalAlert;
window.GlobalSearch = GlobalSearch;
window.RealtimeManager = RealtimeManager;
window.ThemeManager = ThemeManager;
