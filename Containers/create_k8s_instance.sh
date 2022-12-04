if [[ $# -eq 0 ]]; then
    echo "-a for apply, -d for delete"
    exit 1
fi

if [[ $1 == '-a' ]]; then
  kubectl apply -f datadogcurryware-deployment.yaml
  kubectl apply -f datadogcurryware-service.yaml
fi

if [[ $1 == '-d' ]]; then
  kubectl delete -f datadogcurryware-deployment.yaml
  kubectl delete -f datadogcurryware-service.yaml
fi
