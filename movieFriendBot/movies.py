import json
import math
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime
from datetime import timedelta

# api_key 가 정의되지 않았다는 오류가 발생하여 하드코딩으로 직접 영화진흥원 API key 값을 넣어주었다.
api_key = '03adf941c6a1a842ab1828957797af65'

# REST API 를 이용하여 영화 박스 오피스 순위를 가져올 수 있습니다.


class BoxOffice(object):
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/' \
               'searchDailyBoxOfficeList.json'

    def __init__(self, api_key):
        self.api_key = api_key

    def get_movies(self):
        # learning-python 레포의 date,time module 디렉토리 참고하기
        # 현재의 날짜에 하루를 빼는 것
        target_dt = datetime.now() - timedelta(days=1)
        # 년도월일 형식으로 저장
        target_dt_str = target_dt.strftime('%Y%m%d')
        # url 형성
        query_url = '{}?key={}&targetDt={}'.format(self.base_url, self.api_key, target_dt_str)
        # URLLIB 모듈 - urlopen 함수 : 웹 문서 불러오기
        # 웹에서 얻은 데이터에 대한 객체를 돌려줌
        with urlopen(query_url) as fin:
            # json 모듈 - loads 함수
            # json 문자열을 파이썬 객체로 다시 변경해준다.
            return json.loads(fin.read().decode('utf-8'))

    def simplify(self, result):
        return [
            {
                'rank': entry.get('rank'),
                'name': entry.get('movieNm'),
                'code': entry.get('movieCd')
            }
            # 일별 박스오피스 API 응답구조
            # 응답필드  :   값   :   설명
            # rank      : 문자열 : 해당일자의 박스오피스 순위를 출력합니다.
            # movieNm   : 문자열 : 영화명(국문)을 출력합니다.
            # movieCd   : 문자열 : 영화의 대표코드를 출력합니다.
            for entry in result.get('boxOfficeResult').get('dailyBoxOfficeList')
        ]


box = BoxOffice(api_key)
# 영화 정보(객체)
movies = box.get_movies()
print(box.simplify(movies))