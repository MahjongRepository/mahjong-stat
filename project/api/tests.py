from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from api.models import ApiToken
from website.accounts.models import Player
from website.games.models import Game


class ApiTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com')
        self.client = Client()

    def test_not_authorized_request(self):
        response = self.client.post(reverse('api_add_tenhou_game'), {})
        self.assertEqual(response.status_code, 401)

    def test_add_new_game_record(self):
        username = u'ばーや'
        token = ApiToken.objects.create(user=self.user)
        player = Player.objects.create(user=self.user, username=username)

        data = {
            'id': '2016051813gm-0001-0000-d455c767',
            'username': username
        }
        response = self.client.post(reverse('api_add_tenhou_game'), data, **{'HTTP_TOKEN': token.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

        games = Game.objects.filter(player=player)
        self.assertEqual(games.count(), 1)
        game = games[0]
        self.assertEqual(game.external_id, data['id'])
        self.assertEqual(game.player_position, 3)
        self.assertEqual(float(game.rate), 1440.14)
        self.assertEqual(game.rank, Game.SECOND_DAN)
        self.assertNotEqual(game.game_log_content, '')
        self.assertEqual(game.rounds.all().count(), 6)

    def test_add_already_added_game(self):
        token = ApiToken.objects.create(user=self.user)
        Player.objects.create(user=self.user, username='NoName')

        data = {
            'id': '2016051813gm-0001-0000-d455c767',
            'username': 'NoName'
        }
        response = self.client.post(reverse('api_add_tenhou_game'), data, **{'HTTP_TOKEN': token.token})
        self.assertEqual(response.json()['success'], True)

        response = self.client.post(reverse('api_add_tenhou_game'), data, **{'HTTP_TOKEN': token.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_add_new_tenhou_game_without_id(self):
        token = ApiToken.objects.create(user=self.user)
        data = {
            'id': '',
            'username': ''
        }
        response = self.client.post(reverse('api_add_tenhou_game'), data, **{'HTTP_TOKEN': token.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

        self.assertEqual(Game.objects.all().count(), 0)

    def test_add_new_tenhou_game_without_players(self):
        token = ApiToken.objects.create(user=self.user)
        data = {
            'id': '1',
            'username': '1'
        }
        response = self.client.post(reverse('api_add_tenhou_game'), data, **{'HTTP_TOKEN': token.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

        self.assertEqual(Game.objects.all().count(), 0)
