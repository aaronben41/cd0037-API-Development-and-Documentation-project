import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def generate_random_integers(selection):
    num = random.randint(0 , len(selection) - 1)
    return num

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    #   CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    #DONE

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    
    #DONE

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods = ['GET'])
    def retrieve_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            return jsonify({
                'categories': {category.id:category.type for category in categories},
                'success': True,
                'total_categories': len(categories)
            })
        except:
           abort(404)

    #DONE
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods = ['GET'])
    def retrieve_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.id).all()


        if len(current_questions) == 0:
            abort(404)

        return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "current_category": categories[0].type,
                "categories": {category.id:category.type for category in categories}
            })

    #DONE
    
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question=Question.query.filter(Question.id==question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(selection)
            })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

    #DONE

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    
    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        body = request.get_json()

        question_new = body.get('question', '')
        answer_new = body.get('answer', '')
        category_new = body.get('category', 1)
        difficulty_new = body.get('difficulty', 1)
        search_term = body.get('searchTerm', None)

        if (question_new == '' or answer_new == '') and search_term is None:
            abort(422)

        try:
            if search_term:
                questions = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search_term))).all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(questions)
                })
            else:
                question = Question(question=question_new, answer=answer_new, category=category_new, difficulty=difficulty_new)
                question.insert()

                questions = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': len(questions)
                }), 201
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
  

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_category_questions(category_id):
        try:
            category = Category.query.filter(Category.id == category_id).one_or_none()

            if category is None:
                abort(404)

            category_questions= Question.query.order_by(Question.id).filter(Question.category == category_id).all()
            current_questions = paginate_questions(request, category_questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(category_questions),
                'current_category': category.type
            })
        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def retrieve_quizzes():
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')
        random_question = None

        try:
            if quiz_category is None or quiz_category['id'] == 0:
                questions_selection = [question.format() for question in Question.query.all()]
            else:
                questions_selection = [question.format() for question in Question.query.filter(Question.category == quiz_category['id']).all()]
                        
            questions = []
            for question in questions_selection:
                if question['id'] not in previous_questions:
                    questions.append(question)
                
            if (len(questions) > 0):
                random_question = random.choice(questions)
                    
            return jsonify({
                'success': True,
                'question': random_question,
                'previous_questions': previous_questions
            })   
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource Not Found"}),
            404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422)
    
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({"success": False, "error": 400, "message": "bad request"}), 400)

    @app.errorhandler(500)
    def bad_request(error):
        return (jsonify({"success": False, "error": 500, "message": "Internal server error"}), 500)



    return app

