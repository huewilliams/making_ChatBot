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
        # <learning-python 레포의 date,time module 디렉토리 참고하기>

        # 현재의 날짜에 하루를 빼는 것
        target_dt = datetime.now() - timedelta(days=1)
        # 년도월일 형식으로 저장
        target_dt_str = target_dt.strftime('%Y%m%d')
        # url 형성
        query_url = '{}?key={}&targetDt={}'.format(self.base_url, self.api_key, target_dt_str)
        # <learning-python 레포의 URLLIB module 디렉토리 참고하기>

        # URLLIB 모듈 - urlopen 함수 : 웹 문서 불러오기
        # 웹에서 얻은 데이터에 대한 객체를 돌려줌
        with urlopen(query_url) as fin:
            # <learning-python 레포의 json module 디렉토리 참고하기>

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

# 롯데 시네마는 공개된 OPEN API 가 없기 때문에 아래와 같이 정보를 가져온다.


class LotteCinema(object):
    # base_url =  'http://www.lottecinema.co.kr'
    base_url = 'http://moviefriend.cafe24.com'
    # 롯데시네마는 해외에서 접속하는 경우 응답을 거절하기 때문에, 예제 용도로 국내 프록시 서버를 사용합니다
    base_url_cinema_data = '{}/LCWS/Cinema/CinemaData.aspx'.format(base_url)
    # 영화관 정보를 cinema_data 에 저장
    base_url_movie_list = '{}/LCWS/Ticketing/TicketingData.aspx'.format(base_url)
    # 영화 리스트를 movie_list 에 저장

    # <learning-python 레포의 args and kwargs 디렉토리 참고하기>

    # **kwargs는 키워드된 가변 갯수의 인자들을 함수에 보낼 때 사용합니다 (key 와 value 로 이루어짐)
    def make_payload(self, **kwargs):
        param_list = {'channelType': 'MW', 'osType': '', 'osVersion': '', **kwargs}
        # key 와 value 로 이루어진 딕셔너리 생성
        data = {'ParamList': json.dumps(param_list)}
        # 유니 코드 문자열을 바이트 문자열로 나타내려면 인코딩이라고 합니다.
        payload = urlencode(data).encode('utf8')
        return payload

    def byte_to_json(self, fp):
        # 바이트 문자열을 유니 코드 문자열로 변환하는 것을 디코딩이라고 합니다.
        content = fp.read().decode('utf8')
        return json.loads(content)

    def get_theater_list(self):
        url = self.base_url_cinema_data
        # 영화관 요소를 리스트로 생성
        payload = self.make_payload(MethodName='GetCinemaItems')
        with urlopen(url, data=payload) as fin:
            json_content = self.byte_to_json(fin)
            return [
                {
                    'TheaterName': '{} 롯데시네마'.format(entry.get('CinemaNameKR')),
                    # 시네마(극장) 이름을 한글이름으로 반환
                    'TheaterID': '{}|{}|{}'.format(entry.get('DivisionCode'), entry.get('SortSequence'), entry.get('CinemaID')),
                    # 시네마 아이디를 반환
                    'Longitude': entry.get('Longitude'),
                    # 시네마의 위치 : 경도 반환
                    'Latitude': entry.get('Latitude')
                    # 시네마의 위치 : 위도 반환
                }
                for entry in json_content.get('Cinemas').get('Items')
            ]

    def distance(self, x1, x2, y1, y2):
        # 거리를 구하는 함수, (x1,y1) 와 (x2,y2)사이의 거리
        dx = float(x1) - float(x2)
        dy = float(y1) - float(y2)
        # 두 점 사이의 거리를 구하는 함수
        # sqrt(제곱근)을 사용하기 위해 math 모듈 참조
        distance = math.sqrt(dx**2 + dy**2)
        return distance

    def filter_nearest_theater(self, theater_list, pos_latitude, pos_longitude, n=3):
        # 가장 가까운 극장을 구하는 함수
        # pos_latitude : 현재 사용자 위치의 위도 , pos_longitude : 현재 사용자 위치의 경도
        distance_to_theater = []
        for theater in theater_list:
            distance = self.distance(pos_latitude, theater.get('Latitude'), pos_longitude, theater.get('Longitude'))
            distance_to_theater.append((distance, theater))
            # 리스트에 (거리, 극장이름) 형식으로 저장

        # 극장의 거리가 저장되어 있는 distance_to_theater 리스트를 정렬하고 가장가까운 극장(0번 요소 부터 3번까지)를 return
        return [theater for distance, theater in sorted(distance_to_theater, key=lambda x: x[0])[:n]]

    def get_movie_list(self, theater_id):
        # 영화 정보를 리스트로 보여주는 함수, 매개변수 : 극장 아이디
        url = self.base_url_movie_list
        # 영화 리스트 url
        target_dt = datetime.now()
        # 현재 시간을 저장
        target_dt_str = target_dt.strftime('%Y-%m-%d')
        # 날짜와 시간을 문자열(년도-월-일 형식)로 변환
        payload = self.make_payload(MethodName='GetPlaySequence', playDate=target_dt_str, cinemaID=theater_id, representationMovieCode='')
        with urlopen(url, data=payload) as fin:
            json_content = self.byte_to_json(fin)
            movie_id_to_info = {}
            # 영화의 MovieCode 를 저장하는 딕셔너리

            for entry in json_content.get('PlaySeqsHeader', {}).get('Items', []):
                movie_id_to_info.setdefault(entry.get('MovieCode'), {})['Name'] = entry.get('MovieNameKR')
            # 영화 한글 이름을 받아온 후 그것의 MovieCode 를 받아와 movie_id_to_info 딕셔너리에 저장
            for order, entry in enumerate(json_content.get('PlaySeqs').get('Items')):
                schedules = movie_id_to_info[entry.get('MovieCode')].setdefault('Schedules', [])
                # 영화 코드로 영화 스케줄 정보를 받아와 리스트로 저장
                schedule = {
                    'StartTime': '{}'.format(entry.get('StartTime')),
                    # 영화 시작 시간을 받아와 저장
                    'RemainingSeat': int(entry.get('TotalSeatCount')) - int(entry.get('BookingSeatCount'))
                    # 남은 좌석수를 받아와 저장(총 좌석수 - 예매된 좌석 수)
                }
                schedules.append(schedule)
                # 영화 schedule 을 schedules 리스트에 저장
            return movie_id_to_info

cinema = LotteCinema()

print(cinema.filter_nearest_theater(cinema.get_theater_list(), 37.5, 126.844))
# 가장 가까운 극장 3개를 출력
print(cinema.get_movie_list('1|2|1018'))
# 극장 아이디를 전달해 해당 극장의 영화 리스트를 출력
