FROM python:3.10-slim

LABEL maintainer="buildwithzee"
LABEL description="Crop Recommendation Model Server — MLflow"
LABEL version="1.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

#install py dependencies
RUN pip install --no-cache-dir \
    mlflow==2.12.2 \
    scikit-learn==1.4.2 \
    pandas==2.2.2 \
    numpy==1.26.4 \
    gunicorn \
    dagshub

EXPOSE 5001
#model uri
CMD ["mlflow", "models", "serve", \
     "--model-uri", "model_output", \
     "--host", "0.0.0.0", \
     "--port", "5001", \
     "--no-conda"]
