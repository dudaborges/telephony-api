FROM python:3.9.13-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir virtualenv
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
