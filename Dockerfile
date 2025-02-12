FROM python:3.12-alpine

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . /usr/src/app

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

CMD ["gunicorn", "--bind", 0.0.0.0.8000, "speech_to_text.wsgi:application"]