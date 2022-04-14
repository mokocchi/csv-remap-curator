FROM python:3.9-bullseye

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN mkdir venv  
RUN chown 1000 venv

USER 1000

ENV VIRTUAL_ENV=venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --no-cache-dir -r requirements.txt

COPY --chown=1000 ./csv_remap_curator ./csv_remap_curator