import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10
# Pagination function
def paginate(request, questions):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  paginated_questions = [question.format() for question in questions]
  returned_questions = paginated_questions[start:end]

  return returned_questions

def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # CORS setup
  CORS(app)

  # CORS headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Acces-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
    
    return response

  # GET /categories
  @app.route('/categories')
  def get_categories():
    error = False
    categories = Category.query.all()
    res_body = {}
    
    if len(categories) == 0:
      error = True
      abort (404)

    categories_dict = {category.id: category.type for category in categories}
    res_body['categories'] = categories_dict
    res_body['success'] = True

    return jsonify(res_body)


  # GET /questions?page={}
  @app.route('/questions')
  def get_questions():
    error = False
    res_body = {}
    questions = Question.query.all()
    categories = Category.query.all()

    # Paginate 10 questions per page according to paginate function defined at the start of the file
    shown_questions = paginate(request, questions)
    number_of_questions = len(questions)
    
    if len(shown_questions) == 0 or len(categories) == 0:
      error = True
      abort (404)


    categories_dict = {category.id: category.type for category in categories}
    res_body['success'] = True
    res_body['questions'] = shown_questions
    res_body['total_questions'] = number_of_questions
    res_body['categories'] = categories_dict

    return jsonify(res_body)


  # DELETE /questions/{id}
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    error = False
    question = Question.query.get(id)
    
    # Aborting if no question found
    if not question:
      abort (404)

    try:
      question.delete()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()

    if error:
      abort (422)
    
    return jsonify({
      'success': True,
      'deleted_id': question.id
    })

  # POST /questions 
  @app.route('/questions', methods=['POST'])
  def add_question():
    error = False
    req_body = request.get_json()
    question = req_body['question']
    answer = req_body['answer']
    difficulty = req_body['difficulty']
    category = req_body['category']

    if not question or not answer or not difficulty or not category:
        abort (400)

    question = Question(
      question = question,
      answer = answer,
      difficulty = difficulty,
      category = category
    )

    try:
      question.insert()
      return jsonify({
        "success": True,
        "created_id": question.id
      })
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()

    if error:
      abort (422)



  # POST /questions/search 
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    error = False
    search_term = request.get_json()['searchTerm']
    res_body = {}

    questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

    # Abort if no matches
    if len(questions) == 0:
      abort (404)

    # Paginate questions
    shown_questions = paginate(request, questions)

    try:
      res_body['questions'] = shown_questions
      res_body['total_questions'] = len(questions)
      res_body['success'] = True
    except:
      error = True
      print(sys.exc_info())
    
    if error:
      abort (422)
    else:
      return jsonify(res_body)


  # GET /categories/{id}/questions
  @app.route('/categories/<int:id>/questions')
  def get_categories_questions(id):
    error = False
    res_body = {}

    category = Category.query.filter_by(id=id).one_or_none()

    if category is None:
      abort (404)
    
    questions = Question.query.filter_by(category=category.id).all()

    if len(questions) == 0:
      abort (404)

    shown_questions = paginate(request, questions)

    try:
      res_body['success'] = True
      res_body['questions'] = shown_questions
      res_body['total_questions'] = len(questions)
    except:
      error = True
      print(sys.exc_info())
    
    if error:
      abort (422)
    else:
      return jsonify(res_body)


  # Quizzes
  @app.route('/quizzes', methods=['POST'])
  def quiz():
    error = False
    req_body = request.get_json()
    
    if not req_body['quiz_category']:
      error = True
      abort (400)

    # Loading quiz questions. The 'ALL' category has an id=0 that's why it's given that condition here
    if req_body['quiz_category']['id'] == 0:
      questions = Question.query.all()
    else:
      questions = Question.query.filter_by(category=req_body['quiz_category']['id']).all()

    # Generating a random question
    def random_question():
      return questions[random.randrange(0, len(questions), 1)]

    
    # Puting all the id questions in a list
    all_questions_id = [question.id for question in questions]

    used_questions_id = req_body['previous_questions']

    available_questions = [question for question in all_questions_id if question not in used_questions_id]

    print(available_questions)

    # Showing score if all questions is used
    if len(available_questions) == 0:
      return jsonify({
          "success": True
        })


    # Generating a random question from the avaiable list
    rand_question = available_questions[random.randrange(0, len(available_questions), 1)]

    question = Question.query.filter_by(id=rand_question).one_or_none()

    return jsonify({
      "success": True,
      "question": question.format()
    })  


  ############## ERROR HANDLERS #######################
 
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found"
    }), 404

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
    }), 400

  @app.errorhandler(422)
  def not_processable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable"
    }), 422

  
  return app

    