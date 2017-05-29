from db_init import User, Base, Companies
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///./test2.db')
Base.metadata.bind = engine


DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

session.query(User).all()

person = session.query(User).first()
person.username
session.query(Companies).filter(Companies.user == person).all()
session.query(Companies).filter(Companies.user == person).one()
company = session.query(Companies).filter(Companies.user == person).one()
print(company.ticker)