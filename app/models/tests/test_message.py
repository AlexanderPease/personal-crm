import requests
import os
import time
from nose.tools import assert_equals

from app import app
from app.config import TestConfig
from app.models import db
from app.models.message import Message, EmailAddress


class TestMessage:

    @classmethod
    def setup_class(cls):
        os.environ['NOSE_TESTS'] = 'true'  # not being set...

    def setup(self):
        # Not correctly setting env variables, or at least __init__ isn't seeing it...
        # os.environ['NOSE_TESTS'] = 'true'
        
        self.app = app.test_client()
        
        # ...hack around config
        self.app.application.config.from_object(TestConfig)
        
        with self.app.application.app_context():
            db.create_all()

    def teardown(self):
        with self.app.application.app_context():
            db.drop_all()
        

    def test_flask(self):
        result = self.app.get('/')
        assert_equals(result.status_code, 200)

    def test_init(self):
        print('test_init')

        message = Message(thread_id=1)
        assert_equals(message.thread_id, 1)
        print(self.app.application.config)
        print(self.app.application)
        print(self.app.application.app_context)
        
        with self.app.application.app_context():
            db.session.add(message)
            db.session.commit()
            assert_equals(
                len(Message.query.all()), 1
            )
