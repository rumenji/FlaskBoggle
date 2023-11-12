from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_show_board(self):
        with self.client:
            response = self.client.get('/')
            
            self.assertIn('board', session)
            self.assertIn(b'<tr>', response.data)
            self.assertIsNone(session.get('high_score'))
            self.assertIsNone(session.get('played'))
            


    def test_check_valid_guess(self):
        with self.client as client:
            with client.session_transaction() as game:
                game['board'] = [['Q', 'A', 'V', 'E', 'Q'],
                                ['K', 'E', 'T', 'N', 'Y'],
                                ['H', 'U', 'U', 'X', 'U'],
                                ['B', 'G', 'Z', 'M', 'Z'],
                                ['I', 'R', 'P', 'P', 'R']]
        
        response = self.client.post('/', data = json.dumps({'guess': 'at'}), headers={'Content-Type': 'application/json'} )
        self.assertEqual(response.json, 'ok')

        response2 = self.client.post('/', data = json.dumps({'guess': 've'}), headers={'Content-Type': 'application/json'} )
        self.assertEqual(response2.json, 'not-word')

        response3 = self.client.post('/', data = json.dumps({'guess': 'word'}), headers={'Content-Type': 'application/json'} )
        self.assertEqual(response3.json, 'not-on-board')

    def test_high_score(self):
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 8
                change_session['played'] = 1
            response = self.client.post('/high_score', data = json.dumps({'score': 6}), headers={'Content-Type': 'application/json'} )
            self.assertEqual(session['high_score'], 8)

            response2 = self.client.post('/high_score', data = json.dumps({'score': 10}), headers={'Content-Type': 'application/json'} )
            self.assertEqual(session['high_score'], 10)


    
