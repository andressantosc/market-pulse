from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from db_init import User, Base, Companies
 
engine = create_engine('sqlite:///./test2.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

firstuser = User("ANDRES", "asantos")
session.add(firstuser)
session.commit()

firstcompany = Companies("Apple", "AAPL", firstuser)
session.add(firstcompany)
session.commit()


