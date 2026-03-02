# 03. Kubernetes 배포

## Kubernetes란?

Kubernetes(K8s)는 **컨테이너 오케스트레이션** 플랫폼입니다.

> 오케스트라 지휘자가 수십 명의 연주자를 조율하듯,
> Kubernetes는 수백 개의 컨테이너를 자동으로 관리합니다.

```
┌──────────────────────────────────────────────────────┐
│                   Kubernetes Cluster                  │
│                                                      │
│  ┌─────────────────────────────────────────────────┐ │
│  │                 Control Plane                    │ │
│  │  ┌──────────┐ ┌──────────┐ ┌─────────────────┐  │ │
│  │  │API Server│ │Scheduler │ │Controller Manager│  │ │
│  │  └──────────┘ └──────────┘ └─────────────────┘  │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │   Node 1     │  │   Node 2     │                 │
│  │ ┌──────────┐ │  │ ┌──────────┐ │                 │
│  │ │  Pod A   │ │  │ │  Pod C   │ │                 │
│  │ │┌────────┐│ │  │ │┌────────┐│ │                 │
│  │ ││Container││ │  │ ││Container││ │                 │
│  │ │└────────┘│ │  │ │└────────┘│ │                 │
│  │ └──────────┘ │  │ └──────────┘ │                 │
│  │ ┌──────────┐ │  │ ┌──────────┐ │                 │
│  │ │  Pod B   │ │  │ │  Pod D   │ │                 │
│  │ └──────────┘ │  │ └──────────┘ │                 │
│  └──────────────┘  └──────────────┘                 │
└──────────────────────────────────────────────────────┘
```

## Docker와 비교

| 항목 | Docker | Kubernetes |
|------|--------|------------|
| 역할 | 컨테이너 **실행** | 컨테이너 **관리/조율** |
| 확장 | 수동 (`docker run` 반복) | 자동 (`replicas: 10`) |
| 복구 | `restart: always` | Self-healing (자동 감지 + 재생성) |
| 네트워킹 | 수동 포트 매핑 | Service로 자동 라우팅 |
| 배포 | 중단 후 재시작 | 롤링 업데이트 (무중단) |
| 설정 관리 | ENV, 파일 마운트 | ConfigMap, Secret |

**Docker는 컨테이너를 "만드는" 도구, Kubernetes는 컨테이너를 "운영하는" 플랫폼**입니다.

## 핵심 개념

### Pod
Kubernetes의 **최소 배포 단위**. 하나 이상의 컨테이너를 감싸는 래퍼입니다.

```
┌──── Pod ────┐
│ ┌─────────┐ │
│ │Container│ │  ← 보통 1 Pod = 1 Container
│ └─────────┘ │
└─────────────┘
```

### Deployment
Pod의 **원하는 상태**(desired state)를 선언합니다. "이 앱을 3개 복제본으로 항상 유지해줘"

```yaml
replicas: 3  →  K8s가 항상 3개 Pod를 유지
                Pod가 죽으면 자동으로 새로 생성
```

### Service
Pod들에게 **고정 주소**를 부여합니다. Pod는 수시로 생성/삭제되지만, Service는 변하지 않습니다.

```
Client → Service (고정 IP) → Pod A
                            → Pod B  (로드밸런싱)
                            → Pod C
```

### Ingress
외부 트래픽을 클러스터 내부 Service로 **라우팅**하는 규칙입니다.

```
인터넷 → Ingress (도메인 기반 라우팅) → Service → Pod
```

### Namespace
클러스터 내의 **가상 분리 공간**. 환경(dev/staging/prod)이나 팀별로 리소스를 격리합니다.

### ConfigMap
애플리케이션 **설정을 코드와 분리**하여 관리합니다. 환경변수나 설정 파일을 주입할 수 있습니다.

## Manifest 파일 해설

### namespace.yaml
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: infra-tutorial    # 우리 앱 전용 네임스페이스
```

### configmap.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DEPLOY_ENV: "kubernetes"    # 환경변수로 주입됨
```

### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3                 # Pod 3개 유지
  template:
    spec:
      containers:
      - name: app
        image: infra-tutorial:latest
        ports:
        - containerPort: 5000
        envFrom:
        - configMapRef:
            name: app-config  # ConfigMap에서 환경변수 가져옴
