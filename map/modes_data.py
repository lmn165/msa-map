import os
import re

import django
import csv
import sys
from common.models import ValueObject, Reader
# system setup
from map.models import Map, MedPoint
# SET FOREIGN_KEY_CHECKS = 0;
from sphinx.util import requests
import json


class DbUploader():
    def __init__(self):
        self.vo = ValueObject()
        self.reader = Reader()
        self.vo.context = 'map/data/'

    def insert_data(self):
        self.insert_med_point()
        self.insert_world_map()
        self.insert_map_with_med_geo()
        self.insert_map_with_cases_geo()

    def insert_med_point(self):
        self.vo.fname = 'med_point_20211115.csv'
        self.csvfile = self.reader.new_file(self.vo)
        with open(self.csvfile, newline='', encoding='utf8') as csvfile:
            data_reader = csv.DictReader(csvfile)
            for row in data_reader:
                if not MedPoint.objects.filter(med_point_name=row['의료기관명']).exists():
                    MedPoint.objects.create(med_point_name=row['의료기관명'])
            print('MED POINT DATA UPLOADED SUCCESSFULLY!')

    def insert_map_with_med_geo(self):
        self.vo.fname = 'med_point_20211115.csv'
        self.csvfile = self.reader.new_file(self.vo)
        with open(self.csvfile, newline='', encoding='utf8') as csvfile:
            data_reader = csv.DictReader(csvfile)
            for row in data_reader:
                m = MedPoint()
                med_point = MedPoint.objects.all().filter(med_point_name=row['의료기관명']).values()[0]
                m.id = med_point['id']
                if not Map.objects.filter(name=row['의료기관명']).exists():
                    geo = self.trans_geo(row['주소'])
                    if geo != 0:
                        Map.objects.create(type='medpoint',
                                           name=row['의료기관명'],
                                           meta=row['주소'],
                                           latitude=geo['lat'],
                                           longitude=geo['long'],
                                           med_point=m)

    def trans_geo(self, addr):
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + addr
        headers = {"Authorization": "KakaoAK 494e0b25b56b815a43298d2314a551a0"}
        result = json.loads(str(requests.get(url, headers=headers).text))
        status_code = requests.get(url, headers=headers).status_code
        if (status_code != 200):
            return 0

        try:
            match_first = result['documents'][0]['address']
            long = match_first['x']
            lat = match_first['y']

            return {'long': long, 'lat': lat}
        except IndexError:  # match값이 없을때
            return 0
        except TypeError:  # match값이 2개이상일때
            return 0

    def insert_map_with_cases_geo(self):
        self.vo.fname = 'new_data/message.csv'
        self.csvfile = self.reader.new_file(self.vo)
        with open(self.csvfile, newline='', encoding='utf8') as csvfile:
            data_reader = csv.DictReader(csvfile)
            for row in data_reader:
                val = self.test_read_address(row['내용'])
                word_set = ['None', '성동구청', '강동구청', '이동동선', '성동구청', '이동경로']
                if val not in word_set:
                    geo = self.trans_geo(val)
                    if geo != 0:
                        Map.objects.create(type='cases',
                                           name=val,
                                           meta=f'{row["연"]}-{"%02d"%int(row["월"])}-{"%02d"%int(row["일"])}',
                                           latitude=geo['lat'],
                                           longitude=geo['long'])

    def test_read_address(self, message):
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

    def insert_world_map(self):
        self.vo.fname = 'new_data/integrated_cases.csv'
        self.csvfile = self.reader.new_file(self.vo)
        with open(self.csvfile, newline='', encoding='utf8') as csvfile:
            data_reader = csv.DictReader(csvfile)
            for row in data_reader:
                # m = Map()
                # map = Map.objects.all().filter(name=row['name']).values()[0]
                # m.id = map['id']
                if not Map.objects.filter(name=row['name']).exists():
                    Map.objects.create(type='world',
                                           name=row['name'],
                                           meta=row['short_name'],
                                           population=row['population'],
                                           cases=row['cases']
                                       )
                else:
                    Map.objects.filter(type='world', name=row['name']).update(
                        population=row['population'], cases=row['cases'])
            print('WORLD MAP DATA UPLOADED SUCCESSFULLY!')
