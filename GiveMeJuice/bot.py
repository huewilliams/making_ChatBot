# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

from bothub_client.bot import BaseBot
from bothub_client.messages import Message


class Bot(BaseBot):
    def handle_message(self, event, context):
        content = event.get('content')

        if not content:
            if event['new_joined']:
                self.send_chatroom_welcome_message(event)
            return

        if content.startswith('/start'):
            self.send_welcome_message(event)

        elif content == '메뉴보기':
            self.send_menu(event)

        elif content.startswith('/show'):
            _, name = content.split()
            self.send_show(name, event)

        elif content.startswith('/order_confirm'):
            _, name = content.split()
            self.send_order_confirm(name, event)

        elif content.startswith('/order'):
            _, name = content.split()
            self.send_order(name, event)


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

    # 선택한 메뉴의 가격을 보여주는 함수
    def send_show(self, name ,event):
        menu = self.get_project_data()['menu']
        selected_menu = menu[name]
        text = '{name}는 {description}\n 가격은 {price}원 입니다.'.format(name=name, **selected_menu)
        message = Message(event).set_text(text)\
                                .add_quick_reply('{} 주문 '.format(name), '/order {}'.format(name))\
                                .add_quick_reply('메뉴보기')
        self.send_message(message)

    # 주문할 지 여부를 물어보는 함수
    def send_order_confirm(self, name, event):
        message = Message(event).set_text('{}를 주문하시겠습니까?'.format(name))\
                                .add_quick_reply('예', '/order {}'.format(name))\
                                .add_quick_reply('취소', '메뉴보기')
        self.send_message(message)

    #
    def send_order(self, name, event, quantity=1):
        self.send_message('{}를 {}잔 주문했습니다. 음료가 준비되면 알려드리겠습니다.'.format(name, quantity))

        chat_id = self.get_project_data().get('chat_id')
        order_message = Message(event).set_text('{} {}잔 주문이 들어왔습니다.'.format(name, quantity))\
                                      .add_quick_reply('완료', '/done {} {}'.format(event['sender']['id'], name))
        self.send_message(order_message, chat_id=chat_id)

    def send_chatroom_welcome_message(self, event):
        self.remember_chatroom(event)
        message = Message(event).set_text('안녕하세요? GiveMeJuice 봇 입니다.\n'\
                                          '고객의 주문과 평가를 전해드립니다.')
        self.send_message(message)

    def remember_chatroom(self, event):
        chat_id = event.get('chat_id')
        data = self.get_project_data()
        data['chat_id'] = chat_id
        self.set_project_data(data)

