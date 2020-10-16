# Full Stack API Project

## Full Stack Trivia

Trivia is a full stack web application that allows users to test their knowlege by playing quizzes of questions of various categories, as well as allowing them to control the content of these quizzes by adding and removing questions.

## Installation

### Database Setup
In order to setup the database, we'll use the ```trivia.psql``` file provided within the backend directory files to set up our database named <b>trivia</b>:<br>
```
createdb trivia
psql -U postgres -f trivia.psql trivia
```

### Backend
To get started navigate to the backend directory by running the command ```cd backend``` and then:
1. Install dependencies ```pip install -r requirements.txt```
2. Set up the app ```export FLASK_APP=flaskr```
3. Set up the development environment ```export FLASK_ENV=development```
4. Start the backend server by typing ```flask run```

### Frontend
In another terminal, navigate to the frontend directory ```cd frontend``` followed by ```npm install``` or ```npm i``` to install the dependecies and finally start the server by using the command ```npm start```

## Features
The app enables users to do the following:
* Display Questions: either by showing them the full list of questions or filtering questions by category
* Add new Questions
* Delete Questions
* Search for Questions
* Play the quiz game, either by choosing a specefic category or getting random questions from any category


## API Reference
### Getting Started
Base URL: http://127.0.0.1:5000/

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
   "success":False,
   "code":404,
   "message":"the requested resource was not found"
}
```
The API will return 5 error types:
* 400: Bad request
* 404: Not found
* 405: Method not allowed
* 422: Unprocessable entity
* 500: Internal Server Error

### Endpoints

#### GET /categories
* General: Returns a list of category objects and a success value
* Sample:
curl http://127.0.0.1:5000/categories

```
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
```

#### GET /questions
* General: Returns a list of question objects, success value, a list of categories objects and the total number of questions
* Sample:
curl http://127.0.0.1:5000/questions

```
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
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
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
    }
  ],
  "success": true,
  "total_questions": 28
}
```

#### POST /questions
* General: Returns the newly created question along with a success value
* Sample:
```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type:application/json" -d '{"question":"What are the cutest felines on earth?", "answer":"Cats","category":1,"difficulty":2}' ```
```
  "question": {
    "answer": "Cats",
    "category": 1,
    "difficulty": 2,
    "id": 52,
    "question": "What are the cutest felines on earth?"
  },
  "success": true
}
```

## Testing
To run the tests, run the following commands:
```
dropdb trivia_test
createdb trivia_test
psql -U postgres -f trivia.psql trivia_test
python test_flaskr.py
```
