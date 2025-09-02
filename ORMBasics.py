from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, ForeignKey, func


#engine = create_engine("sqlite:///test.db", echo=True)
#for local db
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/tutorialdb", echo=True)

conn = engine.connect()
meta = MetaData()

people = Table("people", meta,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("age", Integer)
)

pets = Table("pets", meta,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("is_Dog", Boolean, nullable=False),
        Column("owner_id", Integer, ForeignKey("people.id"))
)

belongings = Table("belongings", meta,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("price", Integer, nullable=False),
        Column("owner_id", Integer, ForeignKey("people.id"))
)
meta.create_all(engine)

#update_statement = people.update().where(people.c.id == 2).values(name="Johnnyy Doe", age=75)

#result = conn.execute(update_statement)

#delete_statement = people.delete().where(people.c.name == "mark Doe")

#result = conn.execute(delete_statement)

#conn.commit()
     
#insert_statement = belongings.insert().values([
#    {"name": "Watch", "price": 100, "owner_id": 3},
#    {"name": "Laptop", "price": 150, "owner_id": 2},
#    {"name": "Car", "price": 200, "owner_id": 6},
#    {"name": "Bike", "price": 100, "owner_id": 7},
#    {"name": "Cup", "price": 150, "owner_id": 8},
#    {"name": "Jewlery", "price": 100, "owner_id": 3},
#    {"name": "Chair", "price": 150, "owner_id": 2},
#    {"name": "Picture", "price": 200, "owner_id": 6},
#    {"name": "Books", "price": 100, "owner_id": 7},
#    {"name": "Clothes", "price": 150, "owner_id": 8}
#])

#result = conn.execute(insert_statement)
#conn.commit()

join_statement = people.join(pets, people.c.id == pets.c.owner_id)
select_statement = people.select().with_only_columns(people.c.name, pets.c.name, pets.c.is_Dog).select_from(join_statement)
result = conn.execute(select_statement)

for row in result.fetchall():
    print(row)

aggregate_statement = belongings.select().with_only_columns(belongings.c.owner_id, func.sum(belongings.c.price)).group_by(belongings.c.owner_id).having(func.sum(belongings.c.price) > 200)

result = conn.execute(aggregate_statement)

for row in result.fetchall():
    print(row)
