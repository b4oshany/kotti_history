# -*- coding: utf-8 -*-

"""
Created on 2017-01-03
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from datetime import datetime
from kotti import Base, DBSession
from kotti.interfaces import IDefaultWorkflow
from sqlalchemy import (
    Column, ForeignKey, Integer, Unicode,
    Float, Boolean, Date, DateTime, String
)
from zope.interface import implements

from kotti_history import _


class SearchHistory(Base):

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(ForeignKey('principals.id',
                                onupdate="CASCADE",
                                ondelete="CASCADE"),
                     primary_key=True)
    term = Column(String, nullable=False)
    date_last_viewed = Column(DateTime, default=datetime.today())

    @classmethod
    def create(cls, user_id, term):
        sh = cls(user_id=user_id, term=term)
        DBSession.add(sh)

    @classmethod
    def find_by_user(cls, user_id, query=None):
        if not query:
            query = cls.query
        return query.filter(
            cls.user_id == user_id
        )

    @classmethod
    def find_by_term(cls, term, query=None):
        if not query:
            query = cls.query
        return query.filter(
            cls.term == term
        )


class ViewHistory(Base):
    """ A custom content type. """

    implements(IDefaultWorkflow)

    id = Column(ForeignKey('contents.id',
                           onupdate="CASCADE",
                           ondelete="CASCADE"),
                primary_key=True)
    user_id = Column(ForeignKey('principals.id',
                                onupdate="CASCADE",
                                ondelete="CASCADE"),
                     primary_key=True)
    content_type = Column(String, nullable=False)
    num_views = Column(Integer, default=1)
    date_last_viewed = Column(DateTime, default=datetime.today())

    @classmethod
    def create(cls, content, user):
        history = cls(
            user_id=user.id,
            content_type=cls.__class__.__name__,
            id=content.id
        )
        DBSession.add(history)

    @classmethod
    def find_by_content_id(cls, id, query=None):
        if not query:
            query = cls.query
        return query.filter(
                cls.id == id
            )

    @classmethod
    def find_by_user(cls, user_id, query=None):
        if not query:
            query = cls.query
        return query.filter(
            cls.user_id == user_id
        )

    @classmethod
    def find(cls, content_id=None, user_id=None):
        query = cls.query
        if content_id:
            query = cls.find_by_content_id(content_id)
        if user_id:
            query = cls.find_by_user_id(user_id)
        return query

