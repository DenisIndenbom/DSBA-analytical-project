FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/

COPY ./fastapi ./fastapi
COPY ./README.md ./README.md
COPY ./requirements.txt ./requirements.txt
COPY ./data ./data

RUN pip3 install -r requirements.txt

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/health

ENTRYPOINT ["fastapi", "run", "fastapi/api.py"]