```

### service.yaml
```yaml
apiVersion: v1
kind: Service
spec:
  type: ClusterIP             # 클러스터 내부에서만 접근
  ports:
  - port: 80                  # Service 포트
    targetPort: 5000          # Pod의 포트
  selector:
    app: infra-tutorial       # 이 레이블을 가진 Pod에게 트래픽 전달
```

### ingress.yaml
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
spec:
  rules:
  - host: app.local           # 이 도메인으로 들어온 요청을
    http:
      paths:
      - path: /
        backend:
          service:
            name: app-service  # 이 Service로 전달
```

## Step-by-step 배포

### 사전 준비

로컬 개발 환경에서는 [minikube](https://minikube.sigs.k8s.io/)를 사용합니다.

```bash
# minikube 설치 (macOS)
brew install minikube

# 클러스터 시작
minikube start

# kubectl 확인
kubectl version
```

### 1단계: 이미지 빌드

```bash
# minikube의 Docker daemon 사용
eval $(minikube docker-env)

# 이미지 빌드
docker build -t infra-tutorial:latest -f 02-docker/Dockerfile .
```

### 2단계: 리소스 생성

```bash
# Namespace 생성
kubectl apply -f 03-kubernetes/manifests/namespace.yaml

# 나머지 리소스 생성 (순서대로)
kubectl apply -f 03-kubernetes/manifests/configmap.yaml
kubectl apply -f 03-kubernetes/manifests/deployment.yaml
kubectl apply -f 03-kubernetes/manifests/service.yaml
kubectl apply -f 03-kubernetes/manifests/ingress.yaml
```

또는 한 번에:
```bash
kubectl apply -f 03-kubernetes/manifests/
```

### 3단계: 상태 확인

```bash
# Pod 확인
kubectl get pods -n infra-tutorial

# 출력 예시:
# NAME                              READY   STATUS    RESTARTS   AGE
# infra-tutorial-6d4f7b8c9-abc12   1/1     Running   0          30s
# infra-tutorial-6d4f7b8c9-def34   1/1     Running   0          30s
# infra-tutorial-6d4f7b8c9-ghi56   1/1     Running   0          30s

# Service 확인
kubectl get svc -n infra-tutorial

# 전체 리소스 확인
kubectl get all -n infra-tutorial
```

### 4단계: 접속 테스트

```bash
# minikube에서 Service 접속
minikube service app-service -n infra-tutorial

# 또는 포트 포워딩
kubectl port-forward svc/app-service 8080:80 -n infra-tutorial
# → http://localhost:8080
```

### 5단계: 스케일링

```bash
# Pod를 5개로 확장
kubectl scale deployment infra-tutorial -n infra-tutorial --replicas=5

# 확인
kubectl get pods -n infra-tutorial
# → 5개의 Pod가 Running 상태

# 다시 2개로 축소
kubectl scale deployment infra-tutorial -n infra-tutorial --replicas=2
```

### 6단계: 롤링 업데이트

코드를 수정하고 새 이미지를 빌드한 후:

```bash
# 새 이미지로 업데이트 (무중단)
kubectl set image deployment/infra-tutorial \
  app=infra-tutorial:v2 \
  -n infra-tutorial

# 업데이트 진행 상태 확인
kubectl rollout status deployment/infra-tutorial -n infra-tutorial

# 문제 발생 시 롤백
kubectl rollout undo deployment/infra-tutorial -n infra-tutorial
```

## Self-Healing 확인

```bash
# Pod 하나를 강제 삭제
kubectl delete pod <pod-name> -n infra-tutorial

# 바로 확인 → 새 Pod가 자동 생성됨!
kubectl get pods -n infra-tutorial
```

Kubernetes는 Deployment에 선언된 `replicas` 수를 항상 유지합니다. Pod가 죽으면 자동으로 새로 만듭니다.

## 정리

```bash
# 모든 리소스 삭제
kubectl delete namespace infra-tutorial

# minikube 중지
minikube stop
```

## 학습을 마치며

3가지 환경에서 동일한 앱을 배포해봤습니다:

| | BareMetal | Docker | Kubernetes |
|---|-----------|--------|------------|
| 배포 | 수동 설치 | 이미지 빌드 | manifest apply |
| 확장 | 서버 추가 | 컨테이너 추가 | `replicas: N` |
| 복구 | systemd | restart policy | self-healing |
| 업데이트 | 서비스 중단 | 컨테이너 교체 | 롤링 업데이트 |

→ 더 자세한 비교는 [docs/comparison.md](../docs/comparison.md) 를 참고하세요.
