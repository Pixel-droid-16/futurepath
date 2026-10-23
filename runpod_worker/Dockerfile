
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

WORKDIR /app

# Install worker dependencies
COPY runpod_worker/requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the Serverless handler
COPY runpod_worker/handler.py ./handler.py

# Configure the inference model
ENV MODEL_ID=Qwen/Qwen2.5-3B-Instruct

# Start the RunPod Serverless worker
CMD ["python", "-u", "handler.py"]
