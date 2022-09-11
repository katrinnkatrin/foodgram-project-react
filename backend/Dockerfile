FROM python:3.7

WORKDIR /code
COPY . /code
#RUN python3 -m pip install --upgrade pip && \
    #pip3 install -r requirements.txt --no-cache-dir &&
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
