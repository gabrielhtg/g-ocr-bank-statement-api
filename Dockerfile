FROM python:3.12
LABEL authors="gabriel"

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt
RUN apt update -y
RUN apt install -y libgl1-mesa-dev libglib2.0-0

EXPOSE 5000

CMD ["python", "app.py"]