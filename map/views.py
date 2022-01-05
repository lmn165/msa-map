from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes

from map.modes_data import DbUploader
from map.serializer import MapSerializer
from map.models import Map


@api_view(['GET'])
@parser_classes([JSONParser])
def upload(request):
    print('############ 1 ##########')
    DbUploader().insert_data()
    return JsonResponse({'Map Data Upload': 'SUCCESS'})


@api_view(['GET'])
@parser_classes([JSONParser])
def world_maps(request):
    all_region = Map.objects.filter(type='world').order_by('-cases')[:10]
    korea = Map.objects.filter(name='S. Korea')
    serializer = MapSerializer(all_region.union(korea), many=True)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['POST'])
@parser_classes([JSONParser])
def med_points(request):
    current_geo = request.data
    # print(current_geo)
    med_points = Map.objects.raw('SELECT *, (6371*acos(cos(radians(%s))*cos(radians(latitude))*cos(radians(longitude)'
                                                         '-radians(%s))+sin(radians(%s))*sin(radians(latitude)))) '
                                                         'AS distance FROM maps WHERE type = "medpoint" HAVING distance < 2 ORDER BY distance',
                                                         [current_geo["latitude"], current_geo["longitude"], current_geo["latitude"]])
    serializer = MapSerializer(med_points, many=True)
    # print(serializer.data)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['POST'])
@parser_classes([JSONParser])
def cases_points(request):
    current_geo = request.data
    cases_points = Map.objects.raw('SELECT *, (6371*acos(cos(radians(%s))*cos(radians(latitude))*cos(radians(longitude)'
                                             '-radians(%s))+sin(radians(%s))*sin(radians(latitude)))) '
                                             'AS distance FROM maps WHERE type="cases" GROUP BY name HAVING distance < 2 ORDER BY distance',
                                             [current_geo["latitude"], current_geo["longitude"], current_geo["latitude"]])
    serializer = MapSerializer(cases_points, many=True)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['GET'])
@parser_classes([JSONParser])
def med_point(request, med_point):
    med_point_info = Map.objects.filter(med_point=med_point)[0]
    serializer = MapSerializer(med_point_info)
    return JsonResponse(data=serializer.data, safe=False)
