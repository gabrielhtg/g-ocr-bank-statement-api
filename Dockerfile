FROM python:3.12
LABEL authors="gabriel"

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt
RUN pip list

EXPOSE 5000

CMD ["python", "app.py"]