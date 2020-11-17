FROM python:3.8.6-buster

WORKDIR /app

COPY ["main.py", "requirements.txt", "./"]

ADD main.py /

# Essencial tools
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils\
    software-properties-common \
    unzip \
    curl

RUN apt-get install -y wget \
        build-essential \
        libgl1-mesa-glx \
        libgtk-3-dev \
        libdbus-glib-1-2

# Debian requires a manual installation for firefox
ARG FIREFOX_VERSION=81.0.1
RUN wget --no-verbose -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 \
   && rm -rf /opt/firefox \
   && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
   && rm /tmp/firefox.tar.bz2 \
   && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
   && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox
   #&& ln -fs /opt/geckodriver-$FIREFOX_VERSION /usr/bin/wires
 
# Gecko Driver
ARG GECKODRIVER_VERSION=v0.27.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
  && chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/geckodriver
  #&& ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/wires

# Install dependencies
RUN pip install -r requirements.txt

# Run
ENTRYPOINT ["python", "./main.py"]
