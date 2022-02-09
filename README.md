# BitcoinLong

기능:
1. 모든 코인 종목 중 수익성이 짙은 코인 하나를 선택하여 투자
2. 매매는 일 단위로 진행
3. 만약, 선택된 코인이 수익성은 짙으나 투자 알고리즘의 기준에 부합하지 않는 경우 해당 코인을 리스트에서 제거하고 차선책의 코인을 선정(ver1.1 update)
4. 투자항목이 변동성이 짙기 때문에 최대 이익률을 설정하고 이를 초과하면 바로 매도함.(ver1.2 update)

<Ubuntu 서버 명령어>
(*추가)한국 기준으로 서버 시간 설정: sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
현재 경로 상세 출력: ls -al
경로 이동: cd 경로
vim 에디터로 파일 열기: vim bitcoinAutoTrade.py
vim 에디터 입력: i
vim 에디터 저장: :wq!
패키지 목록 업데이트: sudo apt update
pip3 설치: sudo apt install python3-pip
pip3로 pyupbit 설치: pip3 install pyupbit
백그라운드 실행: nohup python3 bitcoinAutoTrade.py > output.log &
실행되고 있는지 확인: ps ax | grep .py
프로세스 종료(PID는 ps ax | grep .py를 했을때 확인 가능): kill -9 PID
