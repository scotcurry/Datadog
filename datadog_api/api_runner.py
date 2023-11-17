import os

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.api.logs_archives_api import LogsArchivesApi
from datadog_api_client.v1.api.logs_indexes_api import LogsIndexesApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem
from datadog_api_client.v2.model.content_encoding import ContentEncoding


# dd_api_key = os.environ['DD_API_KEY']
# dd_app_key = os.environ['DD_APP_KEY']
configuration = Configuration()
# app_key_dict = {'apiKeyAuth': dd_api_key, 'appKeyAuth': dd_app_key}
# configuration.api_key = app_key_dict
with ApiClient(configuration) as api_client:

    # api_instance = MetricsApi(api_client)
    # response = api_instance.list_metrics(
    #     q="q",
    # )
    # print('--- Available Metrics ---')
    # print(response)
    #
    # logs_api_instance = LogsApi(api_client)
    # log_items = logs_api_instance.list_logs_get_with_pagination(page_limit=2)
    # for item in log_items:
    #     print(item)
    #
    # api_log_archive_instance = LogsArchivesApi(api_client)
    # response = api_log_archive_instance.list_logs_archives()
    # print('--- Archives are Storage Buckets that ARE NOT on Datadog Storage ---')
    # print(response)
    #
    # log_indexes_api_instance = LogsIndexesApi(api_client)
    # response = log_indexes_api_instance.list_log_indexes()
    # print('--- Indexes are stored, the key concept here is exclusions ----')
    # print(response)

    api_instance = LogsApi(api_client)

    log_file = open('/Users/scot.curry/Downloads/dd.log', 'r')
    log_line = log_file.readline()
    print(log_line)
    log_array = []

    for current_line in log_file:
        if not current_line:
            break

        line_fields = current_line.split('|')
        if len(line_fields) > 2:
            log_time = line_fields[0][0:19]
            status = line_fields[2].strip()
            host = 'att'
            service = 'kafka'
            message = 'status=' + status + ':' + line_fields[4].strip()
            tags = 'env:prod,status:' + status
            this_item = HTTPLogItem(ddsource='att', ddtags=tags, hostname='att', message=message,
                                    service='kafka')
            log_array.append(this_item)
            body = HTTPLog(
                # [
                #     HTTPLogItem(
                #         ddsource='att',
                #         ddtags='env:prod,project=att',
                #         hostname='att',
                #         message=message,
                #         service='kafka',
                #     ),
                # ]
                log_array
            )
            response = api_instance.submit_log(content_encoding=ContentEncoding.DEFLATE, body=body)
