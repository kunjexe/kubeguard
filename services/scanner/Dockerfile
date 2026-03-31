FROM gcr.io/distroless/python3

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --upgrade wheel==0.46.2 jaraco.context==6.1.0

COPY . .

CMD ["python", "app.py"]