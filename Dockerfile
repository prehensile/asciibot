FROM gliderlabs/alpine

MAINTAINER Henry Cooke <me@prehensile.co.uk>

# update system
RUN apk update && apk upgrade

# install python
RUN apk add python py-pip

# copy python requirements into container
ADD ./requirements.txt /requirements.txt

# install python requirements in container
RUN pip install -r requirements.txt

# copy app code into container
ADD ./app /app

# entry point
CMD "/app/main.py"
