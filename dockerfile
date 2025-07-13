FROM python:3.12-alpine as builder

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    make \
    cmake \
    wget \
    unzip

COPY requirements.txt /app/
RUN pip install --no-cache-dir --user -r requirements.txt

RUN mkdir -p /tmp/rules-download && \
    cd /tmp/rules-download && \
    wget -O capa-rules.zip "https://github.com/mandiant/capa-rules/archive/refs/heads/master.zip" && \
    unzip capa-rules.zip && \
    mv capa-rules-master /app/capa-rules && \
    cd /app && \
    rm -rf /tmp/rules-download

RUN mkdir -p /tmp/sigs-download && \
    cd /tmp/sigs-download && \
    wget -O capa-sigs.zip "https://github.com/mandiant/capa/releases/download/v9.2.1/capa-v9.2.1-linux.zip" && \
    unzip capa-sigs.zip && \
    mkdir -p /app/capa-sigs && \
    mv *.sig /app/capa-sigs/ 2>/dev/null || true && \
    cd /app && \
    rm -rf /tmp/sigs-download

FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    libgcc \
    libstdc++ \
    musl

RUN pip install --no-cache-dir flare-capa

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/capa-rules /app/capa-rules
COPY --from=builder /app/capa-sigs /app/capa-sigs

ENV PATH=/root/.local/bin:$PATH

COPY src/ /app/src/

EXPOSE 8000

CMD ["python", "src/main.py"]