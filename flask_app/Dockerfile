FROM python:3.11.4-alpine3.18 AS builder

WORKDIR /flask_app

COPY . /flask_app

RUN pip install -r requirements.txt

EXPOSE 5000
# CMD ["sh", "-c", "gunicorn -w 4 --bind 0.0.0.0:5000 main_app:app > log.txt 2>&1"]

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "main_app:app"]