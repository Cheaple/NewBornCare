import json

import flask_unittest
from app import create_app, db, models
from app.init_db import init_test_data

class TestApiAdmin(flask_unittest.ClientTestCase):
    
    app = create_app('test')
    jwt = None

    def setUp(self, client):
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        init_test_data()

        data = {"username": "admin", "password": "admin"}
        response = client.post("/api/admin/login", json=data)
        json_data = json.loads(response.data)
        self.jwt = json_data["jwt"]

    def tearDown(self, client):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_admin_login(self, client):
        """
        验证登陆
        """

        '''使用错误的信息进行登录，检查返回值为失败'''
        data = {"username": "admin", "password": "wrong_pw"}
        response = client.post("/api/admin/login", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)

        '''使用正确的信息进行登录，检查返回值为成功'''
        data = {"username": "admin", "password": "admin"}
        response = client.post("/api/admin/login", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['name'], "测试管理员")

    def test_admin_logout(self, client):
        """
        验证登出
        """
        pass

    def test_admin_add(self, client):
        """
        验证注册管理员账户
        """

        '''未登陆，检查返回值为失败'''
        data = {}
        response = client.post("/api/admin/add", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        

        '''使用错误的信息进行注册，检查返回值为失败'''
        data = {
            "username": "admin1",
            "password": "admin1",
            "name": "测试管理员1号",
            "department": 1,
        }
        response = client.post(
            "/api/admin/add",
            json=data,
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)


        '''使用正确的信息进行注册，检查返回值为成功'''
        data = {
            "username": "admin1",
            "password": "Administrator1",
            "name": "测试管理员一号",
        }
        response = client.post(
            "/api/admin/add",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


        '''使用重复的用户名进行注册，检查返回值为失败'''
        data = {
            "username": "admin1",
            "password": "Administrator1",
            "name": "测试管理员一号",
        }
        response = client.post(
            "/api/admin/add",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)


    def test_admin_update(self, client):
        """
        验证更新管理员信息
        """

        '''未登陆，检查返回值为失败'''
        data = {}
        response = client.patch("/api/admin/update/1", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        
        '''使用错误的信息进行更新，检查返回值为失败'''
        data = {
            "name": "测试管理员0号",
            "department": 0,
        }
        response = client.patch(
            "/api/admin/update/1",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

        '''使用正确的信息进行更新，检查返回值为成功'''
        data = {
            "name": "测试管理员零号",
            "department": 0,
        }
        response = client.patch(
            "/api/admin/update/1",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


