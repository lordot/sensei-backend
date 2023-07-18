FROM python:3.11-alpine

RUN mkdir /sensei

COPY requirements.txt /sensei

RUN pip3 install -r /sensei/requirements.txt --no-cache-dir

COPY ./ /sensei

WORKDIR /sensei

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
