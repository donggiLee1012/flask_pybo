from sqlalchemy import create_engine
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
db = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)