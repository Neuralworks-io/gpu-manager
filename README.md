# GPU Manager Emulator

if __name__ == '__main__': 아래의 host_url을 변경할 수 있습니다.

현재는 GPU Server 1에만 연결됩니다.

다른 GPU Server에 연결하고 싶다면 Process를 늘리고 GPU Server ID를 인자로 넣어주면 됩니다.

GPU Server당 2개의 Process를 만들어야 합니다.
- i_am_alive를 실행하는 Process(health check)
- work를 실행하는 Process(Job 처리)

해당 레포로 푸쉬하면 서버에 자동으로 반영됩니다.

## GPU Manger 21-08-09 개편 사항
logs에 메타 데이터를 남기기 위해 Low-level API 도입하게 됨.(Log에 tag 데이터를 넣어주기 위함)
로그를 직접 보내주는 방식이 아닌 filebeat에서 이를 관리하도록 함. (docker container에서 발생한 log 데이터를 전달해주는 방식)

/etc/filebeat/filebeat.yml 에서 설정 확인 할 수 있습니다. (elk 레포지토리에서 확인 가능)
