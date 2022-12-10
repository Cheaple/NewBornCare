import json

import flask_unittest
from app import create_app, db, models
from app.init_db import init_test_data

class TestApiTransfusion(flask_unittest.ClientTestCase):
    
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
        
    def test_transfusion_add(self, client):
        """
        验证添加输液记录
        """

        '''未登陆，检查返回值为失败'''
        data = {}
        response = client.post("/api/transfusion/add", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        

        '''使用错误的信息进行注册，检查返回值为失败'''
        data = {
            "nurseId": 1,
            "patientId": 1,
            "name": "输液治疗",
            "vein": 1,
            "tool": 1,
            "drug": [{
                "drug": "葡萄糖",
                "seq": 1,
                "dose": 500,    
                "rate": 3
                }
            ]
        }
        response = client.post(
            "/api/transfusion/add",
            json=data,
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)


        '''使用正确的信息进行注册，检查返回值为成功'''
        data = {
            "nurseId": 1,
            "patientId": 1,
            "name": "输液治疗",
            "vein": 1,
            "tool": 1,
            "drug": [{
                "drug": 3,
                "seq": 1,
                "dose": 500,    
                "rate": 3
                }
            ]
        }
        response = client.post(
            "/api/transfusion/add",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)



    def test_transfusion_update(self, client):
        """
        验证修改输液记录
        """

        '''未登陆，检查返回值为失败'''
        data = {}
        response = client.patch("/api/transfusion/update/1", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        
        '''使用错误的信息进行更新，检查返回值为失败'''
        data = {
            "status": "中止",
        }
        response = client.patch(
            "/api/transfusion/update/1",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

        '''使用正确的信息进行更新，检查返回值为成功'''
        data = {
            "status": -1,
        }
        response = client.patch(
            "/api/transfusion/update/1",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_transfusion_next(self, client):
        """
        验证输液换药
        """

        '''未登陆，检查返回值为失败'''
        data = {}
        response = client.patch("/api/transfusion/update/1", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        
        '''换药，检查返回值为成功'''
        response = client.patch(
            "/api/transfusion/update/1/next",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_transfusion_finish(self, client):
        """
        验证输液完成
        """

        '''未登陆，检查返回值为失败'''
        data = {}
        response = client.patch("/api/transfusion/update/1", json=data)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        
        '''未到最后一个药品，无法完成输液，检查返回值为失败'''
        response = client.patch(
            "/api/transfusion/update/1/finish",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)

        '''完成输液，检查返回值为失败'''
        response = client.patch(
            "/api/transfusion/update/1/next",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        response = client.patch(
            "/api/transfusion/update/1/finish",
            json=data, 
            headers={"Authorization": self.jwt}
        )
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


