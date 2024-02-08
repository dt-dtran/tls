# pull the official docker image
FROM python:3.11-slim
RUN python -m pip install --upgrade pip
# set work directory
WORKDIR /app

# set env variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
CMD uvicorn main:app --host 0.0.0.0 --port 5002
