from multiprocessing import Process
import requests
import time
import datetime
import docker


def i_am_alive(url: str, gpu_server_id: int):
    health_check_url = url + '/api/workers/gpus/' + str(gpu_server_id) + '/status'
    worker_request = {'isOn': True, 'lastResponse': str(datetime.datetime.now().isoformat())}

    while True:
        response = requests.put(health_check_url, json=worker_request)
        time.sleep(300)


def work(url: str, gpu_server_id: int):
    while True:
        job_url = url + '/api/workers/gpus/' + str(gpu_server_id) + '/job'
        response = requests.get(job_url)

        if response.status_code != 200:
            time.sleep(10)
            continue

        job = response.json()
        print("가져온 작업입니다" + str(job))

        worker_job_request = {'jobStatus': 'RUNNING'}
        running_status_url = url + '/api/workers/jobs/' + str(job['id']) + '/status'
        print("이 주소로 요청을 보냅니다" + running_status_url)
        response = requests.put(running_status_url, json=worker_job_request)
        print("상태가 RUNNING 으로 변경되었습니다.")

        print("도커를 이미지를 빌드하는중입니다.")
        client = docker.from_env()
        image = client.images.pull("aprn7950/mnist_test_auto", tag="0.1")
        container = client.containers.run(image, detach=True, auto_remove=True)
        print("도커이미지를 빌드했습니다.")

        log_url = url + '/api/workers/jobs/' + str(job['id']) + '/log'

        for line in container.logs(stream=True):
            # 현재 로그 전달
            print(line.decode('utf-8'))
            log = {'content': line.decode('utf-8')}
            response = requests.post(log_url, json=log)
        else:
            worker_job_request = {'jobStatus': 'COMPLETED'}
            complete_status_url = url + '/api/workers/jobs/' + str(job['id']) + '/status'
            response = requests.put(complete_status_url, json=worker_job_request)


if __name__ == '__main__':
    host_url = 'https://gpuismine.kro.kr'

    Process(target=i_am_alive, args=(host_url, 1)).start()
    Process(target=work, args=(host_url, 1)).start()
