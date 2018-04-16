FROM python:3.6.5

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /root/
RUN git clone https://github.com/CoffeeTaro/getTweet
RUN pip install -r /root/getTweet/requirements.txt

ENTRYPOINT ["python", "/root/getTweet/getTweet.py", "-o", "/root/getTweet/output"]
