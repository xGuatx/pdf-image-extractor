FROM python:latest 
WORKDIR /app 
RUN apt update && apt install poppler-utils -y 
COPY . /app  
RUN pip install -r /app/requirements.txt


