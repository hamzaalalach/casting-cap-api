import unittest
import json
import os
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


def get_last_element_id(element):
    elements = element.query.order_by('id').all()

    return str(elements[len(elements) - 1].format()['id'])


def get_auth_header(token_for):
    return {'Authorization': 'Bearer ' + os.environ.get(token_for)}


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://postgres:0000@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_actor = {
            'name': 'Kevin Darnell Hart',
            'age': 40,
            'gender': 'Male'
        }

        self.new_movie = {
            'title': 'The Hobbit: The Battle of the Five Armies',
            'release_date': '1 December 2014'
        }

    def tearDown(self):
        pass

    def test_get_actors_200(self):
        res = self.client().get('/actors',
                                headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])
        self.assertEqual(data['total_actors'], 1)
        self.assertTrue(data['success'])

    def test_get_actors_404(self):
        res = self.client().get('/actors?page=1000',
                                headers=get_auth_header('PRODUCER'))

        self.assertEqual(res.status_code, 404)

    def test_post_actors_200(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)
        last_id = get_last_element_id(Actor)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], int(last_id))

    def test_post_actors_422(self):
        res = self.client().post('/actors', json={},
                                 headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_patch_actors_200(self):
        last_id = get_last_element_id(Actor)
        res = self.client().patch(
            '/actors/' + last_id,
            json={
                'age': 67},
            headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)
        actor = Actor.query.get(last_id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(actor.age, 67)
        self.assertTrue(data['success'])
        self.assertEqual(data['edited'], last_id)

    def test_patch_actors_404(self):
        res = self.client().patch('/actors/1000',
                                  headers=get_auth_header('PRODUCER'))

        self.assertEqual(res.status_code, 404)

    def test_delete_actors_200(self):
        last_id = get_last_element_id(Actor)
        res = self.client().delete(
            '/actors/' + last_id,
            headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)
        actor = Actor.query.filter_by(id=last_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], last_id)
        self.assertTrue(data['success'])
        self.assertIsNone(actor)

    def test_delete_actors_404(self):
        res = self.client().delete('/actors/1000',
                                   headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_movies_200(self):
        res = self.client().get('/movies',
                                headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])
        self.assertEqual(data['total_movies'], 1)
        self.assertTrue(data['success'])

    def test_get_movies_404(self):
        res = self.client().get('/movies?page=1000',
                                headers=get_auth_header('PRODUCER'))

        self.assertEqual(res.status_code, 404)

    def test_post_movies_200(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)
        last_id = get_last_element_id(Movie)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], int(last_id))

    def test_post_movies_422(self):
        res = self.client().post('/movies', json={},
                                 headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_patch_movies_200(self):
        last_id = get_last_element_id(Movie)
        res = self.client().patch(
            '/movies/' + last_id,
            json={
                'release_date': '30 December 2018'},
            headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)
        movie = Movie.query.get(last_id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(movie.release_date, '30 December 2018')
        self.assertTrue(data['success'])
        self.assertEqual(data['edited'], last_id)

    def test_patch_movies_404(self):
        res = self.client().patch('/movies/1000',
                                  headers=get_auth_header('PRODUCER'))

        self.assertEqual(res.status_code, 404)

    def test_delete_movies_200(self):
        last_id = get_last_element_id(Movie)
        res = self.client().delete(
            '/movies/' + last_id,
            headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)
        movie = Movie.query.filter_by(id=last_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], last_id)
        self.assertTrue(data['success'])
        self.assertIsNone(movie)

    def test_delete_movies_404(self):
        res = self.client().delete('/movies/1000',
                                   headers=get_auth_header('PRODUCER'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_missing_auth_header_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['error'], 'authorization_header_missing')

    def test_wrong_bearer_token_401(self):
        res = self.client().get(
            '/actors',
            headers={
                'Authorization': 'Bearer somewrongtoken'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_assistant_get_movies_200(self):
        res = self.client().get('/movies',
                                headers=get_auth_header('ASSISTANT'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])
        self.assertTrue(data['success'])

    def test_assistant_delete_movies_403(self):
        res = self.client().delete('/movies/1000',
                                   headers=get_auth_header('ASSISTANT'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_director_patch_movies_200(self):
        last_id = get_last_element_id(Movie)
        res = self.client().patch(
            '/movies/' + last_id,
            json={
                'release_date': '30 December 2050'},
            headers=get_auth_header('DIRECTOR'))
        data = json.loads(res.data)
        movie = Movie.query.get(last_id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(movie.release_date, '30 December 2050')
        self.assertTrue(data['success'])


if __name__ == "__main__":
    unittest.main()
