FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/

COPY ./webapp ./webapp
COPY ./README.md ./README.md
COPY ./requirements.txt ./requirements.txt
COPY ./data ./data

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "./webapp/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
