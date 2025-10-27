from src.database.core import engine, Base
from src.entities.driver import Driver
from src.entities.partner import Partner
from src.entities.route import Route
from src.entities.partner_payout import PartnerPayout

def migrate_database():
    Base.metadata.create_all(engine)
    print("Tabel yang dibuat :",Base.metadata.tables.keys())
    
migrate_database()
