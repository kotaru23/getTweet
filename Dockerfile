FROM ubuntu:18.04

# -- Install Pipenv:
RUN apt update && apt install python3-pip -y && pip3 install pipenv

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app

# -- Adding Pipfiles
ONBUILD COPY Pipfile Pipfile
ONBUILD COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
ONBUILD RUN set -ex && pipenv install --deploy --system

COPY ./getTweet.py /app/getTweet.py
CMD python3 getTweet.py -k /app/key.toml -s /app/screen_name.txt -o /app/output/
