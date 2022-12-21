import json

import requests
from delivery.DeliveryServices import additions_lpost, additions_pony_express


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
        self.city_from = form_params['city_from'].capitalize()
        self.subject_from = form_params['subject_from'].capitalize()
        self.subject_type_from = value_to_subject_dict[
            form_params['subject_type_from']].capitalize()
        # self.district_from = form_params['district_from'].capitalize()
        self.city_to = form_params['city_to'].capitalize()
        self.subject_to = form_params['subject_to'].capitalize()
        self.subject_type_to = value_to_subject_dict[
            form_params['subject_type_to']].capitalize()
        # self.district_to = form_params['district_to'].capitalize()
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
        delivery_lpost = [f'Доставка до почтового склада за {day_logistic} '
                          f'(кол-во дней) за {courier_cost}р',
                          f'Доставка курьером до двери за '
                          f'{day_logistic_courier}'
                          f'(кол-во дней) за {to_post_cost}р']
        return delivery_lpost

    def calculate_pony_express(self):
        data = {
            'parcel[currency_id]': '4',
            'parcel[tips_iblock_code]': 'form_tips',
            'parcel[tips_section_code]': 'pegas',
            'parcel[direction]': 'inner',
            'parcel[from_country]': 'Россия',
            'parcel[from_city]': 'Екатеринбург',
            'parcel[to_country]': 'Россия',
            'parcel[to_city]': 'Москва',
            'parcel[weight]': self.weight,
            'b_volume_l': '',
            'b_volume_h': '',
            'b_volume_w': '',
            'c_volume_l': '',
            'c_volume_d': '',
            't_volume_h': '',
            't_volume_b': '',
            't_volume_a': '',
            't_volume_c': '',
            'parcel[usecurrentdt]': '0',
            'parcel[kgo]': '0',
            'parcel[og]': '0',
            'parcel[isdoc]': '0',
        }

        response = requests.post(
            'https://www.ponyexpress.ru/local/ajax/tariff.php',
            cookies=additions_pony_express.cookies,
            headers=additions_pony_express.headers,
            data=data)
        resp_text = response.text

        print(resp_text)

        # delivery_pony_express = []
        # dict_of_response = json.loads(resp_text)
        # count_tariff = 0
        # text_tariff = 'tariffall'
        # for _ in range(len(dict_of_response['result'])):
        #     if count_tariff == 0:
        #         dict_for_tariff = dict_of_response['result'][text_tariff]
        #     else:
        #         dict_for_tariff = dict_of_response['result'][
        #             f'{count_tariff}:{text_tariff}']

        #     delivery_pony_express.append(f'{dict_for_tariff["servise"]} '
        #                                  f'стоимостью '
        #                                  f'{dict_for_tariff["tariff"]} за '
        #                                  f'{dict_for_tariff["delivery"]}
        # дней')
        #     count_tariff += 1
        # print(delivery_pony_express)
