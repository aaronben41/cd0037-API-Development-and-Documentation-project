import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables app."""
        self.question_new = {
            "question": "Sample question",
            "answer": "Sample answer",
            "difficulty": 3,
            "category": 4
        }
        self.question_new_422 = {
            "answer": "Sample answer",
            "category": 2
        }

        self.search_term = {
            "searchTerm": "search"
        }

        self.quiz_422 = {
            "quiz_category": {},
            "previous_questions": {}
        }
        
        """Initialize app"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format(
            "postgres:7777", "localhost:5432", self.database_name
            )

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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["categories"]), data["total_categories"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_categories"])

    
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
    
    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get('/questions?page=97')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_question(self):
        question = Question.query.first()
        question = question.format()
        res = self.client().delete(f"/questions/{question['id']}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], question['id'])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_404_not_found_delete_question(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_new_question(self):
        res = self.client().post("/questions", json=self.question_new)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_422_unprocessable_new_question(self):
        res = self.client().post("/questions", json=self.question_new_422)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], "unprocessable")
        self.assertTrue(data['error'])
    
    def test_search_questions(self):
            res = self.client().post("/questions", json=self.search_term)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)
            self.assertTrue(data['questions'])
            self.assertTrue(data['total_questions'])
    
    def test_retrieve_category_questions(self):
        res = self.client().get("/categories/3/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['current_category'], "Geography")
        self.assertEqual(data["success"], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_not_found_retrieve_category_questions(self):
        res = self.client().get("/categories/150/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_retrieve_quiz(self):
        quiz = {
            "quiz_category": {"id": 2, "type": "Art"},
            "previous_questions": [23, 24]
        }
        res = self.client().post("/quizzes", json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertNotEqual(data['question']['id'], 23)
        self.assertNotEqual(data['question']['id'], 24)
    
    def test_422_unprocessable_retrieving_quizzes(self):
        res = self.client().post("/quizzes", json=self.quiz_422)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], "unprocessable")
        self.assertTrue(data['error'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()