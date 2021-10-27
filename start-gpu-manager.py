import datetime
import time
from multiprocessing import Process

import docker
import requests
from docker.types import LogConfig


def i_am_alive(url: str, gpu_server_id: int):
    while True:
        try:
            health_check_url = url + '/api/workers/gpus/' + str(gpu_server_id) + '/status'
            worker_request = {'isOn': True, 'lastResponse': str(datetime.datetime.now().isoformat())}
            response = requests.put(health_check_url, json=worker_request)
            print(response)
            time.sleep(10)
        except requests.exceptions.RequestException as e:
            continue


def work(url: str, gpu_server_id: int):
    while True:
        try:
            job_url = url + '/api/workers/gpus/' + str(gpu_server_id) + '/job'
            response = requests.get(job_url)

            if response.status_code != 200:
                time.sleep(10)
                continue

            job = response.json()
            print("가져온 작업입니다" + str(job))
            print(f"가져온 작업의 url입니다{job['metaData']}")

            image_url = job['metaData']
            worker_job_request = {'jobStatus': 'RUNNING'}
            running_status_url = url + '/api/workers/jobs/' + str(job['id']) + '/status'
            print("이 주소로 요청을 보냅니다 - " + running_status_url)
            response = requests.put(running_status_url, json=worker_job_request)
            print("상태가 RUNNING 으로 변경되었습니다.")

            print("도커를 이미지를 빌드하는중입니다.")

            api_client = docker.APIClient(base_url='unix:///var/run/docker.sock')

            lc = LogConfig(type=LogConfig.types.JSON, config={
                "tag": str(job['id'])
            })
            hc = api_client.create_host_config(log_config=lc)

            api_client.pull(image_url)

            container = api_client.create_container(image_url, detach=True,
                                                    host_config=hc)
            print("도커이미지를 빌드했습니다.")
            api_client.start(container=container.get('Id'))
            print("Job 실행을 시작했습니다.")
            api_client.wait(container)
            print("Job 실행을 완료했습니다.")

            worker_job_request = {'jobStatus': 'COMPLETED'}
            complete_status_url = url + '/api/workers/jobs/' + str(job['id']) + '/status'
            print("이 주소로 완료 요청을 보냅니다 - " + running_status_url)
            response = requests.put(complete_status_url, json=worker_job_request)
            print("Job 상태 완료로 변경되었습니다.")
        except requests.exceptions.RequestException as e:
            print(f"Running Exception!{e}")
            worker_job_request = {'jobStatus': 'CANCLED'}
            complete_status_url = url + '/api/workers/jobs/' + str(job['id']) + '/status'


if __name__ == '__main__':
    # host_url = 'https://api.gpuismine.com' main
    host_url = 'https://dev-api.gpuismine.com'  # dev

    Process(target=i_am_alive, args=(host_url, 1)).start()
    Process(target=work, args=(host_url, 1)).start()

    Process(target=i_am_alive, args=(host_url, 2)).start()
    Process(target=work, args=(host_url, 2)).start()

    Process(target=i_am_alive, args=(host_url, 3)).start()
    Process(target=work, args=(host_url, 3)).start()
