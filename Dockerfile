FROM python:3.6

RUN apt-get update && apt-get -y install \
    python3-pip python3-dev libpq-dev

WORKDIR /phopo
ADD    ./requirements.txt   /phopo/
RUN    pip install -r requirements.txt

ADD    ./               /phopo/
#ADD    ./manage.py      /phopo/

CMD ["python", "manage.py", "runserver", "0:8000"]
