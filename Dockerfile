FROM python:3.12.14-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY src/ src/
COPY configs/ configs/
COPY data/sample/ data/sample/
CMD ["python", "src/benchmark.py", "--config", "configs/config.json"]
