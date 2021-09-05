FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /backend
ADD requirements.txt /backend/
RUN pip install -r requirements.txt
ADD . /backend/
CMD ["sh", "-c", "python manage.py collectstatic --no-input; python manage.py migrate; gunicorn core.wsgi -b 0.0.0.0:8000"]