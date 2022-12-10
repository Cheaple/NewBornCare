import json

import flask_unittest
from app import create_app, db, models
from app.init_db import init_test_data

class TestApiCheck(flask_unittest.ClientTestCase):
    
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
        
    def test_check_add(self, client):
        """
        验证添加巡视记录
        """

        '''未登陆，检查返回值为失败'''
        data = {}
        response = client.post("/api/check/add", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        

        '''使用错误的信息进行添加，检查返回值为失败'''
        data = {
            "nurseId": 1,
        }
        response = client.post(
            "/api/check/add",
            json=data,
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)


        '''使用正确的信息进行添加，检查返回值为成功'''
        data = {
            "nurseId": 1,
            "patientId": 2,
            "transfusionId": 2,
            "info": "一切正常"
        }
        response = client.post(
            "/api/check/add",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)



    def test_check_update(self, client):
        """
        验证修改巡视记录
        """

        '''未登陆，检查返回值为失败'''
        data = {}
        response = client.patch("/api/check/update/1", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        
        '''使用错误的信息进行更新，检查返回值为失败'''
        data = {
            "time": "11:20",
        }
        response = client.patch(
            "/api/check/update/1",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

        '''使用正确的信息进行更新，检查返回值为成功'''
        data = {
            "info": "体温过高",
        }
        response = client.patch(
            "/api/check/update/1",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)