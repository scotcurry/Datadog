FROM python:3.9-slim-buster

# This section in needed for Source Code Linking (https://curryware.datadoghq.com/source-code/setup/apm).
# They get updated in the Jenkinsfile build script.
ARG DD_GIT_REPOSITORY_URL
ARG DD_GIT_COMMIT_SHA
ENV DD_GIT_REPOSITORY_URL=${DD_GIT_REPOSITORY_URL}
ENV DD_GIT_COMMIT_SHA=${DD_GIT_COMMIT_SHA}

# Uncomment these when building a local container, but comment them when building a container for deployment.
# ENV LISTEN_PORT=8080
EXPOSE 8088

WORKDIR /app
COPY ../requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY ../.. .

RUN useradd appuser && chown -R appuser /app
USER appuser
CMD exec ddtrace-run gunicorn -b :8088 --workers 1 --threads 8 --timeout 0 app:app