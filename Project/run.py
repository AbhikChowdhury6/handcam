from handcam.app import create_app
from flask_script import Manager

application = create_app()

if __name__ == '__main__':
    application.run(host='0.0.0.0')
