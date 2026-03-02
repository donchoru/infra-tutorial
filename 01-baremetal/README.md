# 01. BareMetal 배포

## BareMetal이란?

BareMetal(베어메탈)은 **물리 서버에 OS를 직접 설치하고, 그 위에 애플리케이션을 실행**하는 전통적인 배포 방식입니다.

"BareMetal"은 문자 그대로 "벌거벗은 금속" — 가상화 계층 없이 하드웨어 위에 바로 소프트웨어가 올라간다는 뜻입니다.

```
┌─────────────────────────┐
│      Application        │  ← 우리가 만든 Flask 앱
├─────────────────────────┤
│    Runtime (Python)      │  ← Python, pip, gunicorn
├─────────────────────────┤
│   OS (Ubuntu, CentOS)   │  ← 직접 설치한 운영체제
├─────────────────────────┤
│     Physical Server      │  ← 실제 하드웨어
└─────────────────────────┘
```

## 장단점

### 장점
- **최고 성능**: 가상화 오버헤드 없음
- **단순함**: 이해하기 쉬운 구조
- **완전한 제어**: 하드웨어부터 OS까지 모든 설정 가능

### 단점
- **환경 불일치**: "내 PC에서는 되는데..." 문제
- **확장 어려움**: 서버 추가 시 동일 환경 구성을 반복
- **복구 느림**: 서버 장애 시 수동 복구
- **리소스 낭비**: 하나의 앱이 서버 전체를 점유

## 구성 요소

| 구성 요소 | 역할 |
|-----------|------|
| **Python** | 애플리케이션 런타임 |
| **gunicorn** | WSGI 서버 (프로덕션용 앱 서버) |
| **systemd** | 프로세스 관리 (자동 시작, 재시작) |
| **nginx** | 리버스 프록시 (선택사항) |

## 아키텍처

```
                    ┌──────────────┐
   Client ────────▶ │    nginx     │ :80
                    │ (reverse     │
                    │  proxy)      │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   gunicorn   │ :5000
                    │  (4 workers) │
                    ├──────────────┤
                    │  Flask App   │
                    │  (app.py)    │
                    └──────────────┘
                           │
                    ┌──────▼───────┐
                    │   systemd    │
                    │ (프로세스     │
                    │  관리자)      │
                    └──────────────┘
```

## Step-by-step 배포

### 1단계: 시스템 패키지 설치

```bash
# Ubuntu/Debian 기준
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx
```

### 2단계: 프로젝트 클론 및 가상환경 설정

```bash
cd /opt
sudo git clone <repo-url> infra-tutorial
cd infra-tutorial

# Python 가상환경 생성
python3 -m venv .venv
source .venv/bin/activate

# 의존성 설치
pip install -r app/requirements.txt
```

### 3단계: 환경변수 설정

```bash
export DEPLOY_ENV=baremetal
```

### 4단계: gunicorn으로 실행 테스트

```bash
cd app
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

브라우저에서 `http://<서버IP>:5000` 접속하여 확인합니다.

### 5단계: systemd 서비스 등록

```bash
sudo cp /opt/infra-tutorial/01-baremetal/app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable app
sudo systemctl start app
```

```bash
# 상태 확인
sudo systemctl status app

# 로그 확인
sudo journalctl -u app -f
```

### 6단계: nginx 리버스 프록시 설정 (선택)

```nginx
# /etc/nginx/sites-available/app
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## setup.sh 사용법

이 폴더의 `setup.sh`는 위 과정을 자동화한 스크립트입니다:

```bash
chmod +x 01-baremetal/setup.sh
sudo ./01-baremetal/setup.sh
```

## 생각해보기

> "이 앱을 서버 2대에 배포해야 한다면?"

BareMetal 환경에서는:
1. 새 서버에 **동일한 OS, Python, 패키지를 다시 설치**해야 합니다
2. 버전이 미묘하게 다르면 **"내 서버에서는 되는데..."** 발생
3. 서버마다 **설정 파일을 수동으로 관리**해야 합니다

이 문제를 해결하기 위해 등장한 것이 바로 **Docker** 입니다.

→ [02-docker](../02-docker/) 에서 계속
