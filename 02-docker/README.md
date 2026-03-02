# 02. Docker 배포

## Docker란?

Docker는 애플리케이션과 그 실행 환경을 **컨테이너**라는 단위로 패키징하는 기술입니다.

> **컨테이너 = 앱 코드 + 런타임 + 라이브러리 + 설정**

"내 PC에서는 되는데 서버에서 안 돼요" 문제를 근본적으로 해결합니다. 어디서든 동일한 컨테이너를 실행하면 동일하게 동작합니다.

```
┌─────────────────────────────────────────────┐
│              Physical Server                 │
├─────────────────────────────────────────────┤
│                    OS                        │
├─────────────────────────────────────────────┤
│              Docker Engine                   │
├──────────────┬──────────────┬───────────────┤
│ Container A  │ Container B  │ Container C   │
│ ┌──────────┐ │ ┌──────────┐ │ ┌───────────┐ │
│ │ Flask App│ │ │  nginx   │ │ │  Redis    │ │
│ │ Python   │ │ │          │ │ │           │ │
│ └──────────┘ │ └──────────┘ │ └───────────┘ │
└──────────────┴──────────────┴───────────────┘
```

## BareMetal과 비교

| 항목 | BareMetal | Docker |
|------|-----------|--------|
| 환경 구성 | 서버마다 수동 설치 | Dockerfile로 정의 |
| 이식성 | 서버 종속적 | 어디서든 동일 실행 |
| 격리 | 프로세스 수준 | 컨테이너 수준 (파일시스템, 네트워크) |
| 시작 시간 | 수분 (부팅) | 수초 (컨테이너 생성) |
| 리소스 | 서버 전체 점유 | 필요한 만큼만 사용 |

## 핵심 개념

### 이미지 (Image)
컨테이너의 **설계도**. Dockerfile로 만들며, 읽기 전용입니다.

```
이미지 = "Ubuntu + Python 3.12 + Flask + 내 앱 코드"
```

### 컨테이너 (Container)
이미지를 **실행한 인스턴스**. 하나의 이미지로 여러 컨테이너를 만들 수 있습니다.

```
이미지 : 컨테이너 = 클래스 : 객체 = 레시피 : 요리
```

### 레이어 (Layer)
이미지는 여러 **레이어**가 쌓인 구조입니다. 변경된 레이어만 다시 빌드하여 속도를 높입니다.

```
Layer 4: COPY app/ .            ← 코드 변경 시 여기만 재빌드
Layer 3: RUN pip install ...    ← requirements.txt 변경 시
Layer 2: COPY requirements.txt
Layer 1: FROM python:3.12-slim  ← 베이스 이미지 (캐시됨)
```

### 레지스트리 (Registry)
이미지를 저장하고 공유하는 **저장소**. Docker Hub가 대표적입니다.

## Dockerfile 해설

```dockerfile
# 베이스 이미지: Python 3.12 경량 버전
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일만 먼저 복사 (캐시 최적화)
COPY app/requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY app/ .

# 환경변수 설정
ENV DEPLOY_ENV=docker

# 컨테이너가 사용할 포트 선언
EXPOSE 5000

# 컨테이너 시작 시 실행할 명령
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

**왜 requirements.txt를 먼저 복사할까?**

Docker는 레이어를 캐시합니다. 코드만 변경하면 `pip install` 레이어는 캐시에서 재사용되어 빌드가 빨라집니다.

## Step-by-step 배포

### 1단계: Docker 설치

```bash
# Ubuntu
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

### 2단계: 이미지 빌드

```bash
# 프로젝트 루트에서 실행
docker build -t infra-tutorial -f 02-docker/Dockerfile .
```

```
✅ 빌드 완료 메시지:
Successfully tagged infra-tutorial:latest
```

### 3단계: 컨테이너 실행

```bash
docker run -d \
  --name my-app \
  -p 5000:5000 \
  -e DEPLOY_ENV=docker \
  infra-tutorial
```

| 옵션 | 의미 |
|------|------|
| `-d` | 백그라운드 실행 (detach) |
| `--name` | 컨테이너 이름 지정 |
| `-p 5000:5000` | 호스트:컨테이너 포트 매핑 |
| `-e` | 환경변수 설정 |

브라우저에서 `http://localhost:5000` 접속하여 확인합니다.

### 4단계: 컨테이너 관리

```bash
# 실행 중인 컨테이너 확인
docker ps

# 로그 확인
docker logs -f my-app

# 컨테이너 내부 접속
docker exec -it my-app /bin/bash

# 컨테이너 중지/삭제
docker stop my-app
docker rm my-app
```

### 5단계: Docker Compose로 실행

`docker-compose.yml`을 사용하면 앱 + nginx를 한 번에 실행할 수 있습니다.

```bash
cd 02-docker
docker compose up -d
```

```
✅ 결과:
- http://localhost:5000 → Flask 앱 직접 접근
- http://localhost:80   → nginx를 통한 접근
```

```bash
# 중지
docker compose down
```

## Docker Compose 해설

```yaml
services:
  app:                          # Flask 앱 서비스
    build:
      context: ..               # 빌드 컨텍스트 = 프로젝트 루트
      dockerfile: 02-docker/Dockerfile
    ports:
      - "5000:5000"             # 포트 매핑
    restart: unless-stopped     # 자동 재시작

  nginx:                        # 리버스 프록시 서비스
    image: nginx:alpine         # 공식 nginx 이미지 사용
    ports:
      - "80:80"
    depends_on:                 # app이 먼저 시작되어야 함
      app:
        condition: service_healthy
```

## 생각해보기

> "컨테이너를 10개로 늘려야 한다면? 하나가 죽으면 누가 다시 살릴까?"

Docker만으로도 컨테이너를 실행할 수 있지만:
1. 컨테이너 **수십~수백 개**가 되면 수동 관리가 불가능
2. **자동 확장/축소** (트래픽에 따라)가 필요
3. 컨테이너가 죽으면 **자동으로 재시작**하는 시스템이 필요
4. **무중단 배포** (롤링 업데이트)가 필요

이 문제를 해결하기 위해 등장한 것이 **Kubernetes** 입니다.

→ [03-kubernetes](../03-kubernetes/) 에서 계속
