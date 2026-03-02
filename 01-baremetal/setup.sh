#!/bin/bash
# BareMetal 배포 자동화 스크립트
# 사용법: sudo ./setup.sh

set -e

APP_DIR="/opt/infra-tutorial"
SERVICE_NAME="app"

echo "========================================="
echo "  BareMetal 배포 스크립트"
echo "========================================="

# 1. 시스템 패키지 설치
echo "[1/5] 시스템 패키지 설치..."
apt update -qq
apt install -y python3 python3-pip python3-venv

# 2. 가상환경 생성 + 의존성 설치
echo "[2/5] Python 가상환경 설정..."
cd "$APP_DIR"
python3 -m venv .venv
source .venv/bin/activate
pip install -q -r app/requirements.txt

# 3. 환경변수 설정
echo "[3/5] 환경변수 설정..."
export DEPLOY_ENV=baremetal

# 4. systemd 서비스 등록
echo "[4/5] systemd 서비스 등록..."
cp "$APP_DIR/01-baremetal/app.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"

# 5. 확인
echo "[5/5] 서비스 상태 확인..."
systemctl status "$SERVICE_NAME" --no-pager

echo ""
echo "========================================="
echo "  배포 완료!"
echo "  http://localhost:5000 에서 확인하세요"
echo "========================================="
