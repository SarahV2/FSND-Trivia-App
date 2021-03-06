import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]

    finalized_list = questions[start:end]
    return finalized_list


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    # ------------------------------------------------------------------------------------
    # GET all categories
    @app.route("/categories", methods=["GET"])
    def get_categories():
        if request.method == "POST":
            abort(405)
        try:
            categories = Category.query.all()
            avaliable_categories = {}
            for category in categories:
                avaliable_categories[category.id] = category.type

            return jsonify(
                {"success": True, "categories": avaliable_categories})
        except BaseException:
            abort(500)

    # ------------------------------------------------------------------------------------

    # GET all questions
    @app.route("/questions", methods=["GET"])
    def get_questions():
        questions_list = Question.query.all()

        categories = Category.query.all()
        avaliable_categories = {}
        for category in categories:
            avaliable_categories[category.id] = category.type
        current_list = paginate_questions(request, questions_list)

        # if the use requested a page with no more avaliable questions
        if len(current_list) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_list,
                "total_questions": len(questions_list),
                "categories": avaliable_categories,
                # "currentCategory": avaliable_categories,
            }
        )

    # ------------------------------------------------------------------------------------

    # POST a new question
    @app.route("/questions", methods=["POST"])
    def add_question():
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)

        if (
            new_question is None or
            new_answer is None or
            new_category is None or
            new_difficulty is None
        ):
            abort(400)

        newQuestion = Question(
            question=new_question,
            answer=new_answer,
            category=new_category,
            difficulty=new_difficulty,
        )

        newQuestion.insert()
        return jsonify({"success": True, "question": newQuestion.format()})

    # ------------------------------------------------------------------------------------

    # DELETE a question
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_Question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question is None:
            abort(404)

        try:
            question.delete()
            selection = Question.query.all()
            current_questions = paginate_questions(request, selection)
            return jsonify(
                {
                    "success": True,
                    "deleted_q_id": question_id,
                    "total_questions": len(Question.query.all()),
                }
            )
        except BaseException:
            abort(422)

    # ------------------------------------------------------------------------------------

    # Search for questions
    @app.route("/questions/search", methods=["POST"])
    def search():
        categories = Category.query.all()
        avaliable_categories = {}
        for category in categories:
            avaliable_categories[category.id] = category.type
        body = request.get_json()
        search_term = body.get("searchTerm", None)

        if search_term:
            search_query = Question.question.ilike(
                "%{}%".format(search_term)
            )  # look for the search term, ignoring the case sensetivity
            search_results = Question.query.filter(search_query).all()
            questions_list = [question.format() for question in search_results]
            if len(search_results) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": questions_list,
                    "total_questions": len(questions_list),
                }
            )
        else:
            abort(400)

    # ------------------------------------------------------------------------------------

    # GET questiond based on category
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        all_categories = Category.query.all()
        formatted_categories = [category.format()
                                for category in all_categories]
        list_of_ids = []
        for category in formatted_categories:
            list_of_ids.append(category["id"])

        # check if the id exists within the list of categories ids
        if category_id in list_of_ids:
            try:
                questions = Question.query.filter(
                    Question.category == category_id)
                questions_list = [question.format() for question in questions]
                if len(questions_list) == 0:
                    abort(404)
                return jsonify(
                    {
                        "success": True,
                        "questions": questions_list,
                        "total_questions": len(questions_list),
                    }
                )
            except BaseException:
                abort(500)
        else:
            abort(404)

    # ------------------------------------------------------------------------------------
    @app.route("/quizzes", methods=["POST"])
    def play():
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)

        # if no category or list provided within the request, abort with code
        # status 422 bad request
        if quiz_category is None or previous_questions is None:
            abort(400)

        try:
            if quiz_category["id"] == 0:
                questions = Question.query.all()
            # Get questions based on the specified category
            else:
                questions = Question.query.filter(
                    Question.category == quiz_category["id"]
                ).all()
            # only keep questions that are not included in
            # the previously asked questions' list
            # (filter the questions list by question id)

            filtered_questions = [
                question
                for question in questions
                if question.id not in previous_questions
            ]

            if len(filtered_questions) == 0:
                return jsonify(
                    {"message": "Sorry, no more questions avaliable"})

            # select a random question
            selected_question = random.choice(filtered_questions)

            return jsonify(
                {
                    "success": True,
                    "question": selected_question.format(),
                    "total_questions": len(questions),
                }
            )
        except BaseException:
            abort(500)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 404,
                    "message": "the requested resource was not found",
                }
            ),
            404,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify(
                {"success": False,
                 "error": 500,
                    "message": "internal server error", }
            ),
            500,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False,
                     "error": 400,
                     "message": "bad request", }),
            400,
        )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify(
                {"success": False,
                 "error": 422,
                 "message": "unprocessable entity", }
            ),
            422,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (jsonify({"success": False, "error": 405,
                         "message": "method not allowed", }), 405, )

    """
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  """

    return app
