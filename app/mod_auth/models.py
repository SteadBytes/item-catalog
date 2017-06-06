from app import db_session
from app import Base
import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=True)
    avatar = Column(String(200))
    tokens = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    authenticated = Column(Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated (i.e when logged in)."""
        return self.authenticated

    def is_anonymous(self):
        """False, anonymous users aren't supported, required for Flask-Login."""
        return False
