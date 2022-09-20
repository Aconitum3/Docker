FROM python:3.7
RUN pip install mysqlclient flask gunicorn
COPY app.py ./
CMD gunicorn app:app --bind 0.0.0.0:80