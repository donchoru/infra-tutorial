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
- BareMetal: "내 PC에서는 되는데..." → **Docker**가 해결
- Docker: "컨테이너 100개를 어떻게 관리하지?" → **Kubernetes**가 해결

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
