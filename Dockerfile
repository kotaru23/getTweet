FROM python:3.7.2

# -- Install Pipenv:
RUN apt-get update -y && apt-get upgrade -y

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

# -- Install dependencies:
RUN  pip install -r requirements.txt

COPY ./getTweet.py /app/getTweet.py
CMD python getTweet.py -k /app/key.toml -s /app/screen_name.txt -o /app/output/
