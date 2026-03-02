# 용어 사전 (Glossary)

인프라 학습에서 자주 등장하는 용어들을 한글로 정리했습니다.

---

### BareMetal (베어메탈)
가상화 없이 물리 서버에 직접 OS와 애플리케이션을 설치하여 운영하는 방식.

### Container (컨테이너)
애플리케이션과 실행에 필요한 모든 것(코드, 런타임, 라이브러리)을 하나로 패키징한 격리된 실행 환경. VM보다 가볍고 빠르다.

### ConfigMap (컨피그맵)
Kubernetes에서 설정 데이터를 키-값 쌍으로 저장하는 오브젝트. 환경변수나 설정 파일을 Pod에 주입할 때 사용.

### Cluster (클러스터)
Kubernetes를 실행하는 노드(서버)들의 집합. Control Plane과 Worker Node로 구성.

### Control Plane (컨트롤 플레인)
Kubernetes 클러스터의 두뇌. API Server, Scheduler, Controller Manager 등으로 구성되어 클러스터의 상태를 관리.

### Daemon (데몬)
백그라운드에서 지속적으로 실행되는 프로세스. 웹 서버, 데이터베이스 서버 등이 데몬으로 동작.

### Deployment (디플로이먼트)
Kubernetes에서 Pod의 원하는 상태(desired state)를 선언하는 오브젝트. 복제본 수, 업데이트 전략 등을 정의.

### Docker
컨테이너를 빌드하고 실행하는 플랫폼. Dockerfile로 이미지를 만들고, 이미지로 컨테이너를 실행.

### Docker Compose
여러 컨테이너로 구성된 애플리케이션을 정의하고 실행하는 도구. `docker-compose.yml` 파일로 서비스를 정의.

### Docker Hub
Docker 이미지를 저장하고 공유하는 공개 레지스트리. `python:3.12-slim` 같은 공식 이미지를 제공.

### Dockerfile
Docker 이미지를 만드는 설계도. `FROM`, `COPY`, `RUN`, `CMD` 등의 명령어로 이미지 빌드 과정을 정의.

### gunicorn (그린유니콘)
Python WSGI HTTP 서버. Flask, Django 같은 Python 웹 앱을 프로덕션에서 실행할 때 사용. 여러 워커 프로세스로 요청을 처리.

### Health Check (헬스 체크)
애플리케이션의 정상 동작 여부를 확인하는 메커니즘. Kubernetes에서는 liveness/readiness probe로 구현.

### HPA (Horizontal Pod Autoscaler)
Kubernetes에서 CPU, 메모리 등의 메트릭을 기반으로 Pod 수를 자동으로 조절하는 기능.

### Image (이미지)
컨테이너의 실행 템플릿. 읽기 전용이며, 이미지를 실행하면 컨테이너가 된다. 여러 레이어로 구성.

### Ingress (인그레스)
Kubernetes에서 외부 HTTP/HTTPS 트래픽을 클러스터 내부 Service로 라우팅하는 규칙. 도메인 기반 라우팅과 SSL 종료를 담당.

### kubectl (큐브씨티엘)
Kubernetes 클러스터를 관리하는 CLI 도구. 리소스 생성, 조회, 삭제 등 모든 관리 작업을 수행.

### Layer (레이어)
Docker 이미지의 구성 단위. Dockerfile의 각 명령어가 하나의 레이어를 생성. 변경되지 않은 레이어는 캐시에서 재사용.

### Liveness Probe (라이브니스 프로브)
Kubernetes에서 컨테이너가 살아있는지 확인하는 검사. 실패하면 컨테이너를 재시작.

### Manifest (매니페스트)
Kubernetes 리소스를 선언적으로 정의한 YAML 파일. `kubectl apply -f`로 클러스터에 적용.

### minikube (미니큐브)
로컬 환경에서 Kubernetes 클러스터를 실행하는 도구. 학습 및 개발용.

### Namespace (네임스페이스)
Kubernetes 클러스터 내의 가상 분리 공간. 환경(dev/prod)이나 팀별로 리소스를 격리.

### nginx (엔진엑스)
고성능 웹 서버이자 리버스 프록시. 정적 파일 서빙과 로드밸런싱에 주로 사용.

### Node (노드)
Kubernetes 클러스터의 워커 머신(물리 또는 가상). Pod가 실행되는 곳.

### Pod (파드)
Kubernetes의 최소 배포 단위. 하나 이상의 컨테이너를 포함하며, 같은 Pod 내 컨테이너는 네트워크와 스토리지를 공유.

### Port Forwarding (포트 포워딩)
네트워크의 한 포트로 들어온 트래픽을 다른 포트로 전달하는 것. `kubectl port-forward`로 로컬에서 Pod에 접근할 때 사용.

### Readiness Probe (레디니스 프로브)
Kubernetes에서 컨테이너가 트래픽을 받을 준비가 됐는지 확인하는 검사. 실패하면 Service에서 제외.

### Registry (레지스트리)
Docker 이미지를 저장하는 저장소. Docker Hub(공개), AWS ECR, GCR(비공개) 등이 있다.

### Replica (레플리카)
동일한 Pod의 복제본. `replicas: 3`이면 같은 Pod가 3개 실행됨. 고가용성과 부하 분산을 위해 사용.

### Reverse Proxy (리버스 프록시)
클라이언트와 백엔드 서버 사이에서 요청을 중계하는 서버. nginx가 대표적. SSL 종료, 로드밸런싱, 캐싱 등을 담당.

### Rolling Update (롤링 업데이트)
새 버전의 Pod를 하나씩 생성하고 이전 버전을 하나씩 제거하여 무중단으로 배포하는 전략.

### Secret (시크릿)
Kubernetes에서 민감한 데이터(비밀번호, API 키, 인증서)를 저장하는 오브젝트. ConfigMap과 비슷하지만 base64로 인코딩되어 저장.

### Self-Healing (셀프 힐링)
Kubernetes가 장애를 자동으로 감지하고 복구하는 기능. Pod가 죽으면 자동으로 새 Pod를 생성.

### Service (서비스)
Kubernetes에서 Pod 집합에 대한 네트워크 엔드포인트를 제공하는 오브젝트. Pod의 IP는 바뀌지만, Service의 IP는 고정.

### systemd (시스템디)
Linux의 시스템 및 서비스 관리자. 부팅 시 서비스 자동 시작, 크래시 시 재시작 등을 담당.

### Volume (볼륨)
컨테이너에 연결되는 저장 공간. 컨테이너가 삭제되어도 데이터를 유지할 수 있다. Docker 볼륨, Kubernetes PV/PVC 등이 있다.

### WSGI (위스키)
Web Server Gateway Interface. Python 웹 앱과 웹 서버 사이의 표준 인터페이스. gunicorn이 WSGI 서버의 대표적인 예.

### YAML (야믈)
"YAML Ain't Markup Language"의 약자. 사람이 읽기 쉬운 데이터 직렬화 형식. Kubernetes, Docker Compose 등의 설정 파일에서 사용.
