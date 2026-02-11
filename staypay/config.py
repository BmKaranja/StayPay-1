import os


class Config:
    # SQLAlchemy Connection String: mysql+connector://user:password@host/dbname
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/staypay_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = 'staypay-secret-group-key'
    #placeholder key
    PAYSTACK_SECRET_KEY = 'sk_test_NITAWATUMIA SECRET KEY'