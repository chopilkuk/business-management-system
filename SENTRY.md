# Sentry 연동 가이드

1. Sentry 프로젝트 생성
2. 환경 변수에 `SENTRY_DSN` 추가
3. `sentry-sdk` 설치 (requirements.txt에 이미 포함됨)
4. `business_management/settings.py`에 초기화 코드 추가:

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.0,
    send_default_pii=False,
)
```

5. 배포 환경에서 `traces_sample_rate`를 적절히 설정하고 `DEBUG=False`로 운영하세요.
