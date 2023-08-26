FROM python:3.6.5

WORKDIR /code
COPY app/* /code/
RUN pip install -r requirements.txt --upgrade pip
CMD [ "gunicorn", "--worker-class", "eventlet", "--workers", "4", "--bind", "0.0.0.0:5000", "--reload", "main:app" ]