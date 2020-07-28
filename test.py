from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Setup before each test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test HTML display and session information"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        """Test a valid word in the board"""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["E", "A", "E", "T", "B"], 
                                 ["G", "P", "W", "G", "S"], 
                                 ["G", "S", "Q", "H", "E"], 
                                 ["A", "F", "E", "P", "V"], 
                                 ["C", "D", "T", "J", "L"]]
        response = self.client.get('/check-word?word=egg')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word exists"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')


    def test_not_on_board(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get('/check-word?word=incomprehensiveness')
        self.assertEqual(response.json['result'], 'not-on-board')
        