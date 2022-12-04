cd ..
docker build --tag docker.io/scotcurry4/datadogcurryware:0.1.0 --file ./Docker/Dockerfile .
cd Docker
docker-compose up -d