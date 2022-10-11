# start by pulling the python image
FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . ../app
ENTRYPOINT [ "python" ]
CMD ["app.py" ]