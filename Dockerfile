FROM python:3.12 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /umut

RUN apt-get update && apt-get install -y \
    netcat-traditional \
    binutils \
    libproj-dev

COPY requirements.txt /umut/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /umut/requirements.txt

COPY . .

EXPOSE 8001

COPY . /umut

RUN chmod +x /umut/entrypoint.sh

CMD ["/umut/entrypoint.sh"]
