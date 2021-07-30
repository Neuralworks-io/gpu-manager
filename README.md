# GPU Manager 에뮬레이터

if __name__ == '__main__': 아래의 host_url을 변경할 수 있습니다.

현재는 GPU Server 1에만 연결됩니다.

다른 GPU Server에 연결하고 싶다면 Process를 늘리고 GPU Server ID를 인자로 넣어주면 됩니다.

GPU Server당 2개의 Process를 만들어야 합니다.
- i_am_alive를 실행하는 Process(health check)
- work를 실행하는 Process(Job 처리)
