# Koyeb GPU Optimized Dockerfile
# Northeastern University Chatbot - A100 GPU Optimized for Koyeb
FROM nvidia/cuda:12.1-devel-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create symlinks for python
RUN ln -s /usr/bin/python3.11 /usr/bin/python && \
    ln -s /usr/bin/python3.11 /usr/bin/python3

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy requirements first for better caching
COPY requirements_gpu.txt .

# Install Python dependencies with GPU support
RUN pip install --no-cache-dir -r requirements_gpu.txt

# Copy application files
COPY koyeb_gpu_handler.py .
COPY koyeb_gpu_start.py .
COPY chroma_cloud_config.py .

# Set environment variables for GPU optimization
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV CUDA_VISIBLE_DEVICES=0
ENV TOKENIZERS_PARALLELISM=false
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Expose port (Koyeb will set PORT environment variable)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start the application
CMD ["python", "koyeb_gpu_start.py"]