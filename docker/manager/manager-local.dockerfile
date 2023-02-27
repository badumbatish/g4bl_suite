FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN mkdir -p /usr/etc/config
COPY local-manager.yaml /usr/etc/config/manager.yaml
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./manager-main.py" ]