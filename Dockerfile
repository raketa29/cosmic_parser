# syntax=docker/dockerfile:1

FROM python:3.9-alpine
WORKDIR /usr/main
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "./main.py"]
