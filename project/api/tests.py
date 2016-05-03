import json

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from api.models import ApiToken
from website.accounts.models import User
from website.games.models import Game


class ApiTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com')
        self.client = Client()

    def test_not_authorized_request(self):
        response = self.client.post(reverse('api_add_tenhou_game'), {})
        self.assertEqual(response.status_code, 401)

    def test_add_new_game_record(self):
        token = ApiToken.objects.create(user=self.user)
        data = {
            'id': '2016050122gm-0009-7999-x3b3ca93e0c99&tw=2',
            'position': 1
        }
        response = self.client.post(reverse('api_add_tenhou_game'), {'data': json.dumps(data)},
                                    **{'HTTP_TOKEN': token.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

        self.assertEqual(Game.objects.all().count(), 1)
        self.assertEqual(Game.objects.all()[0].external_id, data['id'])
        self.assertEqual(Game.objects.all()[0].player_position, data['position'])
