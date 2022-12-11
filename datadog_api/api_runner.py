import os

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi


dd_api_key = os.environ['DD_API_KEY']
dd_app_key = os.environ['DD_APP_KEY']
configuration = Configuration()
with ApiClient(configuration) as api_client:
    # api_instance = AuthenticationApi(api_client)
    api_instance = MetricsApi(api_client)
    response = api_instance.list_metrics(
        q="q",
    )

    print(response)
