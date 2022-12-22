import json

import requests
from delivery.AdditionalsDeliveryServices import (additionals_boxberry,
                                                  additions_lpost)


class CalculationDelivery:
    def __init__(self, form_params):
        value_to_subject_dict = {
            '1': 'город федерального значения',
            '2': 'республика',
            '3': 'край',
            '4': 'область',
            '5': 'автономный округ',
            '6': 'автономная область'
        }
        self.weight = form_params['weight']
        self.length = form_params['length']
        self.width = form_params['width']
        self.height = form_params['height']
        self.cost = form_params['cost']
        self.city_from = form_params['city_from'].capitalize()
        self.subject_from = form_params['subject_from'].capitalize()
        self.subject_type_from = value_to_subject_dict[
            form_params['subject_type_from']].capitalize()
        self.city_to = form_params['city_to'].capitalize()
        self.subject_to = form_params['subject_to'].capitalize()
        self.subject_type_to = value_to_subject_dict[
            form_params['subject_type_to']].capitalize()
        self.volume = self.width * self.height * self.length
        self.ditance = 10

    def find_coordinates(self, place):
        geocoder_params = {
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
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

    def calculate_l_post(self):
        box_params = {
            'weight': self.weight,
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'quantity': 1,
        }
        place = f'{self.subject_to} {self.subject_type_to}, {self.city_to}'
        toponym_longitude, toponym_lattitude = self.find_coordinates(place)

        params = {
            'cityFrom': self.city_from,
        }

        response = requests.get('https://l-post.ru/l-backend/calc/'
                                'get-id-sklad',
                                params=params,
                                cookies=additions_lpost.cookies,
                                headers=additions_lpost.headers,)

        resp_text = response.text

        dict_of_response = json.loads(resp_text)
        id_sklad = dict_of_response['id_sklad']

        json_data = {
            'Calculator': {
                'cityFrom': self.city_from,
                'cityTo': self.city_to,
                'cityToWithRegion': place,
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

        dict_of_response = json.loads(resp_text)
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
        delivery_lpost = [f'До почтового отделения: за {day_logistic}'
                          f'(количество дней) за {courier_cost} рублей',
                          f'До двери: от {day_logistic_courier}'
                          f'(количество дней) за {to_post_cost} рублей'
                          ]
        return delivery_lpost

    def calculate_boxberry(self):
        with open('delivery/AdditionalsDeliveryServices/sities_code.json', 'r',
                  encoding='utf8') as read_file:
            cities_name_to_code = json.load(read_file)
        city_from = cities_name_to_code[self.city_from.lower()]
        city_to = cities_name_to_code[self.city_to.lower()]
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
        dict_of_response = json.loads(resp_text.text)
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
            f'До почтового отделения: за {coutier_delivery_day}'
            f'(количество дней) за {coutier_delivery_cost} рублей',
            f'До двери: от {post_delivery_day}'
            f'(количество дней) за {coutier_delivery_cost + 200} рублей'
        ]
        return delivery_boxberry
