FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt --verbose

CMD ["python", "./src/model_serving.py"]
