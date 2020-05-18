import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


from auth import AuthError, requires_auth
from models import setup_db, create_all, Actor, Movie

ELEMENTS_PER_PAGE = 10


def get_elements_paginated(elements, page):
	start = (page - 1) * ELEMENTS_PER_PAGE
	end = start + ELEMENTS_PER_PAGE
	formatted_elements = [element.format() for element in elements]

	return formatted_elements[start:end]

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)
	CORS(app)
	setup_db(app)
	create_all()

	@app.after_request
	def after_request(response):
		response.headers.add('Access-Controll-Allow-Headers', 'Content-Type, Authorization, true')
		response.headers.add('Access-Controll-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')

		return response

	@app.route('/actors')
	@requires_auth('get:actors')
	def get_actors():
		all_actors = Actor.query.order_by('id').all()
		page = request.args.get('page', 1, int)
		selected_actors = get_elements_paginated(all_actors, page)

		if len(selected_actors) == 0:
			abort(404)

		return jsonify({
			'total_actors': len(selected_actors),
			'actors': selected_actors,
			'success': True
		})

	@app.route('/actors', methods=['POST'])
	@requires_auth('post:actors')
	def create_actor():
		body = request.get_json()

		try:
			actor = Actor(body['name'],
						body['age'],
						body['gender'])

			actor.insert()

			return jsonify({
				'success': True,
				'created': actor.id
			})

		except:
			print(sys.exc_info())
			abort(422)

	@app.route('/actors/<id>', methods=['DELETE'])
	@requires_auth('delete:actors')
	def delete_actor(id):
		actor = Actor.query.filter_by(id=id).one_or_none()

		if not actor:
			abort(404)

		try:
			actor.delete()

			return jsonify({
				'deleted': id,
				'success': True
			})

		except:
			abort(422)

	@app.route('/actors/<id>', methods=['PATCH'])
	@requires_auth('patch:actors')
	def edit_actor(id):
		actor = Actor.query.filter_by(id=id).one_or_none()

		if not actor:
			abort(404)

		try:
			body = request.get_json()
			print(body)
			age = body.get('age')
			name = body.get('name')
			gender = body.get('gender')
			if age:
				actor.age = age
			if name:
				actor.name = name
			if gender:
				actor.gender = gender

			actor.update()

			return jsonify({
				'success': True,
				'edited': id
			})

		except:
			print(sys.exc_info())
			abort(422)

	@app.route('/movies')
	@requires_auth('get:movies')
	def get_movies():
		all_movies = Movie.query.order_by('id').all()
		page = request.args.get('page', 1, int)
		selected_movies = get_elements_paginated(all_movies, page)

		if len(selected_movies) == 0:
			abort(404)

		return jsonify({
			'total_movies': len(selected_movies),
			'movies': selected_movies,
			'success': True
		})

	@app.route('/movies', methods=['POST'])
	@requires_auth('post:movies')
	def create_movie():
		body = request.get_json()

		try:
			movie = Movie(body['title'],
						body['release_date'])

			movie.insert()

			return jsonify({
				'success': True,
				'created': movie.id
			})

		except:
			print(sys.exc_info())
			abort(422)

	@app.route('/movies/<id>', methods=['DELETE'])
	@requires_auth('delete:movies')
	def delete_movie(id):
		movie = Movie.query.filter_by(id=id).one_or_none()

		if not movie:
			abort(404)

		try:
			movie.delete()

			return jsonify({
				'deleted': id,
				'success': True
			})

		except:
			abort(422)

	@app.route('/movies/<id>', methods=['PATCH'])
	@requires_auth('patch:movies')
	def edit_movie(id):
		movie = Movie.query.filter_by(id=id).one_or_none()

		if not movie:
			abort(404)

		try:
			body = request.get_json()
			title = body.get('title')
			release_date = body.get('release_date')
			if title:
				movie.title = title
			if release_date:
				movie.release_date = release_date

			movie.update()

			return jsonify({
				'success': True,
				'edited': id
			})

		except:
			print(sys.exc_info())
			abort(422)

	@app.errorhandler(422)
	def unprocessable(error):
	    return jsonify({
	        'success': False,
	        'error': 422,
	        'message': 'unprocessable'
	    }), 422


	@app.errorhandler(404)
	def not_found(error):
	    return jsonify({
	        'success': False,
	        'error': 404,
	        'message': 'resource not found'
	    }), 404


	@app.errorhandler(405)
	def not_allowed(error):
	    return jsonify({
	        'success': False,
	        'error': 405,
	        'message': 'method not allowed'
	    }), 405


	@app.errorhandler(401)
	def unauthorized(error):
	    return jsonify({
	        'success': False,
	        'error': 401,
	        'message': 'unauthorized'
	    }), 401


	@app.errorhandler(500)
	def internal_server_error(error):
	    return jsonify({
	        'success': False,
	        'error': 500,
	        'message': 'internal server error'
	    }), 500

	@app.errorhandler(AuthError)
	def auth_error(auth_res):
	    return jsonify({
	        'success': False,
	        'error': auth_res.error['code'],
	        'message': auth_res.error['description']
	    }), auth_res.status_code

	return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
