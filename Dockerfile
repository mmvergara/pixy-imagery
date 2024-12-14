FROM python:3.9.20

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5100

CMD ["python", "app.py"]