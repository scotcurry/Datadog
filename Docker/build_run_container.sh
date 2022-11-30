cd ..
docker build --tag datadog_container --file ./Docker/Dockerfile .
cd Docker
docker-compose up -d