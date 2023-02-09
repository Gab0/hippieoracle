FROM python:latest

RUN pip install --upgrade pip

RUN pip install django geopy requests pillow
RUN pip install pandas

COPY . /hippieoracle/

WORKDIR /hippieoracle

ENTRYPOINT ["python", "manage.py", "runserver", "--ipv6", "[::]:8000"]
