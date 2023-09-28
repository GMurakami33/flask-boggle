from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with self.app.session_transaction() as session:
            session['board'] = [['T', 'E', 'S', 'T', 'E'],
                                ['S', 'T', 'E', 'S', 'T'],
                                ['E', 'S', 'T', 'E', 'S'],
                                ['S', 'T', 'E', 'S', 'T'],
                                ['T', 'E', 'S', 'T', 'E']]
            session['score'] = 0
            session['guessed_words'] = []

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('<h2>Guess A Word</h2>', html)

    def test_check_word_valid(self):
        response = self.app.post('/check-word', json={'word': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_check_word_duplicate(self):
        response = self.app.post('/check-word', json={'word': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_check_word_invalid(self):
        response = self.app.post('/check-word', json={'word': 'xyzyz'})
        self.assertEqual(response.status_code, 200)

    def test_check_word_not_on_board(self):
        response = self.app.post('/check-word', json={'word': 'apple'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['result'], 'not-on-board')