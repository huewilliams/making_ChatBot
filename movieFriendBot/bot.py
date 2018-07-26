# -*- coding: utf-8 -*-
# 챗봇과 연동하기 - 영화 순위

from __future__ import (absolute_import, division, print_function, unicode_literals)

from bothub_client.bot import BaseBot
from bothub_client.messages import Message
# BoxOffice 박스오피스 순위를 받아오는 모듈 참조
from .movies import BoxOffice
# LotteCinema 영화관 정보를 받아오는 모듈 참조
from .movies import LotteCinema


class Bot(BaseBot):

    # 사용자들이 메신저를 통해 MovieFriendBot 에게 말을 걸면, handle_message (event, context) 메소드가 호출됨
    # event 변수에는 유저가 입력한 내용과 함께 다양한 부가 정보들이 들어있다.
    # 그 중 event['content'] 에는 사용자가 입력한 텍스트 메세지가 담겨있다.
    def handle_message(self, event, context):
        message = event.get('content')
        # 사용자의 위치 정보 (latitude : 위도, longitude : 경도)를 받아옴
        location = event.get('location')

        # location 이 존재할 경우 send_nearest_theaters 함수 실행
        if location:
            self.send_message('위치 정보 입력받았습니다.')
            # 2018-7-27 오류 해결 : 매개변수에 event 를 전달해야 함
            self.send_nearest_theaters(location['latitude'], location['longitude'], event)
            return

        # 사용자가 '영화순위' 입력시, send_box_office 함수 실행
        if message == '영화순위':
            self.send_box_office(event)

        # 사용자가 '근처 상영관 찾기' 입력시, send_search_theater_message 함수 실행
        elif message == '근처 상영관 찾기':
            self.send_search_theater_message(event)

    # 영화 순위를 메세지로 보내주는 함수
    def send_box_office(self, event):
        data = self.get_project_data()
        api_key = data.get('box_office_api_key')
        box_office = BoxOffice(api_key)
        movies = box_office.simplify(box_office.get_movies())
        rank_message = ','.join(['{}. {}'.format(m['rank'], m['name']) for m in movies])
        response = '요즘 볼만한 영화들의 순위입니다.\n{}'.format(rank_message)

        # send_message 의 인자로는 평범한 문자열이 올 수도 있지만,
        # 풍부한 메세지(rich message)를 보내기 위해서는 Message 객체를 사용할 수도 있습니다.
        # 이 경우에는 Message 객체를 사용하여 메세지에 빠른 응답(quick reply)을 포함시켰습니다.
        message = Message(event).set_text(response)\
                                .add_quick_reply('영화순위')\
                                .add_quick_reply('근처 상영관 찾기')
        # send_message(message) 메소드를 통해 사용자에게 메세지를 보낼 수 있습니다.
        self.send_message(message)

    # 위치입력 요청을 메세지로 보내주는 함수
    def send_search_theater_message(self, event):
        message = Message(event).set_text('현재 계신 위치를 알려주세요')\
                                .add_location_request('위치 전송하기')
        self.send_message(message)

    # 가장 가까운 상영관 3개를 메세지로 보내주는 함수
    def send_nearest_theaters(self, latitude, longitude, event):
        c = LotteCinema()
        # 영화관의 정보를 리스트로 만들어 저장
        theaters = c.get_theater_list()
        nearest_theaters = c.filter_nearest_theater(theaters, latitude, longitude)

        message = Message(event).set_text('가장 가까운 상영관들입니다' + \
                                          '상영시간표를 확인하세요')

        for theater in nearest_theaters:
            # 각각의 영화관의 상영영화 정보를 받아 data 에 저장
            data = '/schedule {} {}'.format(theater['TheaterID'], theater['TheaterName'])
            # 버튼을 추가 (3개의 영화관 정보를 선택 가능)
            message.add_postback_button(theater['TheaterName'], data)

        message.add_quick_reply('영화순위')
        self.send_message(message)