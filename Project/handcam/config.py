import os


class Config:
    SECRET_KEY = "dasdasdsadasds"
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/handcam'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # email = "alukaraj2894@gmail.com"
    # password = ""
    # MAIL_USERNAME = email
    # MAIL_PASSWORD = password
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
