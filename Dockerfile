FROM python:latest

WORKDIR /app

COPY . /app

RUN apt update
RUN chmod 777 build.sh
RUN ./build.sh

EXPOSE 5000

CMD ["python","run.py"]
