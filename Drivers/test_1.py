# -- coding: utf-8 --
from __future__ import unicode_literals
import sqlalchemy as db


class FirstConfig(__):
    __bind_key__ = 'app'

    EXTERNAL_GSM_ANT = 'EXTERNAL_GSM_ANT'
    INTERNAL_GSM_ANT = 'INTERNAL_GSM_ANT'
    UNKNOWN_GSM_ANT = 'UNKNOWN_GSM_ANT'

    DEFAULT_APN = ''
    DEFAULT_BALANCE_NUMBER = ''

    __tablename__ = 'GsmConfig'
    id = db.Column(db.Integer, primary_key=True)
    balance_number = db.Column(db.String(64), unique=False)
    apn = db.Column(db.String(128), unique=True)
    antenna = db.Column(db.String(128), unique=True)
    has_external_antenna = db.Column(db.Boolean, default=False)