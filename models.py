from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Meeting(db.Model):
    """Store meeting analysis history"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    transcript = db.Column(db.Text, nullable=False)
    action_items = db.Column(db.Text)  # JSON array
    translated_text = db.Column(db.Text)
    summary = db.Column(db.Text)
    dialogue_text = db.Column(db.Text)
    audio_file_name = db.Column(db.String(255))
    target_lang = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Meeting {self.id}: {self.filename}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'transcript': self.transcript,
            'action_items': json.loads(self.action_items) if self.action_items else [],
            'translated_text': self.translated_text,
            'summary': self.summary,
            'dialogue_text': self.dialogue_text,
            'audio_file_name': self.audio_file_name,
            'target_lang': self.target_lang,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
