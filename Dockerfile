FROM python:3.7.2-alpine3.9

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /app
COPY requirements.txt requirements.txt

# -- Install dependencies:
RUN  pip --no-cache-dir install -r requirements.txt

COPY ./getTweet.py /app/getTweet.py

CMD ["python", "getTweet.py", "-k", "/app/key.toml", "-s", "/app/screen_name.txt", "-o", "/app/output/"]
