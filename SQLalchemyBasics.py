from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///test.db", echo=True)

conn = engine.connect()

conn.execute(text("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"))

conn.commit()

from sqlalchemy.orm import Session

session = Session(engine)

session.execute(text("INSERT INTO users (name, age) VALUES (:name, :age)"), [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}])

session.commit()

