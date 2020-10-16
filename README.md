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
4. Start the server by typing ```flask run```

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




## Testing
To run the tests, run the following commands:
```
dropdb trivia_test
createdb trivia_test
psql -U postgres -f trivia.psql trivia_test
python test_flaskr.py
```
