FROM python:3.7

COPY requirements.txt ./

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

WORKDIR /home/

EXPOSE 8888

CMD jupyter lab --ip=0.0.0.0 --port=8888 --allow-root