# start by pulling the python image
FROM bitnami/python:latest
WORKDIR /tmp
COPY app/requirements.txt requirements.txt
# RUN apk add g++ postgresql-dev cargo gcc python3-dev libffi-dev musl-dev zlib-dev jpeg-dev
RUN pip install -r requirements.txt
WORKDIR /
COPY ./app /app/app
WORKDIR /
CMD [ "python3", "app/app/app.py"]