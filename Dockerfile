FROM python:2.7-alpine3.10

COPY . /fsck/

WORKDIR /fsck

RUN pip install bitstring && pip install randompy

CMD python main.py