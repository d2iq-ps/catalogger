# start by pulling the python image
FROM python:alpine3.16
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apk add g++ postgresql-dev cargo gcc python3-dev libffi-dev musl-dev zlib-dev jpeg-dev
RUN pip install -r requirements.txt
COPY . ../app
ENTRYPOINT [ "python" ]
CMD ["app.py" ]