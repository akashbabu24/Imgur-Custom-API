FROM ubuntu:latest
MAINTAINER Akash Babu "akashbabu24@yahoo.co.in"
RUN apt-get update -y
RUN apt-get install -y python3-dev python3-pip build-essential firefox curl wget 
RUN python3 --version
RUN pip3 install flask requests selenium queuelib
COPY . /app
WORKDIR /app
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.24.0-linux64.tar.gz -O > /usr/bin/geckodriver
RUN chmod +x /usr/bin/geckodriver
ENTRYPOINT ["python3"]
CMD ["upload.py"]
EXPOSE 80/tcp
