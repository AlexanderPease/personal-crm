from app.models import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String())
    thread_id = db.Column(db.String())



    def __repr__(self):
        return '<Message {}>'.format(self.id)
