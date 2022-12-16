import os

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.api.logs_archives_api import LogsArchivesApi
from datadog_api_client.v1.api.logs_indexes_api import LogsIndexesApi


dd_api_key = os.environ['DD_API_KEY']
dd_app_key = os.environ['DD_APP_KEY']
configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MetricsApi(api_client)
    response = api_instance.list_metrics(
        q="q",
    )
    print('--- Available Metrics ---')
    print(response)

    logs_api_instance = LogsApi(api_client)
    log_items = logs_api_instance.list_logs_get_with_pagination(page_limit=2)
    for item in log_items:
        print(item)

    api_log_archive_instance = LogsArchivesApi(api_client)
    response = api_log_archive_instance.list_logs_archives()
    print('--- Archives are Storage Buckets that ARE NOT on Datadog Storage ---')
    print(response)

    log_indexes_api_instance = LogsIndexesApi(api_client)
    response = log_indexes_api_instance.list_log_indexes()
    print('--- Indexes are stored, the key concept here is exclusions ----')
    print(response)
