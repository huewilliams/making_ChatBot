# -*- coding: utf-8 -*-
# 챗봇과 연동하기 - 영화 순위

from __future__ import (absolute_import, division, print_function, unicode_literals)

from bothub_client.bot import BaseBot
from bothub_client.messages import Message
from .movies import BoxOffice

class Bot(BaseBot):

    # 사용자들이 메신저를 통해 MovieFriendBot 에게 말을 걸면, handle_message (event, context) 메소드가 호출됨
    # event 변수에는 유저가 입력한 내용과 함께 다양한 부가 정보들이 들어있다.
    # 그 중 event['content'] 에는 사용자가 입력한 텍스트 메세지가 담겨있다.
    def handle_message(self, event, context):
        message = event.get('content')

        if message == '영화순위':
            self.send_box_office(event)

    def send_box_office(self,event):
        data = self.get_project_data()
        api_key = data.get('box_office_api_key')
        box_office = BoxOffice(api_key)
        movies = box_office.simplify(box_office.get_movies())
        rank_message = ','.join(['{}. {}'.format(m['rank'], m['name']) for m in movies])
        response = '요즘 볼만한 영화들의 순위입니다.\n{}'.format(rank_message)

        # send_message(message) 메소드를 통해 사용자에게 메세지를 보낼 수 있습니다.
        # send_message 의 인자로는 평범한 문자열이 올 수도 있지만,
        # 풍부한 메세지(rich message)를 보내기 위해서는 Message 객체를 사용할 수도 있습니다.
        # 이 경우에는 Message 객체를 사용하여 메세지에 빠른 응답(quick reply)을 포함시켰습니다.
        message = Message(event).set_text(response)\
                                .add_quick_reply('영화순위')\
                                .add_quick_reply('근처 상영관 찾기')
        self.send_message(message)
