# Full Stack Trivia API Backend

## Notes
  - The Full Stack is built following the Casting Agency Specifications.
  - The following setup is for local use, otherwise the API is hosted at: [https://casting-cap-api.herokuapp.com](https://casting-cap-api.herokuapp.com)
  - For testing porpuses, I've included tokens for each role in setup.sh and in Heroku config vars, instructions on how to login to the frontend is provided in the frontend README.me .

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment . This keeps your dependencies for each project separate and organaized.

```bash
pip install virtualenv
cd YOUR_PROJECT_DIRECTORY_PATH/
virtualenv env
source env/bin/activate
```
More instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [unittest](https://docs.python.org/3.8/library/unittest.html) Python testing framework.

#### Export config variables

To export the config variables run:
```bash
. setup.sh
```

Please note the . before setup.sh

#### Running the server

From within the `src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python app.py
```

The application by default runs in debug mode, on port 8080.

## Auth0 roles reference

#### Assistant

  - get:actors
  - get:movies

#### Director

  - get:actors
  - get:movies
  - delete:actors
  - patch:actors
  - patch:movies
  - post:actors

#### Producer

  - get:actors
  - get:movies
  - delete:actors
  - patch:actors
  - patch:movies
  - post:actors
  - post:movies
  - delete:movies
  

## API REFERENCE

### Endpoints

- GET '/movies?page={number}'
- POST '/movies'
- PATCH '/movies/{id}'
- DELETE '/movies/{id}'
- GET '/actors?page={number}'
- POST '/actors'
- PATCH '/actors/{id}'
- DELETE '/actors/{id}'


##### GET '/movies?page={number}'
- Fetches the available movies object paginated by 10, given a page number which is by default 1
- Request Arguments: None
- Response sample: 

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "28 November 2012",
      "title": "The Hobbit: An Unexpected Journey"
    },
    {
      "id": 2,
      "release_date": "2 December 2013",
      "title": "The Hobbit: The Desolation of Smaug"
    }
  ],
  "success": true,
  "total_movies": 2
}

```
##### POST '/movies'
- Creates a new movie.
- Request Arguments: Required
    - title: String
    - release_date: String
- Response sample: It returns the id of the newly created movie

```json
{
  "created": 3,
  "success": true
}
```

##### PATCH '/movies/{id}'
- Modifies an existing movie proving its id
- Request Arguments: Optional
    - title: String
    - release_date: String
- Response sample: It returns the id of the newly modified movie

```json
{
  "modified": 1,
  "success": true
}
```

##### DELETE '/movies/{id}'
- Removes an existing movie proving its id
- Request Arguments: None
- Response sample: It returns the id of the newly deleted movie

```json
{
  "deleted": 2,
  "success": true
}
```

##### GET '/actors?page={number}'
- Fetches the available actors paginated by 10, given a page number which is by default 1
- Request Arguments: None
- Response sample: 

```json
{
  "actors": [
    {
      "age": 66,
      "gender": "Male",
      "id": 1,
      "name": "Denzel Washington"
    },
    {
      "age": 46,
      "gender": "Female",
      "id": 2,
      "name": "Penelope Cruz"
    }
  ],
  "success": true,
  "total_actors": 2
}

```
##### POST '/actors'

- Creates a new actor.
- Request Arguments: Required
    - name: String
    - age: Integer
    - gender: String
- Response sample: It returns the id of the newly created actor

```json
{
  "created": 3,
  "success": true
}

```

##### PATCH '/actors/{id}'
- Modifies an existing actor proving its id
- Request Arguments: Optional
    - name: String
    - age: Integer
    - gender: String
- Response sample: It returns the id of the newly modified actor

```json
{
  "modified": 1,
  "success": true
}
```

##### DELETE '/actors/{id}'
- Removes an existing actor proving its id
- Request Arguments: None
- Response sample: It returns the id of the newly deleted actor

```json
{
  "deleted": 2,
  "success": true
}
```

## API ERROR CODES:

 - 422: unprocessable
 - 404: resource not found
 - 405: method not allowed
 - 401: unauthorized
 - 500: internal server error
 - 200: ok

## Testing
To run the tests, execute:

```
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone_test.psql
python test_app.py
```

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE) file for details.

## Author

Created by [Hamza Alalach](https://twitter.com/Hamzaalalach) as a UDACITY [capstone project](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)