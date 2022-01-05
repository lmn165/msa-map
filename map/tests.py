import csv
import json

from sphinx.util import requests

from common.models import ValueObject, Reader
import re


class GetLatLng:
    def __init__(self):
        pass

    def trans_geo(self, addr):
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
        headers = {"Authorization": "KakaoAK 494e0b25b56b815a43298d2314a551a0"}
        # get 방식으로 주소를 포함한 링크를 헤더와 넘기면 result에 json형식의 주소와 위도경도 내용들이 출력된다.
        result = json.loads(str(requests.get(url, headers=headers).text))
        status_code = requests.get(url, headers=headers).status_code
        if (status_code != 200):
            # print(f"ERROR: Unable to call rest api, http_status_coe: {status_code}")
            return 0

        # print(requests.get(url, headers=headers))
        # print(result)

        try:
            match_first = result['documents'][0]['address']
            long = match_first['x']
            lat = match_first['y']
            # print(lon, lat)
            print(f'위도: {match_first["y"]}, 경도: {match_first["x"]}')

            # return {'long':long, 'lat':lat}
        except IndexError:  # match값이 없을때
            return 0
        except TypeError:  # match값이 2개이상일때
            return 0

    def read_message(self):
        vo = ValueObject()
        vo.context = 'data/'
        vo.fname = 'seoul_message'
        reader = Reader()
        csvfile = reader.new_file(vo)
        message = reader.csv(csvfile)
        target_string = ['코로나', '방문', '검사']
        # target_string.append('서초구')
        message = message[message['내용'].map(lambda x: all(string in x for string in target_string))]
        # print(message)
        message.to_csv(vo.context+'new_data/message.csv', index=False)

    def test_read_address(self, message):
        # found = re.search('로', message).end()
        found = re.search('\w+로 ?\w+길 ?\d+', message)
        if found is not None:
            return found[0]

        found = re.search('\w+로 ?\d+길 ?\d+', message)
        if found is not None:
            return found[0]

        found = re.search('\w+로 ?\d+', message)
        if found is not None:
            return found[0]

        found = re.search('\w+동 ?\d+', message)
        if found is not None:
            return found[0]

        found = re.search('\w+동 ?\w+', message)
        if found is not None:
            return found[0]
        return 'None'

    def address_list(self):
        vo = ValueObject()
        vo.context = 'data/new_data/'
        vo.fname = 'message.csv'
        reader = Reader()
        self.csvfile = reader.new_file(vo)
        with open(self.csvfile, newline='', encoding='utf8') as csvfile:
            data_reader = csv.DictReader(csvfile)
            for row in data_reader:
                val = self.test_read_address(row['내용'])
                word_set = ['None', '성동구청', '강동구청', '이동동선', '성동구청', '이동경로']
                if val not in word_set:
                    print(val)


if __name__ == '__main__':
    g = GetLatLng()
    # g.trans_geo('경기도 파주시 중앙로 207')
    # g.read_message()
    # print(g.test_read_address('[서초구청] 7.23~24/7.28~31(09시~16시). 하나은행 서초동지점(서초대로 286) 방문자는 코로나19 유증상시 서초구 선별진료소에서 검사바랍니다.'))
    # print(g.test_read_address('[서초구청] 2020.12.3(목)~12.13(일) 정곡빌딩 동관(서초구 법원로16) 방문하신 분은 가까운 선별진료소에서 코로나19 검사 받으시기 바랍니다.'))
    # print(g.test_read_address('[성북구청]8.20.(목)14:09~15:06 성북동누룽지백숙(성북동,성북로31길9)방문자는 증상유무에 상관없이 선별진료소에서 코로나19검사를 받으시기 바랍니다.'))
    g.address_list()