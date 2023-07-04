cd ..

LATEST=false
CLEAR=false
BUILD=false
UPLOAD=false

for command_line in "$@"
do
  echo "$command_line"
  if [ "$command_line" = "-u" ] || [ "$command_line" = "--upload" ]; then
    echo 'Upload is true'
    UPLOAD=true
  fi
  if [ "$command_line" = "-l" ] || [ "$command_line" = "--latest" ]; then
    LATEST=true
  fi
  if [ "$command_line" = "-c" ] || [ "$command_line" = "--clear" ]; then
    CLEAR=true
  fi
  if [ "$command_line" = "-b" ] || [ "$command_line" = "--build" ]; then
    BUILD=true
  fi
  if [ "$command_line" = "-r" ] || [ "$command_line" = "--run" ]; then
    RUN=true
  fi
done

if [[ $# -eq 0 || ( ( $UPLOAD = false ) && ( $LATEST = false ) && ( $CLEAR = false ) && ( $BUILD = false ) ) ]]; then
  echo 'Parameters: [-c or --clear] [-l or --latest] [-b or --build] [u or --upload']
  echo ''
  echo '-c --clear - Removes all existing containers and images'
  echo '-l --latest - Pulls the latest Datadog agent'
  echo '-b --build - Builds new images'
  echo '-u --upload - Uploads images'
  echo '-r --run Runs the container'
  exit 0
fi

echo $LATEST
read -p "Stop here" -t 20
if [[ $LATEST = true ]]; then
  echo "Pulling latest Datadog Agent"
  docker rm --force datadog_agent
  docker rmi --force datadog/agent:latest
  docker pull datadog/agent:latest
fi

echo $CLEAR
if [[ $CLEAR = true ]]; then
  echo 'Removing Containers'
  docker rm --force datadogcurryware
  echo "Removing Images"
  docker rmi --force scotcurry4/datadogcurryware:latest
  docker rmi --force docker.io/scotcurry4/datadogcurryware:latest
  docker rmi --force us-central1-docker.pkg.dev/currywareff/currywareffrepository/datadogcurryware:latest
fi

echo $BUILD
if [[ $BUILD = true ]]; then
  docker build --tag docker.io/scotcurry4/datadogcurryware:3.704.1123 --file ./Containers/Dockerfile . \
    --label org.opencontainers.image.revision=99f154041cd79e214a5eb3d88700cdb38d14952e \
    --label org.opencontainers.image.source=github.com/scotcurry/Datadog
  docker build --tag scotcurry4/datadogcurryware:3.704.1123 --file ./Containers/Dockerfile . \
    --label org.opencontainers.image.revision=99f154041cd79e214a5eb3d88700cdb38d14952e \
    --label org.opencontainers.image.source=github.com/scotcurry/Datadog
  docker build --tag scotcurry4/datadogcurryware:latest --file ./Containers/Dockerfile . \
    --label org.opencontainers.image.revision=99f154041cd79e214a5eb3d88700cdb38d14952e \
    --label org.opencontainers.image.source=github.com/scotcurry/Datadog
  docker build --platform linux/amd64 --tag us-central1-docker.pkg.dev/currywareff/currywareffrepository/datadogcurryware:latest --file ./Containers/Dockerfile . \
    --label org.opencontainers.image.revision=99f154041cd79e214a5eb3d88700cdb38d14952e \
    --label org.opencontainers.image.source=github.com/scotcurry/Datadog
fi

if [[ $UPLOAD = true ]]; then
  echo 'Uploading Image'
  docker image push docker.io/scotcurry4/datadogcurryware:latest
  gcloud auth configure-docker us-central1-docker.pkg.dev
  cat /Users/scot.curry/PycharmProjects/CurrywareFF/currywareff-d971a11d21cd.json | docker login -u _json_key --password-stdin https://us-central1-docker.pkg.dev
  sudo docker push us-central1-docker.pkg.dev/currywareff/currywareffrepository/datadogcurryware:latest
fi

if [[ $RUN = true ]]; then
  echo "Starting Container"
  cd Containers || exit
  docker-compose up -d
fi