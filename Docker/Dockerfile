# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

# Uncomment these when building a local container, but comment them when building a container for deployment.
# ENV LISTEN_PORT=8080
EXPOSE 8088

WORKDIR /app
COPY ../requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY .. .

RUN useradd appuser && chown -R appuser /app
USER appuser
CMD exec gunicorn -b :8088 --workers 1 --threads 8 --timeout 0 app:app