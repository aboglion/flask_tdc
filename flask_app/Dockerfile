FROM python:3.11.4-alpine3.18 AS builder

WORKDIR /flask_app

COPY . /flask_app


RUN pip install -r requirements.txt
# Flask==2.3.3
# gunicorn==21.2.0
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "main_app:app"]


