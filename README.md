# making_ChatBot
by Telegram and Facebook Messenger, language : python
  
## 참고  
* 사이트
  + Python으로 챗봇 만들어보기 : http://static.wooridle.net/lectures/chatbot/
  + [챗봇 만들기] 30분 만에 텔레그램 봇 만들기 : https://steemit.com/kr-dev/@maanya/30 
  + [챗봇 만들기 — 영화 상영관 찾기] : https://medium.com/bothub-studio-ko/%EC%B1%97%EB%B4%87-%EB%A7%8C%EB%93%A4%EA%B8%B0-%EC%98%81%ED%99%94-%EC%83%81%EC%98%81%EA%B4%80-%EC%B0%BE%EA%B8%B0-ec9bbff353d8
   
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
