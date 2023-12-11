terraform {
  required_providers {
    datadog = {
      source = "DataDog/datadog"
    }
  }
}

# These get passed on the command line by the Jenkins file
variable "datadog_api_key" {
  type = string
}

variable "datadog_app_key" {
  type = string
  nullable = false
}

# Configure the Datadog provider
provider "datadog" {
  api_key = var.datadog_api_key
  app_key = var.datadog_app_key
}

output "print_values" {
  value = "DD_API_KEY:${var.datadog_api_key}"

}

output "print_app_key" {
  value = "DD_APP_KEY:${var.datadog_app_key}"
}

resource "datadog_service_definition_yaml" "service_definition_v2_2" {
  service_definition = <<EOF
schema-version: v2.2
dd-service: chuckjoke-frontend
team: e-commerce-team
contacts:
  - name: Support Email
    type: email
    contact: scotcurry4@gmail.com
  - name: Support Slack
    type: slack
    contact: https://currywareinc.slack.com/archives/C04RNGL2FBL
description: dynamic instrumentation example
tier: high
lifecycle: production
application: chuckjoke-frontend
languages:
  - html
  - python
type: web
links:
  - name: dynamic instrumentation runbook
    type: runbook
    url: https://curryware.datadoghq.com/notebook/446054/curryware-notebook
  - name: dynamic instrumentation wiki
    type: doc
    provider: wiki
    url: https://curryware.atlassian.net/wiki/spaces/DA/overview
  - name: datadog source code
    type: repo
    provider: github
    url: https://github.com/scotcurry/Datadog
tags:
  - business-unit:sales
  - cost-center:curryware
EOF
}