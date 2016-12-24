#!/usr/bin/env python
# coding=utf-8
# base.py

import os
import ConfigParser
import functools
import logging
import json
import urllib
import tornado.web
import tornado.gen
import tornado.httpclient
import json
from BuizModel.UserBuizModel import UserBuizModel 
from BuizModel.FaceSetBuizModel import FaceSetBuizModel
class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        para = {} 
        para['mongodb'] = self.application.mongodb 
        self.session = self.application.sqldb() 
        para['sqlsession'] = self.session
        para['facepp'] = self.application.facepp
        para['ali_service'] = self.application.ali_service
        para['ali_bucket'] = self.application.ali_bucket
        self._user_model = UserBuizModel(**para) 
        self._face_model = FaceSetBuizModel(**para)

    @property
    def user_model(self):
        return self._user_model

    @property
    def face_model(self):
        return self._face_model

    def __del__(self):
        self.session.close()

    def return_to_client(self,return_struct):
        temp_json = json.dumps({'code':return_struct.code,
            'message':return_struct.message,
            'data':return_struct.data})
        temp_json.replace("null", "\'empty\'")
        self.write(temp_json)