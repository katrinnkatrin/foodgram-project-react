FROM python:3.7

WORKDIR /code
COPY . /code
RUN python3 -m pip install --upgrade pip && \
    pip3 install -r /code/requirements.txt --no-cache-dir && \
    python3 /code/manage.py collectstatic --noinput
CMD python3 /code/manage.py migrate --noinput && \
    gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000