FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-2023-05-01

RUN apt-get update && apt-get install -y libmediainfo-dev

WORKDIR /app

COPY . /app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ./start.sh --debug
