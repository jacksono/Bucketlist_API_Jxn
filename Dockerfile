FROM python:3.6.5

WORKDIR /bucketlist

ADD . /bucketlist

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -f -y postgresql-client

EXPOSE 5000

ENTRYPOINT ["python", "start.py"]
