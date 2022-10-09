from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    artist = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(10), nullable=False)
    tempo = db.Column(db.Float, nullable=False)
    key = db.Column(db.String(10), nullable=False)
    signature = db.Column(db.String(5), nullable=False)
    image_url = db.Column(db.String(50))
    song_id = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {"id": self.id,
                "title": self.title,
                "artist": self.artist,
                "duration": self.duration,
                "tempo": self.tempo,
                "key": self.key,
                "signature": self.signature,
                "image_url": self.image_url,
                "song_id": self.song_id}