import logging
from service.models import Base, User

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

class DBApi:
    def __init__(self, url):
        self.url = self.get_valid_url(url)
        engine = create_engine(self.url)
        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        self.session = Session()

    def get_valid_url(self, url):
        if 'postgres' in url:
            return 'postgresql+psycopg2://' + url.split('://')[-1]
        return url

    def get_user(self, email):
        user = self.session.query(User)\
                        .filter_by(email=email)\
                        .first()
        logging.info(user)
        return user

    def set_new_counters(self, user, unread, new):
        user.unread, user.new = unread, new
        db.session.commit()
        logging.info("Setting new counters")

    def create_user(self, email, unread, new):
        user = User(email=email, unread=unread, new=new)
        self.session.add(user)
        self.session.commit()
        return user

if __name__ == '__main__':
    db = DBApi()
    for l in db.get_all_letters():
        print(l)