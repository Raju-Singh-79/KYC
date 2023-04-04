FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

ADD ./requirements.txt /app/requirements.txt

ADD . /code/
RUN pip install -r requirements.txt
RUN apt -y update && apt install  -y vim

CMD  ["python" , "manage.py" , "runserver" , "0.0.0.0:8000"]
