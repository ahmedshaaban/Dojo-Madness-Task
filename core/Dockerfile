FROM python:2.7
# MAINTAINER Shannon Black <shannon@ilovezoona.com>

RUN mkdir /var/core
WORKDIR /var/core

ADD . .

RUN pip install -r requirements.pip

EXPOSE 8888
ENTRYPOINT ["/var/core/docker-entrypoint.sh"]
CMD ["python", "main.py"]
