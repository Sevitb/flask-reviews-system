import datetime
from reviews_system_app import db, login_manager
from flask_login import (LoginManager, UserMixin, login_required,
			  login_user, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100),unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    
    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password_hash, password)

class Materials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.Text, nullable=False)
    reviews = db.relationship('Reviews', backref='material')

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    reviewer_information = db.Column(db.String(500), nullable=False)
    fits_theme = db.Column(db.String(255), nullable=False)
    justified = db.Column(db.String(255), nullable=False)
    goal_reached = db.Column(db.String(255), nullable=False)
    contribution_was_made = db.Column(db.String(255), nullable=False)
    relevance_of_sources = db.Column(db.String(255), nullable=False)
    into_methodology = db.Column(db.String(255), nullable=False)
    results_are_interpreted = db.Column(db.String(255), nullable=False)
    presentation_of_text = db.Column(db.String(255), nullable=False)
    presence_of_graphics = db.Column(db.String(255), nullable=False)
    comment_for_author = db.Column(db.Text, default=False, nullable=False)
    comment_for_editor = db.Column(db.Text, default=False, nullable=False)
    result = db.Column(db.String(150), nullable=False)
    general_recommendations = db.Column(db.Text, default=False, nullable=False)
    created_at = db.Column(db.Text, default=False, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)