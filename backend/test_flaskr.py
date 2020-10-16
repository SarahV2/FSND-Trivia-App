import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "question": "what are the cutest felines ever?",
            "answer": "cats",
            "difficulty": 2,
            "category": 1,
        }
        self.incomplete_question = {
            "question": "what are the cutest felines ever?",
            "answer": "cats",
            "difficulty": 2,
        }

        self.searchTerm = "felines"

    def tearDown(self):
        """Executed after reach test"""
        pass

    # --------------------------------------------------------------------------------------

    # GET /questions
    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["questions"]))

    def test_get_questions_404_error(self):
        res = self.client().get("/questions?page=500")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "the requested resource was not found")

    # --------------------------------------------------------------------------------------

    # GET /categories
    def test_get_all_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_post_categories_405_error(self):
        res = self.client().post("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    # --------------------------------------------------------------------------------------

    # POST /questions
    def test_post_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_post_question_400_error(self):
        res = self.client().post("/questions", json=self.incomplete_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    # --------------------------------------------------------------------------------------

    # DELETE /questions/<id:question_id>
    def test_delete_question(self):
        question_id = 16
        res = self.client().delete("/questions/{}".format(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted_q_id"], question_id)
        self.assertTrue(data["total_questions"])

    def test_delete_question_404_error(self):
        res = self.client().delete("/questions/110110")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "the requested resource was not found")

    # --------------------------------------------------------------------------------------

    # POST /questions/search
    def test_search_for_questions(self):
        res = self.client().post(
            "/questions/search", json={"searchTerm": self.searchTerm}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_search_400_error(self):
        res = self.client().post("/questions/search", json={"searchTerm": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    # --------------------------------------------------------------------------------------

    # GET /categories/<int:category_id>/questions
    def test_search_for_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_category_questions_404_error_invalid_category(self):
        res = self.client().get("/categories/110110/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "the requested resource was not found")

    # --------------------------------------------------------------------------------------

    # POST /quizzes
    def test_request_quiz_question(self):
        res = self.client().post(
            "quizzes",
            json={
                "quiz_category": {"type": "Science", "id": 1},
                "previous_questions": [],
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertTrue(data["total_questions"])

    def test_request_quiz_question_error_400(self):
        res = self.client().post("/quizzes", json={"quiz_category": 0})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
