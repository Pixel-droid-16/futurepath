FROM nvidia/cuda:12.8.0-cudnn-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    MODEL_ID=Qwen/Qwen2.5-3B-Instruct

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/venv

WORKDIR /app

# Install an explicit CUDA 12.8 PyTorch build for NVIDIA Blackwell (sm_120).
RUN python -m pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu128 torch==2.7.1

COPY runpod_worker/requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY runpod_worker/handler.py ./handler.py

CMD ["python", "-u", "handler.py"]
