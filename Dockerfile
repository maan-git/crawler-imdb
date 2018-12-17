FROM python:3.6.4

RUN mkdir /app
WORKDIR /app

RUN apt update && apt install -y poppler-utils

# INSTALL DEPENDENCIES
COPY . /app
RUN pip install -r requirements.txt

ENV my_env=value


CMD ["python", "main.py"]