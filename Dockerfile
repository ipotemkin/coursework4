FROM python:3.10-slim

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

WORKDIR /code
COPY ./app ./app
COPY ./templates ./templates
#COPY ./data ./data
COPY run.py .
COPY README.md .
CMD gunicorn run:app -b 0.0.0.0:80

#RUN apt update && apt install -y python
