import json

import flask_unittest
from app import create_app, db, models
from app.init_db import init_test_data

class TestApiNurse(flask_unittest.ClientTestCase):
    
    app = create_app('test')
    jwt = None

    def setUp(self, client):
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        init_test_data()

        data = {"username": "nurse", "password": "nurse"}
        response = client.post("/api/nurse/login", json=data)
        json_data = json.loads(response.data)
        self.jwt = json_data["jwt"]

    def tearDown(self, client):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_nurse_login(self, client):
        """
        验证登陆
        """

        '''使用错误的信息进行登录，检查返回值为失败'''
        data = {"username": "nurse", "password": "wrong_pw"}
        response = client.post("/api/nurse/login", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)

        '''使用正确的信息进行登录，检查返回值为成功'''
        data = {"username": "nurse", "password": "nurse"}
        response = client.post("/api/nurse/login", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['name'], "测试护士")

    def test_nurse_logout(self, client):
        """
        验证登出
        """
        pass

    def test_nurse_add(self, client):
        """
        验证注册护士账户
        """

        '''未登陆，检查返回值为失败'''
        data = {}
        response = client.post("/api/nurse/add", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        

        '''使用错误的信息进行注册，检查返回值为失败'''
        data = {
            "username": "nurse1",
            "password": "nurse1",
            "name": "测试护士1号",
            "department": 1,
        }
        response = client.post(
            "/api/nurse/add",
            json=data,
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)


        '''使用正确的信息进行注册，检查返回值为成功'''
        data = {
            "username": "nurse1",
            "password": "Nurse100",
            "name": "测试护士一号",
            "tel": 19972640000,
        }
        response = client.post(
            "/api/nurse/add",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


        '''使用重复的用户名进行注册，检查返回值为失败'''
        data = {
            "username": "nurse1",
            "password": "Nurse100",
            "name": "测试护士一号",
            "tel": "19972640000",
        }
        response = client.post(
            "/api/nurse/add",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)


    def test_nurse_update(self, client):
        """
        验证更新护士信息
        """

        '''未登陆，检查返回值为失败'''
        data = {}
        response = client.patch("/api/nurse/update/1", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        
        '''使用错误的信息进行更新，检查返回值为失败'''
        data = {
            "name": "测试护士0号",
        }
        response = client.patch(
            "/api/nurse/update/1",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

        '''使用正确的信息进行更新，检查返回值为成功'''
        data = {
            "name": "测试护士零号",
        }
        response = client.patch(
            "/api/nurse/update/1",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


