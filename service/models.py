"""
Models for Account Microservice
This module defines the database models and operations for Customer Accounts.
"""
import logging
from datetime import datetime
from service import db

logger = logging.getLogger("flask.app")

class DataValidationError(Exception):
    """Used for database data validation errors"""
    pass

class Account(db.Model):
    """
    Class that represents a Customer Account
    """
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    address = db.Column(db.String(256), nullable=True)
    phone_number = db.Column(db.String(32), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def create(self):
        """Creates an Account in the database"""
        logger.info(f"Creating account for: {self.name}")
        if not self.name or not self.email:
            raise DataValidationError("Name and Email are required fields.")
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates an Account in the database"""
        logger.info(f"Updating account: {self.name}")
        if not self.name or not self.email:
            raise DataValidationError("Name and Email are required fields.")
        db.session.commit()

    def delete(self):
        """Removes an Account from the database"""
        logger.info(f"Deleting account: {self.name}")
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes an Account into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def deserialize(self, data):
        """Deserializes an Account from a dictionary"""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data.get("address")
            self.phone_number = data.get("phone_number")
        except KeyError as error:
            raise DataValidationError(f"Invalid Account data: missing {error.args[0]}")
        except TypeError as error:
            raise DataValidationError(f"Invalid Account data: body was bad or invalid: {error}")
        return self

    @classmethod
    def all(cls):
        """Returns all Accounts in the database"""
        logger.info("Retrieving all accounts")
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        """Finds an Account by its ID"""
        logger.info(f"Finding account by id: {account_id}")
        return cls.query.get(account_id)
