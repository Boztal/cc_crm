from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ---------------- USER ----------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


# ---------------- OPERATIONS ----------------
class Operation(db.Model):
    __tablename__ = "operations"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    op_type = db.Column(db.String(50), nullable=False)  # income / expense
    description = db.Column(db.String(255))
    date = db.Column(db.String(50))
    user = db.Column(db.String(100), nullable=False)