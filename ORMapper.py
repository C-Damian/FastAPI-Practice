from sqlalchemy import Boolean, create_engine, Integer, String, Float, Column, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/tutorialdb", echo=True)

Base = declarative_base()

class Person(Base):
  __tablename__ = "people"
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  age = Column(Integer)

  belongings = relationship("Belonging", back_populates="person")

class Belonging(Base):
  __tablename__ = "belongings"
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  price = Column(Integer, nullable=False)
  owner_id = Column(Integer, ForeignKey("people.id"))

  person = relationship("Person", back_populates="belongings")

class Pet(Base):
  __tablename__ = "pets"
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  is_dog = Column(Boolean, nullable=False)
  owner_id = Column(Integer, ForeignKey("people.id"))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#result = session.query(Person).filter(Person.name == "Manuel Gomez").update({'name': 'Damian Torres'})
result = session.query(Belonging.owner_id, func.sum(Belonging.price)).group_by(Belonging.owner_id).having(func.sum(Belonging.price) < 200)

print(result.all())

#new_person = Person(name='Kanuel Gomez', age=33)
#session.add(new_person)
#session.flush()

#new_belonging = Belonging(name = "Captop", price = 200, owner_id = new_person.id)
#session.add(new_belonging)
#session.commit()

#print([t.name for t in new_person.belongings])
#print(new_belonging.person.name)