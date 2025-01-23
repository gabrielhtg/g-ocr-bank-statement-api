FROM python:3.12
LABEL authors="gabriel"

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD python app.py