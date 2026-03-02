FROM python:3.12-slim

WORKDIR /app

# 의존성 먼저 복사 → 캐시 활용
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY app/ .

# 환경변수 설정
ENV DEPLOY_ENV=docker

# 포트 노출
EXPOSE 5000

# gunicorn으로 실행
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
