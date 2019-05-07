FROM ubuntu:latest
MAINTAINER Akash Babu "akashbabu24@yahoo.co.in"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential 
RUN pip install flask
WORKDIR .
ENTRYPOINT ["python"]
CMD ["upload.py"]
