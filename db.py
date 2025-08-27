from pony.orm import *
db = Database()
db.bind(provider="sqlite", filename="bot_store.sqlite", create_db=True)

class Order(db.Entity):
    quantity = Required(int)
    model = Required(str)


db.generate_mapping(create_tables=True)   