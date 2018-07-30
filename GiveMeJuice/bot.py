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

        # 챗봇 시작할 때
        if content.startswith('/start'):
            self.send_welcome_message(event)

        # 사용자가 메뉴보기 요청할 때
        elif content == '메뉴보기':
            self.send_menu(event)

        # 메뉴 선택했을 때 (메뉴 정보 보여주기)
        elif content.startswith('/show'):
            _, name = content.split()
            self.send_show(name, event)

        # 주문하기 여부
        elif content.startswith('/order_confirm'):
            _, name = content.split()
            self.send_order_confirm(name, event)

        elif content.startswith('/order'):
            _, name = content.split()
            self.send_order(name, event)

        # 직원이 주문 완료를 눌렀을 때
        elif content.startswith('/done'):
            self.send_drink_done(content, event)

        # 고객이 평가하기를 눌렀을 때
        elif content == '/feedback':
            self.send_feedback_request()

        else:
            data = self.get_user_data()
            wait_feedback = data.get('wait_feedback')
            if wait_feedback:
                self.send_feedback(content, event)

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

    # 사용자에게 주문 정보, 직원에게 주문 등록
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
        # 현재 사용자의 chat_id를 받아옴
        data = self.get_project_data()
        data['chat_id'] = chat_id
        self.set_project_data(data)
        # bothub studio 프로퍼티에 아이디 설정

    def send_drink_done(self, content, event):
        _, sender_id, menu_name = content.split()
        self.send_message("{}가 준비되었습니다. 카운터에서 수령해주세요.".format(menu_name), chat_id=sender_id)
        message = Message(event).set_text('저희 가게를 이용하신 후 평가를 해주세요')\
                                .add_quick_reply('평가하기','/feedback')
        self.send_message(message, chat_id=sender_id)
        # chat_id=sender_id : 요청을 보낸 사람의 id, 고객에게 대답 전송
        self.send_message('고객분께 음료 완료 알림을 전송했습니다.')

    def send_feedback_request(self):
        self.send_message('음료를 맛있게 즐기셧다면 평가를 해주세요')
        data = self.get_user_data()
        data['wait_feedback'] = True
        self.set_user_data(data)

    def send_feedback(self, content, event):
        chat_id = self.get_project_data().get('chat_id')
        self.send_message('고객의 평가 메세지입니다\n{}'.format(content), chat_id=chat_id)

        message = Message(event).set_text('평가해져서 감사합니다')\
                                .add_quick_reply('메뉴보기')
        self.send_message(message)
        data = self.get_user_data()
        data['wait_feedback'] = False
        self.set_user_data(data)

