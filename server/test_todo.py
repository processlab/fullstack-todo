import unittest
import os
import json
from app import create_app, db, models

class TodoTestCase(unittest.TestCase):
    '''This class represents the todo test case'''

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.todo = {'text': 'React'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
            # add a todolist
            todo_list = models.TodoList()
            db.session.add(todo_list)
            db.session.commit()

    def test_todo_creation(self):
        '''Test API can create a todo. (POST request)'''
        res = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(res.status_code, 201)
        self.assertIn('React', str(res.data))

    def test_api_can_get_all_todo(self):
        '''Test API can get all existing todos. (GET request)'''
        res = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(res.status_code, 201)

        res = self.client().get('/api/v1/todo/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('React', str(res.data))
        self.assertIn('"position": 0', str(res.data))

    def test_api_can_change_status(self):
        '''Test API can change the status of an existing todo. (PUT request)'''
        res = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(res.status_code, 201)

        res2 = self.client().put('/api/v1/todo/1')
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.status_code, 200)

    def test_api_can_change_status_for_all_todos(self):
        '''Test API can change the status of all todos. (PUT request)'''
        rv = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(rv.status_code, 201)
        rv2 = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(rv2.status_code, 201)

        res = self.client().put('/api/v1/todo/complete')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn("active", str(res.data))

    def test_todo_can_be_reordered(self):
        '''Test API can reorder an existing todo. (PUT request)'''
        rv = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(rv.status_code, 201)
        rv2 = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(rv2.status_code, 201)

        rv3 = self.client().put(
            '/api/v1/todo/1/reorder',
            data={'new_position': 1}
        )
        self.assertEqual(rv3.status_code, 200)
        result = json.loads(str(rv3.data.decode('UTF-8')))
        self.assertEqual(1, result[1]['id'])

    def test_todo_can_be_reordered_to_zero(self):
        '''Test API can reorder an existing todo. (PUT request)'''
        rv = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(rv.status_code, 201)
        rv2 = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(rv2.status_code, 201)

        rv3 = self.client().put(
            '/api/v1/todo/2/reorder',
            data={'new_position': 0}
        )
        self.assertEqual(rv3.status_code, 200)
        result = json.loads(str(rv3.data.decode('UTF-8')))
        self.assertEqual(2, result[0]['id'])

    def test_todo_can_be_reordered_to_negative_value(self):
        '''Test API can reorder an existing todo. (PUT request)'''
        rv = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(rv.status_code, 201)
        rv2 = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(rv2.status_code, 201)

        rv3 = self.client().put(
            '/api/v1/todo/2/reorder',
            data={'new_position': -23}
        )
        self.assertEqual(rv3.status_code, 200)
        result = json.loads(str(rv3.data.decode('UTF-8')))
        self.assertEqual(2, result[0]['id'])

    def test_todo_can_be_reordered_to_index_out_of_range(self):
        '''Test API can reorder an existing todo. (PUT request)'''
        rv = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(rv.status_code, 201)
        rv2 = self.client().post('/api/v1/todo/', data=self.todo)
        self.assertEqual(rv2.status_code, 201)

        rv3 = self.client().put(
            '/api/v1/todo/2/reorder',
            data={'new_position': 23}
        )
        self.assertEqual(rv3.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
