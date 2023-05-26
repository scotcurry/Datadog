if [[ $# -eq 0 ]]; then
    echo "-a for apply, -d for delete"
    exit 1
fi

if [[ $1 == '-a' ]]; then
  docker pull scotcurry4/datadogcurryware:latest
  kubectl apply -f datadogcurryware-deployment.yaml
  kubectl apply -f datadogcurryware-service.yaml
  minikube service datadogcurryware-service
fi

if [[ $1 == '-d' ]]; then
  kubectl delete -f datadogcurryware-deployment.yaml
  kubectl delete -f datadogcurryware-service.yaml
  docker rmi scotcurry4/datadogcurryware:latest
fi

#  helm install datadog -f values.yaml datadog/datadog