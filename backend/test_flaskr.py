import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:123@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Testing GET /categories
    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # Testing GET /questions
    def test_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 10)

    # Testing error response for pages that don't exist
    def test_404_question_page_number(self):
        res = self.client().get('/questions?page=300')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    # Testing questions deletion
    def test_delete_question(self):
        # Creating a new question to be deleted
        old_total_number_of_questions = len(Question.query.all())
        question = Question(
            question = 'Test Delete Questions',
            answer = 'Test delete answer',
            category = '2',
            difficulty = 1
            )

        question.insert()

        new_total_number_of_questions = len(Question.query.all())

        res = self.client().delete(f'/questions/{question.id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], question.id)
        # Asserting that the number of questions before the deletion stays the same
        self.assertTrue(new_total_number_of_questions - old_total_number_of_questions == 1)
    
        db.session.close()

    # Testing deletion of wrong question ID
    def test_404_delete_question(self):
        res = self.client().delete('/questions/600')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    # Testing creation of new question
    def test_create_new_question(self):
        old_total_number_of_questions = len(Question.query.all())
        res = self.client().post('/questions', json={
            "question": "Test Questions",
            "answer": "Test Answer",
            "category": "2",
            "difficulty": 3
        })

        data = json.loads(res.data)

        new_total_number_of_questions = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'])
        # Asserting that question was successfuly added to the database
        self.assertTrue(new_total_number_of_questions - old_total_number_of_questions == 1)

        # Deleting the test question after the test
        Question.query.get(data['created_id']).delete()
        db.session.close()

    # Testing creation of new question with missing information
    def test_400_create_question(self):
        old_total_number_of_questions = len(Question.query.all())
        res = self.client().post('/questions', json={
            "question": "Test Questions",
            "answer": "",
            "category": "2",
            "difficulty": 3
        })

        data = json.loads(res.data)

        new_total_number_of_questions = len(Question.query.all())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'])
        # Asserting that question was not added to the database
        self.assertTrue(new_total_number_of_questions - old_total_number_of_questions == 0)   

    # Testing search method
    def test_search_questions(self):
        # Searching the word "invented" in the dummy database
        res = self.client().post('/questions/search', json={"searchTerm": "invented"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        # Searching the word "invented" should return 1 question from the dummy database
        self.assertEqual(data['total_questions'], 1)

    # Testing searching for a word not in database
    def test_404_search_questions(self):
        res = self.client().post('/questions/search', json={"searchTerm": "pool"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    # Testing GET categories' questions based on ID
    def test_get_categories_questions(self):
        # Getting all questions for category number 3: Geography
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    # Testing GET categories' questions based on ID for invalid category
    def test_400_get_categories_questions(self):
        
        res = self.client().get('/categories/555/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    # Test the game
    def test_play(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": [13, 14],
            "quiz_category": {"type": "Geography", "id": "3"}
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        # Assert that the question was not shown before
        self.assertNotEqual(data['question']['id'], 13)
        self.assertNotEqual(data['question']['id'], 14)

    # Test game failure
    def test_game_failure(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": [13, 14],
            "quiz_category": ""
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()