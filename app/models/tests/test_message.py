import requests
import os
import time
from nose.tools import assert_equals

from app import app
from app.models import db
from app.models.message import Message, EmailAddress


class TestMessage:

    @classmethod
    def setup_class(cls):
        # Gets non-.env config vars
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/crm-test'
        # print(app.config)
        

        with app.app_context():
            time.sleep(2)



    def setup(self):
        pass

    def test_init(self):
        message = Message(thread_id=1)
        assert_equals(message.thread_id, 1)
        
        db.session.add(message)
        db.session.commit()
        assert_equals(
            len(Message.query.all()), 1
        )
