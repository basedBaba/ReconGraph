FROM python:3.13.1-alpine

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/

EXPOSE 8000

CMD ["python", "src/main.py"]