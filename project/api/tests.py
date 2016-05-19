import json

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from api.models import ApiToken
from website.accounts.models import User, Player
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
        player = Player.objects.create(user=self.user, username='NoName')

        data = {
            'id': '2016051813gm-0001-0000-d455c767',
        }
        response = self.client.post(reverse('api_add_tenhou_game'), data, **{'HTTP_TOKEN': token.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

        games = Game.objects.filter(player=player)
        self.assertEqual(games.count(), 1)
        self.assertEqual(games[0].external_id, data['id'])
        self.assertEqual(games[0].player_position, 2)

    def test_add_new_tenhou_game_without_id(self):
        token = ApiToken.objects.create(user=self.user)
        data = {
            'id': '',
        }
        response = self.client.post(reverse('api_add_tenhou_game'), {'data': data},
                                    **{'HTTP_TOKEN': token.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

        self.assertEqual(Game.objects.all().count(), 0)

    def test_add_new_tenhou_game_without_players(self):
        token = ApiToken.objects.create(user=User.objects.create_user('test', 'test1@test.com'))
        data = {
            'id': '1',
        }
        response = self.client.post(reverse('api_add_tenhou_game'), {'data': data},
                                    **{'HTTP_TOKEN': token.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

        self.assertEqual(Game.objects.all().count(), 0)
