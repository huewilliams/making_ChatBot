# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

from bothub_client.bot import BaseBot
from bothub_client.messages import Message


class Bot(BaseBot):
    def handle_message(self, event, context):
        content = event.get('content')

        if content.startswith('/start'):
            self.send_welcome_message(event)
        elif content == '메뉴보기':
            self.send_menu(event)

    # 봇을 시작했을 때 기능을 알려주는 함수
    def send_welcome_message(self, event):
        message = Message(event).set_text('반갑습니다. GiveMeJuice 봇 입니다\n'\
                                          '메뉴을 보고 주문해 주세요')\
                                .add_quick_reply('메뉴보기')
        self.send_message(message)

    # 메뉴 리스트를 보여주는 함수
    def send_menu(self, event):
        # bothub studio 의 project property 의 menu 값을 가져온다
        menu = self.get_project_data()['menu']
        # menu 에서 key 값(name)만 받아와 names 에 저장
        names = [name for name in menu.keys()]
        message = Message(event).set_text('어떤 음료를 원하세요?')

        # 버튼으로 메뉴를 하나하나 보여줌
        for name in names:
            message.add_postback_button(name, '/show {}'.format(name))

        self.send_message(message)
