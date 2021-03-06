# Full Stack API Final Project

## Full Stack Trivia

This project is a part of Udacity learning projects where it's required to implement the knowledge they shared on API endpoints and testing in creating a trivia application with a game for tasting one's knowledge in certain category.

The project should be able to do the following: 

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app gave me the ability to structure plan, implement, and test an API.

## Getting Started
### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the frontend

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


### Testing
To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql<br>
python test_flaskr.py

```

ignore the dropdb command the first time you run tests

### API

#### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `http://127.0.0.1:5000/`



#### Error Handling

Errors are always returned as JSON object formatted as:
	{
		"success": False,
		"error": 422,
		"message": Unprocessable
	}

This API returns three types of errors:
* 400 - Bad request
* 404 - Not found
* 422 - unprocessable


#### End points
##### GET /categories
* General: Returns a list categories.
* Sample: `curl http://127.0.0.1:5000/categories` 

        {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
            }, 
            "success": true
        }

##### GET /questions

* General:
  * Returns a list of paginated questions (10 questions per page).
  * Returns list of categories and total number of questions.
* Sample: `curl http://127.0.0.1:5000/questions`
	{
	  "categories": {
	    "1": "Science", 
	    "2": "Art", 
	    "3": "Geography", 
	    "4": "History", 
	    "5": "Entertainment", 
	    "6": "Sports"
	  }, 
	  "questions": [
	    {
	      "answer": "Apollo 13", 
	      "category": 5, 
	      "difficulty": 4, 
	      "id": 2, 
	      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
	    }, 
	    {
	      "answer": "Tom Cruise", 
	      "category": 5, 
	      "difficulty": 4, 
	      "id": 4, 
	      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
	    }, 
	    {
	      "answer": "Edward Scissorhands", 
	      "category": 5, 
	      "difficulty": 3, 
	      "id": 6, 
	      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
	    }, 
	    {
	      "answer": "Brazil", 
	      "category": 6, 
	      "difficulty": 3, 
	      "id": 10, 
	      "question": "Which is the only team to play in every soccer World Cup tournament?"
	    }, 
	    {
	      "answer": "Uruguay", 
	      "category": 6, 
	      "difficulty": 4, 
	      "id": 11, 
	      "question": "Which country won the first ever soccer World Cup in 1930?"
	    }, 
	    {
	      "answer": "George Washington Carver", 
	      "category": 4, 
	      "difficulty": 2, 
	      "id": 12, 
	      "question": "Who invented Peanut Butter?"
	    }, 
	    {
	      "answer": "Lake Victoria", 
	      "category": 3, 
	      "difficulty": 2, 
	      "id": 13, 
	      "question": "What is the largest lake in Africa?"
	    }, 
	    {
	      "answer": "The Palace of Versailles", 
	      "category": 3, 
	      "difficulty": 3, 
	      "id": 14, 
	      "question": "In which royal palace would you find the Hall of Mirrors?"
	    }, 
	    {
	      "answer": "Agra", 
	      "category": 3, 
	      "difficulty": 2, 
	      "id": 15, 
	      "question": "The Taj Mahal is located in which Indian city?"
	    }, 
	    {
	      "answer": "Escher", 
	      "category": 2, 
	      "difficulty": 1, 
	      "id": 16, 
	      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
	    }
	  ], 
	  "success": true, 
	  "total_questions": 18
	}


##### DELETE /questions/<int:id>

* General:
  * Deletes a question by id using url parameter.
  * Returns id of deleted question upon success.
* Sample: `curl http://127.0.0.1:5000/questions/6 -X DELETE`

        {
            "deleted_id": 6, 
            "success": true
        }

##### POST /questions

* General:
  * Creates a new question using JSON request parameters.
  * Returns JSON object with the created question ID.
  * The new question is shown on the last page.
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            "question": "Which US state contains an area known as the Upper Penninsula?",
            "answer": "Michigan",
            "difficulty": 3,
            "category": "3"
        }'`

        {
	  "created_id": 28, 
	  "success": true
	}

##### POST /questions/search

* General:
  * Searches for questions using search term in JSON request parameters.
  * Returns JSON object with paginated matching questions.
* Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "who"}'

	{
	  "questions": [
	    {
	      "answer": "George Washington Carver", 
	      "category": 4, 
	      "difficulty": 2, 
	      "id": 12, 
	      "question": "Who invented Peanut Butter?"
	    }, 
	    {
	      "answer": "Alexander Fleming", 
	      "category": 1, 
	      "difficulty": 3, 
	      "id": 21, 
	      "question": "Who discovered penicillin?"
	    }
	  ], 
	  "success": true, 
	  "total_questions": 2
	}


##### GET /categories/<int:id>/questions

* General:
  * Gets questions by category id using url parameters.
  * Returns JSON object with paginated matching questions.
  * The "ALL" questions is always given an id of "0".
* Sample: `curl http://127.0.0.1:5000/categories/6/questions`

	{
	  "questions": [
	    {
	      "answer": "Brazil", 
	      "category": 6, 
	      "difficulty": 3, 
	      "id": 10, 
	      "question": "Which is the only team to play in every soccer World Cup tournament?"
	    }, 
	    {
	      "answer": "Uruguay", 
	      "category": 6, 
	      "difficulty": 4, 
	      "id": 11, 
	      "question": "Which country won the first ever soccer World Cup in 1930?"
	    }
	  ], 
	  "success": true, 
	  "total_questions": 2
	}


##### POST /quizzes

* General:
  * Users can play the game using this endpoint.
  * Uses JSON request parameters of category and previous questions.
  * Returns JSON object with random question while omitting previous questions.
* Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21], "quiz_category": {"type": "Science", "id": "1"}}'`

        {
            "question": {
                "answer": "Blood", 
                "category": 1, 
                "difficulty": 4, 
                "id": 22, 
                "question": "Hematology is a branch of medicine involving the study of what?"
            }, 
            "success": true
        }

### Acknowledgment
All the frontend and the project files except the API (`__init__.py in flaskr directory`) and the test cases (`test_flaskr.py`) were created by Udacity team as a project template for AdvancedWeb Devlopment Nanodegree.

The mentioned two files above and the API reference in this section was created by me, "Omar Yehia", a passionate web developer.

