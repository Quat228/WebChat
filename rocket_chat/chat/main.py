import requests


class RocketChat:

    def __init__(self, rocket_url):
        self.rocket_url = rocket_url
        self.auth_token = None
        self.user_id = None
        self.headers = None

    def login_as_admin(self):
        url = f'{self.rocket_url}/api/v1/login'
        payload = {
            "user": "Quat",
            "password": "2004Amerika$",
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers).json()

        self.auth_token = response['data']['authToken']
        self.user_id = response['data']['userId']
        self.headers = {'Content-Type': 'application/json', 'X-Auth-Token': self.auth_token, 'X-User-Id': self.user_id}

        return response

    def get_or_create_channel(self, channel_name: str, members: [str]):

        url = f'{self.rocket_url}/api/v1/channels.create'
        payload = {
            "name": channel_name,
            "members": members,
        }

        response = requests.post(url, json=payload, headers=self.headers).json()

        if not response['success'] and response['errorType'] == 'error-duplicate-channel-name':
            url = f'{self.rocket_url}/api/v1/channels.info?'
            payload = {
                "roomName": channel_name,
            }
            for key, value in payload.items():
                url += f'{key}={value}&'
            response = requests.get(url, headers=self.headers).json()

        return response

    def integrations_list(self, integration_type=None):
        url = f'{self.rocket_url}/api/v1/integrations.list'
        response = requests.get(url, headers=self.headers).json()
        if integration_type:
            integrations_list = []
            for integration in response['integrations']:
                if integration['type'] == integration_type:
                    integrations_list.append(integration)
            response['integrations'] = integrations_list
        return response
    
    def integrations_remove(self, integration_id, integration_type):
        url = f'{self.rocket_url}/api/v1/integrations.remove'
        payload = {
            "integrationId": integration_id,
            "type": integration_type,
        }
        response = requests.post(url, json=payload, headers=self.headers).json()
        return response

    def integrations_remove_all(self, integrations_type=None):
        for integration in self.integrations_list(integration_type=integrations_type)['integrations']:
            self.integrations_remove(integration_id=integration['_id'], integration_type=integration['type'])

    def get_or_create_income_integration(self, username, channel, script_enabled: bool = True):
        integrations_list = self.integrations_list(integration_type='webhook-incoming')['integrations']
        for integration in integrations_list:
            if f'#{channel}' in integration['channel']:
                webhook_url = f"{self.rocket_url}/hooks/{integration['_id']}/{integration['token']}"
                return webhook_url

        url = f'{self.rocket_url}/api/v1/integrations.create'
        payload = {
            "type": 'webhook-incoming',
            "username": username,
            "channel": f'#{channel}',
            "scriptEnabled": script_enabled,
            "name": "TelegramBot",
            "enabled": True,
        }
        response = requests.post(url, json=payload, headers=self.headers).json()
        integration1 = response['integration']

        webhook_url = f"{self.rocket_url}/hooks/{integration1['_id']}/{integration1['token']}"

        return webhook_url

    def get_or_create_outcome_integration(self, event, username, channel, urls: [str],
                                          script_enabled: bool = True, token: str = ''):
        integrations_list = self.integrations_list(integration_type='webhook-outgoing')['integrations']
        for integration in integrations_list:
            if f'#{channel}' in integration['channel']:
                webhook_url = f"{self.rocket_url}/hooks/{integration['_id']}/{integration['token']}"
                return webhook_url

        url = f'{self.rocket_url}/api/v1/integrations.create'
        payload = {
            "type": 'webhook-outgoing',
            "event": event,
            "username": username,
            "channel": f'#{channel}',
            "urls": urls,
            "scriptEnabled": script_enabled,
            "name": "TelegramBot",
            "enabled": True,
            "token": token,
        }
        response = requests.post(url, json=payload, headers=self.headers).json()

        return response

    def create_user(self, name, username, password, email, roles: [str] = None):
        if not roles:
            roles = ['user']
        url = f'{self.rocket_url}/api/v1/users.create'
        payload = {
            "name": name,
            "username": username,
            "password": password,
            "email": email,
            "roles": roles,
        }
        response = requests.post(url, json=payload, headers=self.headers).json()

        return response

    def get_or_create_visitor(self, random_token, department='', name='', email='', phone=''):
        url = f'{self.rocket_url}/api/v1/livechat/visitor'
        payload = {
            "visitor": {
                "token": random_token,
                "name": name,
                "email": email,
                "department": department,
                "phone": phone,
            }
        }
        response = requests.post(url, json=payload, headers=self.headers).json()

        return response

    def get_all_rooms(self, updated_since=''):
        url = f'{self.rocket_url}/api/v1/rooms.get?'
        payload = {
            "updatedSince": updated_since,
        }
        for key, value in payload.items():
            url += f'{key}={value}&'
        response = requests.get(url, headers=self.headers).json()

        return response

    def get_room_info(self, room_name=None, room_id=None):
        url = f'{self.rocket_url}/api/v1/rooms.info?'

        payload = {}
        if room_name:
            payload['roomName'] = room_name
        if room_id:
            payload['roomId'] = room_id

        for key, value in payload.items():
            url += f'{key}={value}&'
        response = requests.get(url, headers=self.headers).json()

        return response

    def get_available_agents(self):
        url = f'{self.rocket_url}/api/v1/omnichannel/agents/available'
        response = requests.get(url, headers=self.headers).json()

        return response

    def get_or_create_livechat_room(self, visitor_token, rid='', agent_id=''):
        url = f'{self.rocket_url}/api/v1/livechat/room?'
        payload = {
            "token": visitor_token,
            "rid": rid,
            "agentId": agent_id,
        }
        for key, value in payload.items():
            url += f'{key}={value}&'
        response = requests.get(url, headers=self.headers).json()

        return response

    def send_livechat_message(self, visitor_token, rid, msg):
        url = f'{self.rocket_url}/api/v1/livechat/message'
        payload = {
            "token": visitor_token,
            "rid": rid,
            "msg": msg,
        }
        response = requests.post(url, json=payload, headers=self.headers).json()

        return response

    def start_call(self, rid):
        url = f'{self.rocket_url}/api/v1/livechat/webrtc.call?'
        payload = {
            "rid": rid,
        }
        for key, value in payload.items():
            url += f'{key}={value}&'
        response = requests.get(url, headers=self.headers).json()

        return response

    def get_all_departments(self):
        url = f'{self.rocket_url}/api/v1/livechat/department'
        response = requests.get(url, headers=self.headers).json()

        return response

    def transfer_livechat_room(self, visitor_token, rid, department_id):
        url = f'{self.rocket_url}/api/v1/livechat/room.transfer'
        payload = {
            "token": visitor_token,
            "rid": rid,
            "department": department_id,
        }
        response = requests.post(url, json=payload, headers=self.headers).json()

        return response

    def create_department(self, name, email, description='', show_on_registration=True):
        url = f'{self.rocket_url}/api/v1/livechat/department'
        payload = {
            "department": {
                "enabled": True,
                "showOnOfflineForm": True,
                "name": name,
                "email": email,
                "description": description,
                "showOnRegistration": show_on_registration,
            }
        }
        response = requests.post(url, json=payload, headers=self.headers).json()

        return response

    def remove_department(self, department_id):
        url = f'{self.rocket_url}/api/v1/livechat/department/{department_id}'
        response = requests.delete(url, headers=self.headers).json()

        return response


rocket_chat = RocketChat('http://192.168.0.133:3000')
rocket_chat.login_as_admin()
# rocket_chat.create_user(name='TelegramBot', username='TelegramBot',
#                         password='TelegramBot', email='zharkulov0405@mail.ru', roles=['bot'])
#
# rocket_channel = rocket_chat.get_or_create_channel(channel_name='Telegram2', members=['Quat'])

# print(rocket_chat.get_all_departments())

# print(rocket_chat.get_or_create_visitor(random_token='random_token', name='Quat4', department='Telegram'))
# print(rocket_chat.get_or_create_livechat_room(visitor_token='random_token'))
# print(rocket_chat.send_livechat_message(visitor_token='random_token', rid='nbpqdGQqvNedNKXrN', msg='Hi guys!'))


# print(rocket_chat.get_room_info(room_id='XkuELJzPd4WLgjsEdk73NxiQvhgXgbE5dx'))
#
# print(rocket_chat.start_call(rid='XkuELJzPd4WLgjsEdk73NxiQvhgXgbE5dx'))




