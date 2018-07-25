# making_ChatBot
by Telegram and Facebook Messenger, language : python
  
## 챗봇 무료 호스팅 서버  
BotHub.Studio : https://bothub.studio/?utm_source=wooridle.net&utm_medium=display&utm_campaign=chatbot-lecture-ysctm201706  
로컬 컴퓨터에서 쉘 창을 열어 CLI 도구를 설치
<pre> pip install bothub-cli </pre>
계정을 연결합니다.
<pre> bothub configure </pre>
새로운 프로젝트를 생성합니다.
<pre> bothub init </pre>
그러면 아래와 같이 기본 코드가 생성됩니다.
<pre>.
|-- bothub
|   |-- bot.py
|   `-- __init__.py
|-- bothub.yml
|-- requirements.txt
`-- tests
</pre>
메신저를 연결합니다.
<pre> bothub channel add telegram --api-key=(my-api-key) </pre>
Bot을 서버에 구동합니다.
<pre> bothub deploy </pre>

## 봇 생성하기 - 텔레그램  
텔레그램의 검색창에서 `@BotFather` 를 찾습니다. `/newbot` 명령을 사용하여 새로운 봇을 생성합니다.
