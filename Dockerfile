# app/Dockerfile

FROM python:3.12.5

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN pip3 install -r requirements.txt

EXPOSE 8501