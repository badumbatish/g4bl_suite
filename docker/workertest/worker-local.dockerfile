FROM python:3

WORKDIR /usr/src/app

RUN mkdir -p /usr/etc/config
COPY local-worker.yaml /usr/etc/config/worker.yaml
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./testworkermain.py" ]