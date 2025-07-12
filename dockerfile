FROM python:3.12-alpine as builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    make \
    cmake

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.12-alpine

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Add local bin to PATH
ENV PATH=/root/.local/bin:$PATH

COPY src/ /app/src/

EXPOSE 8000

CMD ["python", "src/main.py"]