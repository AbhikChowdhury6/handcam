import os


class Config:
    SECRET_KEY = "new_secret_key"
    SQLALCHEMY_DATABASE_URI = 'postgresql:///handcam'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # email = ""
    # password = ""
    # MAIL_USERNAME = email
    # MAIL_PASSWORD = password
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
