from app.models import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    google_credentials = db.Column(db.JSON())

    # def __init__(self, name, author, published):
    #     self.name = name
    #     self.author = author
    #     self.published = published

    def __repr__(self):
        return '<User {}>'.format(self.email)

    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'author': self.author,
    #         'published': self.published
    #     }
