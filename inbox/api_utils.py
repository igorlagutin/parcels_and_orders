import requests
import json
import telegram
from parcels_and_orders.env import AUTOLUX_API_URL, AUTOLUX_API_PASS, \
    AUTOLUX_API_LOGIN, BOT_TOKEN, NOVA_POST_API_URL, DRIVERS_PHONE, AUTOLUX_API_LOGIN_URL


class ApiTicketStatusUtils:

    def __init__(self, serial: str or int, deliver_name: str):
        self.serial = str(serial)
        self.deliver_name = deliver_name

    def _get_autolux_token(self, email: str, password: str) -> str:
        """Used for Autolux deliver to get API token"""
        payload = {'email': email, 'password': password}
        raw_response = requests.post(AUTOLUX_API_LOGIN_URL, data=payload)
        response = json.loads(raw_response.content.decode())
        return response['access_token']

    def _get_autolux_ofice_by_id(self, office_id: int) -> dict:

        """Used for Autolux deliver api to get office info"""
        access_token = self._get_autolux_token(
            AUTOLUX_API_LOGIN, AUTOLUX_API_PASS)
        api_address = AUTOLUX_API_URL
        payload = {'access_token': access_token}
        raw_office_info = requests.get(api_address + '/office', params=payload)
        json_office_info = json.loads(raw_office_info.content.decode())
        for office in json_office_info:
            if office['id'] == office_id:
                return office

    def get_ticket_deliver_status(self) -> dict:
        raw_status = {'CityRecipient': '',
                      'WarehouseRecipient': '',
                      'ScheduledDeliveryDate': '',
                      'Status': ''
                      }
        try:
            if self.deliver_name == 'Новая Почта':  # get data from Nova Post Api
                url = NOVA_POST_API_URL
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "modelName": "TrackingDocument",
                    "calledMethod": "getStatusDocuments",
                    "methodProperties": {
                        "Documents": [
                            {
                                "DocumentNumber": self.serial,
                                "Phone": DRIVERS_PHONE
                            }
                        ]
                    }
                }

                payload = json.dumps(payload, ensure_ascii=False)
                raw_response = requests.post(url, headers=headers, data=payload)
                response = raw_response.json()
                raw_status = {'CityRecipient': response.get('data')[0]['CityRecipient'],
                              'WarehouseRecipient': response.get('data')[0]['WarehouseRecipient'],
                              'ScheduledDeliveryDate': response.get('data')[0]['ScheduledDeliveryDate'],
                              'Status': response.get('data')[0]['Status']
                              }

            elif self.deliver_name == 'Автолюкс':
                access_token = self._get_autolux_token(
                    AUTOLUX_API_LOGIN,
                    AUTOLUX_API_PASS)
                payload = {'shipment_id': self.serial, 'access_token': access_token}
                raw_ttn_info = requests.get(
                    AUTOLUX_API_URL + 'shipment/search', params=payload)
                ttn_info = json.loads(raw_ttn_info.content.decode())
                if ttn_info:
                    json_ttn_info = ttn_info[0]
                    office = self._get_autolux_ofice_by_id(json_ttn_info['office_to_id'])
                else:
                    json_ttn_info = {
                        'status_title': 'ошибка получения',
                        'estimated_date_arrival': 'ошибка получения'}
                    office = {'territorial_unit_name': 'недоступно',
                              'address_ua': 'недоступно'}
                raw_status = {'CityRecipient': office['territorial_unit_name'],
                              'WarehouseRecipient': office['address_ua'],
                              'ScheduledDeliveryDate': json_ttn_info['estimated_date_arrival'],
                              'Status': json_ttn_info['status_title']}
        except BaseException as error:
            raw_status = {'CityRecipient': 'Ошибка получения города доставки',
                          'WarehouseRecipient': 'Ошибка получения пункта назначения',
                          'ScheduledDeliveryDate': 'Ошибка получения даты доставки',
                          'Status': 'Ошибка получения статуса: {}'.format(error)
                          }
        return raw_status
