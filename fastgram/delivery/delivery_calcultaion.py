import json

import requests
from django.conf import settings

from delivery.AdditionalsDeliveryServices import (additionals_boxberry,
                                                  additions_lpost)


class CalculationDelivery:
    def __init__(self, weight, length, width, height,
                 cost, city_from, city_to):
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.cost = cost
        self.city_from = city_from
        self.city_to = city_to
        self.volume = self.width * self.height * self.length


class CalculateLPost(CalculationDelivery):
    def __init__(self, weight, length, width, height,
                 cost, city_from, city_to):
        super().__init__(weight, length, width, height,
                         cost, city_from, city_to)

    def find_coordinates(self, place):
        geocoder_params = {
            'apikey': settings.YANDEX_MAPS_API_KEY,
            'geocode': place,
            'format': 'json'}
        response = requests.get(
            'http://geocode-maps.yandex.ru/1.x/?', params=geocoder_params)
        json_response = response.json()
        toponym = json_response['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']
        toponym_coodrinates = toponym['Point']['pos']
        toponym_longitude = float(toponym_coodrinates.split(' ')[0])
        toponym_lattitude = float(toponym_coodrinates.split(' ')[1])
        return toponym_longitude, toponym_lattitude

    def get_is_sklad(self):
        response = requests.get('https://l-post.ru/l-backend/calc/'
                                'get-id-sklad',
                                params={'cityFrom': self.city_from},
                                cookies=additions_lpost.cookies,
                                headers=additions_lpost.headers,)

        resp_text = response.text

        dict_of_response = json.loads(resp_text)
        return dict_of_response['id_sklad']

    def get_response_from_lpost(self):
        box_params = {
            'weight': self.weight,
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'quantity': 1,
        }

        toponym_longitude, toponym_lattitude = self.find_coordinates(
            self.city_to)

        id_sklad = self.get_is_sklad()

        json_data = {
            'Calculator': {
                'cityFrom': self.city_from,
                'cityTo': self.city_to,
                'cityToWithRegion': self.city_to,
                'boxes': [
                    {
                        'size': 'custom',
                        'params': box_params,
                    },
                ],
                'weight': self.weight * 1000,
                'volume': self.volume,
                'sum_payment': 0,
                'value': 0,
                'options': {
                    'return_documents': False,
                },
                'id_sklad': id_sklad,
                'longitude': toponym_longitude,
                'latitude': toponym_lattitude,
                'distance': 10,
            },
        }

        response = requests.post('https://l-post.ru/api/get-services'
                                 '-by-coordinates/',
                                 cookies=additions_lpost.cookies,
                                 headers=additions_lpost.headers,
                                 json=json_data)

        resp_text = response.text

        return json.loads(resp_text)

    def calculate_l_post(self):
        dict_of_response = self.get_response_from_lpost()

        courier_cost = dict_of_response['services'][1]['sum_cost']
        day_logistic = dict_of_response['services'][0]['day_logistic']
        to_post_cost = dict_of_response['services'][0]['sum_cost']
        if courier_cost == to_post_cost:
            if courier_cost == 250:
                to_post_cost = 150
            else:
                to_post_cost = f'{courier_cost - 150} - {courier_cost - 50}'

        if day_logistic - 1 == 0:
            day_logistic_courier = 'срок меньше дня'
        else:
            day_logistic_courier = day_logistic - 1
        delivery_lpost = [f'за {day_logistic}(количество дней) '
                          f'за {courier_cost} рублей',
                          f'от {day_logistic_courier}(количество дней) '
                          f'за {to_post_cost} рублей'
                          ]
        return delivery_lpost


class CalculateBoxberry(CalculationDelivery):
    def __init__(self, weight, length, width, height,
                 cost, city_from, city_to):
        super().__init__(weight, length, width, height,
                         cost, city_from, city_to)

    def get_sities_code(self):
        with open('delivery/AdditionalsDeliveryServices/sities_code.json', 'r',
                  encoding='utf8') as read_file:
            cities_name_to_code = json.load(read_file)
        city_from = cities_name_to_code[self.city_from.lower()]
        city_to = cities_name_to_code[self.city_to.lower()]
        return city_from, city_to

    def get_response_from_boxberry(self):
        city_from, city_to = self.get_sities_code()
        params = {
            'method': 'TarificationLaP',
            'sender_city': city_from,
            'receiver_city': city_to,
            'public_price': self.cost * 100,
            'package[boxberry_package]': 0,
            'package[width]': self.width,
            'package[height]': self.height,
            'package[depth]': self.length,
        }
        resp_text = requests.get(
            'https://boxberry.ru/proxy/delivery/cost/pip?',
            params=params,
            cookies=additionals_boxberry.cookies,
            headers=additionals_boxberry.headers,
        )
        return json.loads(resp_text.text)

    def calculate_boxberry(self):
        dict_of_response = self.get_response_from_boxberry()

        coutier_delivery_cost = dict_of_response['data'][0][
            'default_services_cost'] / 100
        coutier_delivery_day = int(dict_of_response['data'][0]['time'])

        if coutier_delivery_day - 1 == 0:
            post_delivery_day = 'меньше дня'
        else:
            post_delivery_day = coutier_delivery_day - 1
        if int(coutier_delivery_cost) == float(coutier_delivery_cost):
            coutier_delivery_cost = int(coutier_delivery_cost)
        delivery_boxberry = [
            f'за {coutier_delivery_day}(количество дней) '
            f'за {coutier_delivery_cost} рублей',
            f'от {post_delivery_day}(количество дней) '
            f'за {coutier_delivery_cost + 200} рублей'
        ]
        return delivery_boxberry
