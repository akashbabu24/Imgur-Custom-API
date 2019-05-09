FROM ubuntu:bionic
MAINTAINER Akash Babu "akashbabu24@yahoo.co.in"
RUN apt-get update -y
RUN apt-get install -y python python-pip build-essential curl wget libfontconfig
#RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
 #   apt-get purge firefox && \
  #  wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
   # tar xjf $FIREFOX_SETUP -C /opt/ && \
    #ln -s /opt/firefox/firefox /usr/bin/firefox && \
    #rm $FIREFOX_SETUP
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    tar -jxf phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs && \
    rm phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN apt-get install xvfb -y
RUN pip install flask requests selenium queuelib pyvirtualdisplay
RUN Xvfb :10 -ac &
ENV DISPLAY=:10
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1
COPY . /app
WORKDIR /app
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.24.0-linux64.tar.gz -O > /usr/bin/geckodriver
RUN chmod +x /usr/bin/geckodriver
ENTRYPOINT ["python"]
CMD ["upload.py"]
EXPOSE 8080/tcp
