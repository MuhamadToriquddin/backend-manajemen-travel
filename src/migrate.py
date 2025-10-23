from src.database.core import engine, Base

def migrate_database():
    Base.metadata.create_all(engine)
    
migrate_database()