FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY handler.py .
ENV MODEL_ID=Qwen/Qwen2.5-3B-Instruct
CMD ["python","-u","handler.py"]
