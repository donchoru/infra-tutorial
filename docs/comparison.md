# 3가지 배포 환경 비교

## 한눈에 보기

| 항목 | BareMetal | Docker | Kubernetes |
|------|-----------|--------|------------|
| **배포 단위** | 프로세스 | 컨테이너 | Pod |
| **환경 구성** | 수동 설치 | Dockerfile | Manifest (YAML) |
| **확장** | 서버 추가 (수동) | 컨테이너 추가 (수동) | `replicas: N` (자동 가능) |
| **복구** | systemd restart | restart policy | Self-healing |
| **업데이트** | 서비스 중단 후 교체 | 컨테이너 재생성 | 롤링 업데이트 (무중단) |
| **설정 관리** | 파일, 환경변수 | ENV, Volume | ConfigMap, Secret |
| **네트워킹** | IP + 포트 직접 관리 | 포트 매핑 | Service + Ingress |
| **격리** | 없음 (프로세스 수준) | 컨테이너 수준 | Pod + Namespace |
| **학습 난이도** | 낮음 | 중간 | 높음 |
| **운영 복잡도** | 서버 수 비례 증가 | 중간 | 초기 높음, 이후 안정 |

## 배포 방식 비교

### BareMetal
```bash
# 1. 패키지 설치
apt install python3 python3-pip

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 실행
gunicorn --bind 0.0.0.0:5000 app:app
```

### Docker
```bash
# 1. 이미지 빌드 (환경 포함)
docker build -t my-app .

# 2. 실행
docker run -p 5000:5000 my-app
```

### Kubernetes
```bash
# 1. 이미지 빌드 (Docker와 동일)
docker build -t my-app .

# 2. 선언적 배포
kubectl apply -f manifests/
```

## 확장(Scaling) 비교

### BareMetal
```
서버 1대 추가 → OS 설치 → Python 설치 → 앱 배포 → 로드밸런서 설정
⏱️ 수시간 ~ 수일
```

### Docker
```bash
docker run -d my-app    # 하나 더 실행
docker run -d my-app    # 또 하나
# 수동으로 로드밸런서 설정 필요
⏱️ 수초 ~ 수분
```

### Kubernetes
```bash
kubectl scale deployment my-app --replicas=10
# 로드밸런싱 자동!
⏱️ 수초
```

HPA(Horizontal Pod Autoscaler)를 사용하면 트래픽에 따라 자동 확장:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          averageUtilization: 70
```

## 장애 복구 비교

### BareMetal
```
앱 크래시 → systemd가 재시작 (같은 서버)
서버 다운 → 수동 복구 (다른 서버에 다시 배포)
```

### Docker
```
컨테이너 크래시 → restart policy로 재시작
호스트 다운 → 수동으로 다른 호스트에서 실행
```

### Kubernetes
```
Pod 크래시 → 즉시 새 Pod 자동 생성
Node 다운 → 다른 Node에 Pod 자동 재배치
```

## 언제 무엇을 쓸까?

### BareMetal이 적합한 경우
- 서버 1~2대의 소규모 프로젝트
- 최대 성능이 필요한 경우 (게임 서버, HPC)
- 특수 하드웨어 직접 접근이 필요한 경우

### Docker가 적합한 경우
- 개발 환경 통일
- CI/CD 파이프라인
- 소~중규모 서비스 (컨테이너 수십 개 이하)
- 마이크로서비스 개발/테스트

### Kubernetes가 적합한 경우
- 대규모 서비스 (컨테이너 수백 개 이상)
- 자동 확장이 필요한 서비스
- 무중단 배포가 필수인 서비스
- 멀티 클라우드 / 하이브리드 클라우드

## 진화 흐름

```
BareMetal → 가상머신(VM) → 컨테이너(Docker) → 오케스트레이션(K8s) → 서버리스
    │              │              │                  │               │
    │              │              │                  │               └─ AWS Lambda,
    │              │              │                  │                  Cloud Run
    │              │              │                  └─ 자동 관리
    │              │              └─ 환경 패키징
    │              └─ 하드웨어 가상화
    └─ 물리 서버 직접 관리
```

각 단계는 이전 단계의 문제점을 해결하기 위해 등장했습니다.
새 기술이 등장해도 이전 기술이 사라지지는 않으며, 상황에 맞게 선택하는 것이 중요합니다.
