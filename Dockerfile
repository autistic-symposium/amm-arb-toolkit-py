#Deriving the latest base image
FROM python:latest

WORKDIR /src

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir api
COPY api/* ./api/
COPY .env .
COPY setup.py .
COPY Makefile .

RUN make install

CMD [ "bdex", "-r", "5"]
