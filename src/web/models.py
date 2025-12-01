"""Database models for the warehouse application."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Warehouse(db.Model):  # pylint: disable=too-few-public-methods
    """Model representing a warehouse."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    items = db.relationship(
        'Item', backref='warehouse', cascade='all, delete-orphan'
    )


class Item(db.Model):  # pylint: disable=too-few-public-methods
    """Model representing an item in a warehouse."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey('warehouse.id'), nullable=False
    )
