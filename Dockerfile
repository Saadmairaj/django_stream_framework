FROM python:2.7

ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /stream

ADD . /stream

RUN apt update
RUN apt install -y python-pip
RUN pip install poetry==0.8.1
RUN poetry install

EXPOSE 8000
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]