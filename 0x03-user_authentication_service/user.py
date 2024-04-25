#!/usr/bin/env python3
""""
Module 1: Create a class that creates a db table
"""
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer


class Base(DeclarativeBase):
    """
    Declarative base class
    """
    pass


class User(Base):
    """
    Declare a table called users
    """
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(250), nullable=False)
    hashed_password = mapped_column(String(250), nullable=False)
    session_id = mapped_column(String(250), nullable=True)
    reset_token = mapped_column(String(250), nullable=True)
