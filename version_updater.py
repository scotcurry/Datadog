import os
import re
import datetime
import subprocess


#  The current version uses the last digit of the year as the major version, day as the minor version, and minutes
#  into the day as the build version.
def get_current_version_string():

    current_time = datetime.datetime.now()
    year = str(current_time.year)[3]
    month = str(current_time.month)
    day = str(current_time.day)
    if len(day) == 1:
        day = '0' + day
    midnight_time = datetime.datetime(current_time.year, current_time.month, current_time.day)
    time_delta = current_time - midnight_time
    minutes = str(int(time_delta.seconds / 60))
    version = year + '.' + month + day + '.' + minutes
    last_updated = month + '/' + str(current_time.day) + '/' + str(current_time.year) + ':' + minutes
    print('Version: ' + version)
    return version, last_updated


def update_build_run_container(current_version):

    last_git_commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode('utf-8')
    last_git_commit_hash = str.strip(last_git_commit_hash)

    current_directory = os.getcwd()
    run_container_file = current_directory + '/Containers/build_run_container.sh'
    with open(run_container_file, 'r') as file:
        file_content = file.read()
    file.close()

    regex_string = 'datadogcurryware:\d{1}\.\d{1,3}\.\d{1,4}\s--'
    replacement_string = 'datadogcurryware:' + current_version + ' --'
    new_text = re.sub(regex_string, replacement_string, file_content)

    # regex_string = 'org\.opencontainers\.image\.revision=[a-f0-9]{40}'
    # replacement_string = 'org.opencontainers.image.revision=' + last_git_commit_hash
    # new_text = re.sub(regex_string, replacement_string, new_text)

    with open(run_container_file, 'w+') as replacement_file:
        replacement_file.write(new_text)
    replacement_file.close()


def update_docker_compose_file(current_version):

    current_directory = os.getcwd()
    docker_compose_file = current_directory + '/Containers/docker-compose.yaml'
    with open(docker_compose_file, 'r') as file:
        file_content = file.read()

    regex_string = 'DD_VERSION=\d{1}.\d{1,3}.\d{1,4}\r'
    replacement_string = 'DD_VERSION=' + current_version + '\r'
    new_text = re.sub(regex_string, replacement_string, file_content)

    regex_string = 'com.datadoghq.tags.build:\s\'\d{1}\.\d{1,3}\.\d{1,4}\''
    replacement_string = 'com.datadoghq.tags.build: \'' + current_version + '\''
    new_text = re.sub(regex_string, replacement_string, new_text)

    regex_string = 'com.datadoghq.tags.version:\s\'\d{1}\.\d{1,3}\.\d{1,4}\''
    replacement_string = 'com.datadoghq.tags.version: \'' + current_version + '\''
    new_text = re.sub(regex_string, replacement_string, new_text)

    with open(docker_compose_file, 'w+') as replacement_file:
        replacement_file.write(new_text)


# This also updates the gke-deployment file.
def update_deployment_file(current_version):

    current_directory = os.getcwd()
    deployment_file = ''
    for counter in range(2):
        if counter == 0:
            deployment_file = current_directory + '/Containers/datadogcurryware-deployment.yaml'
        if counter == 1:
            deployment_file = current_directory + '/Containers/gke-config/gke-deployment.yaml'

        with open(deployment_file, 'r') as file:
            file_content = file.read()

        regex_string = 'tags.datadoghq.com/version:\s"\d{1}\.\d{1,2}\.\d{1,4}"'
        replacement_string = 'tags.datadoghq.com/version: "' + current_version + '"'
        new_text = re.sub(regex_string, replacement_string, file_content)

        with open(deployment_file, 'w+') as replacement_file:
            replacement_file.write(new_text)


def update_build_action_file(current_version):

    current_directory = os.getcwd()
    workflow_file = current_directory + '/.github/workflows/build-action.yml'
    with open(workflow_file, 'r') as file:
        file_content = file.read()

    regex_string = '}}/datadogcurryware:\d{1}\.\d{1,3}\.\d{1,4},'
    replacement_string = '}}/datadogcurryware:' + current_version + ','
    new_text = re.sub(regex_string, replacement_string, file_content)

    with open(workflow_file, 'w+') as replacement_file:
        replacement_file.write(new_text)

def main():

    current_version, last_updated = get_current_version_string()
    update_build_run_container(current_version)
    update_docker_compose_file(current_version)
    update_deployment_file(current_version)
    update_build_action_file(current_version)

if __name__ == "__main__":
    main()