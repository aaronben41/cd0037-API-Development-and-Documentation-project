# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.


# API Reference

# Endpoints

## GET /categories

Fetches all available categories,

Request arguments: None,

Returns all available categories and success value

Sample: 'curl http://127.0.0.1:5000/categories'

## GET /questions

Fetches a list of questions in all categories

Request arguments: Page

Returns paginated questions of 10 questions per page, the success value (True or False), number of total questions, categories and current category

Sample: 'curl http://127.0.0.1:5000/questions'

## GET /categories/<int:category_id>/questions

Fetches a list of questions based on a specified category

Request arguments: category id

Returns all questions in a given category, success value, number of total questions, and current category

Sample: curl http://127.0.0.1:5000/categories/3/questions

## DELETE /questions/<int:question_id>

Deletes a question using its question id

Request arguments: question id

Returns the ID of the deleted question and the success value

Sample: curl -X DELETE http://127.0.0.1:5000/questions/5

## POST /quizzes

Gets a question used to play the quiz. This endpoint takes a category and the previous question parameters, if available, and returns a new random question

Request arguments: The quiz category and question IDs of previous questions

Returns a random question within the selected category

## POST /questions

Creates a new question that is added to the database

Request arguments: question, answer, difficulty and category

Returns a success value, the id of the added question, paginated questions (also called 'current questions') - 10 questions page and total number of questions

Sample: curl -X POST -H "Content-Type: application/json" -d '{"question":"Sample Question", "answer":"Sample Answer", "difficulty":"3", "category":"5"}' http://127.0.0.1:5000/questions | jq '.'

## POST /questions/search

Searches for a question using a provided search term

Request argument: a search phrase

Returns a success value, a list of questions containing the search phrase, total questions in the search and their category


# Errors

## Error 400

Returns a json object with keys: success, error and message.

{"success": false, "error": 400, "message": "bad request"}

## Error 404

Returns a json object with keys: success, error and message.

{"success": false, "error": 404, "message": "Resource Not Found"}

## Error 405

Returns a json object with keys: success, error and message.

{"success": False, "error": 405, "message": "method not allowed"})

## Error 422

Returns a json object with keys: success, error and message.

{"success": false, "error": 422, "message": "unprocessable"}

## Error 500

Returns a json object with keys: success, error and message.

{"success": false, "error": 500, "message": "internal server error"}

# Testing

To run the tests on the flask app, run in the backend folder:

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py