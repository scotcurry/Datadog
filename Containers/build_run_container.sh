if [[ $# == '-l' ]]; then
    echo "Pulling latest Datadog Agent"
    docker rm --force datadog_agent
    docker rmi --force datadog/agent:latest
    docker pull datadog/agent:latest
fi

cd ..

# Clean everything to start fresh every time.
echo 'Removing Containers'
docker rm --force datadogcurryware
echo "Removing Images"
docker rmi --force scotcurry4/datadogcurryware:0.2.2
docker rmi --force docker.io/scotcurry4/datadogcurryware:0.2.2

docker build --tag docker.io/scotcurry4/datadogcurryware:0.2.2 --file ./Containers/Dockerfile .
docker build --tag scotcurry4/datadogcurryware:0.2.2 --file ./Containers/Dockerfile .
docker build --tag scotcurry4/datadogcurryware:latest --file ./Containers/Dockerfile .

if [[ $1 == -u ]]; then
  docker image push docker.io/scotcurry4/datadogcurryware:0.2.2
fi

cd Containers
docker-compose up -d