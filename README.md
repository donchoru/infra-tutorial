# Infra Tutorial

동일한 Flask 앱을 **BareMetal → Docker → Kubernetes** 3가지 환경에 배포하며 각 기술의 개념과 차이점을 배웁니다.

## 학습 로드맵

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ 01-BareMetal │ ──▶ │  02-Docker  │ ──▶ │    03-K8s   │
│             │     │             │     │             │
│ 물리 서버에   │     │ 컨테이너로   │     │ 오케스트레이션│
│ 직접 배포    │     │ 환경 패키징   │     │ 으로 자동 관리│
└─────────────┘     └─────────────┘     └─────────────┘
```

각 단계는 이전 단계의 **문제점**을 해결하기 위해 등장했습니다:

### BareMetal의 한계 → Docker가 해결

BareMetal 환경에서는 서버에 Python, pip, 라이브러리를 **직접 설치**합니다. 잘 돌아가는 것 같지만, 현실에서 이런 일이 생깁니다:

> **개발자 A**: "내 PC(Ubuntu 22.04, Python 3.11)에서는 잘 되는데요?"
> **개발자 B**: "제 PC(macOS, Python 3.9)에서는 에러나는데요..."
> **운영팀**: "서버(CentOS 7, Python 3.6)에 배포했더니 안 됩니다"

서버를 2대로 늘리려면? **똑같은 설치 과정을 처음부터 반복**합니다. OS 버전, Python 버전, 라이브러리 버전이 조금이라도 다르면 장애가 발생합니다. 서버가 10대면? 10번 반복합니다.

**Docker**는 앱 + 런타임 + 라이브러리를 통째로 **이미지 하나로 패키징**합니다. 이 이미지만 있으면 어떤 서버에서든 `docker run` 한 줄로 동일하게 실행됩니다. "내 PC에서는 되는데" 문제가 원천적으로 사라집니다.

### Docker의 한계 → Kubernetes가 해결

Docker로 컨테이너를 만들면 배포는 편해집니다. 하지만 서비스가 성장하면 새로운 고민이 생깁니다:

> **"Black Friday 트래픽이 10배로 뛰었는데, 컨테이너를 수동으로 늘려야 하나요?"**
> **"새벽 3시에 컨테이너가 죽었는데, 누가 다시 살리죠?"**
> **"새 버전을 배포하는 동안 서비스가 중단돼도 되나요?"**

컨테이너가 3~5개일 때는 `docker run`을 몇 번 치면 됩니다. 하지만 **수십~수백 개**가 되면:
- 어떤 서버에 어떤 컨테이너가 있는지 파악이 안 되고
- 하나가 죽어도 알아차리기 어렵고
- 트래픽에 따라 수동으로 늘렸다 줄였다 하는 건 불가능합니다

**Kubernetes**는 "이 앱을 항상 3개 유지해줘"라고 **선언**하면, 나머지는 알아서 합니다. 컨테이너가 죽으면 자동 재생성(Self-healing), 트래픽이 늘면 자동 확장(HPA), 새 버전은 하나씩 교체하며 무중단 배포(Rolling Update)합니다.

## 프로젝트 구조

```
infra-tutorial/
├── app/                     # 예제 Flask 앱 (공통)
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│       └── index.html
│
├── 01-baremetal/            # BareMetal 배포
│   ├── README.md            # 개념 설명 + 실습 가이드
│   ├── setup.sh             # 자동 배포 스크립트
│   └── app.service          # systemd 서비스 파일
│
├── 02-docker/               # Docker 배포
│   ├── README.md            # 개념 설명 + 실습 가이드
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── docker-compose.yml   # app + nginx
│   └── nginx.conf
│
├── 03-kubernetes/           # Kubernetes 배포
│   ├── README.md            # 개념 설명 + 실습 가이드
│   └── manifests/
│       ├── namespace.yaml
│       ├── configmap.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       └── ingress.yaml
│
└── docs/
    ├── comparison.md        # 3가지 환경 비교표
    └── glossary.md          # 용어 사전 (한글)
```

## 예제 앱

모든 챕터에서 동일한 Flask 앱을 사용합니다.

| 엔드포인트 | 설명 |
|-----------|------|
| `GET /` | 호스트명, IP, 배포 환경, 가동시간을 표시하는 웹 페이지 |
| `GET /health` | 헬스체크 (`{"status": "ok"}`) |
| `GET /info` | 서버 정보 JSON (Python 버전, OS, 환경변수 등) |

환경변수 `DEPLOY_ENV`로 배포 환경을 구분합니다 (`local` / `baremetal` / `docker` / `kubernetes`).

## 빠른 시작

```bash
# 앱 로컬 실행 (Python 필요)
cd app
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

## 학습 순서

1. **[01-BareMetal](01-baremetal/)** — 서버에 직접 설치하는 전통적 배포
2. **[02-Docker](02-docker/)** — 컨테이너로 환경을 패키징하여 배포
3. **[03-Kubernetes](03-kubernetes/)** — 컨테이너를 자동으로 관리/확장하는 플랫폼
4. **[비교표](docs/comparison.md)** — 3가지 환경 한눈에 비교
5. **[용어 사전](docs/glossary.md)** — 핵심 용어 정리

## 사전 준비

| 챕터 | 필요한 것 |
|------|----------|
| 01-BareMetal | Python 3.10+, Linux 서버 (또는 VM) |
| 02-Docker | Docker Desktop 또는 Docker Engine |
| 03-Kubernetes | Docker + minikube + kubectl |

## 핵심 비교

| 항목 | BareMetal | Docker | Kubernetes |
|------|-----------|--------|------------|
| 배포 단위 | 프로세스 | 컨테이너 | Pod |
| 확장 | 수동 (서버 추가) | 수동 (컨테이너 추가) | 자동 (HPA) |
| 장애 복구 | systemd | restart policy | Self-healing |
| 업데이트 | 서비스 중단 | 컨테이너 교체 | 롤링 업데이트 |

→ 자세한 비교는 [docs/comparison.md](docs/comparison.md)
