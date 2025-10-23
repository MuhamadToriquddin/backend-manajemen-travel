from . import models
from sqlalchemy.orm import Session
from src.entities.partner import Partner
from src import exceptions

# fungsi pembantu



# fungsi utama
# fungsi get semua data partner
def get_all_partners(db:Session)->models.Partner:
    try:
        partners:models.Partner = db.query(Partner).all()
        return partners    
    except:
        exceptions.internal_error()

# fungsi get partner spesifik
def get_spesific_partner(db:Session,partner_id:int)->models.Partner:
    try:
        partner:models.Partner = db.query(Partner).filter(Partner.id == partner_id).first()
        return partner    
    except:
        exceptions.internal_error()

# fungsi create partner baru
def create_new_partner(form_data:models.RequestCreateNewPartner,db:Session)->None:
    try:
        if not form_data:
            exceptions.bad_request()
        partner = Partner(
            partner_name=form_data.partner_name,
            phone = form_data.phone,
            address = form_data.address
        )
        db.add(partner)
        db.commit()
        return partner
    except:
        exceptions.internal_error

# fungsi update partner
def update_partner(partner_id:int,form_data:models.RequestUpdatePartner,db:Session):
    try:
        if not form_data:
            exceptions.bad_request()
        partner = db.query(Partner).filter(Partner.id == partner_id).first()
        if not partner :
            exceptions.not_found()
        partner.partner_name=form_data.partner_name
        partner.phone=form_data.phone
        partner.time_schedules=form_data.address
        db.commit()
        db.refresh(partner)
    except:
        exceptions.internal_error()
        
# fungsi soft delete partner
def delete_partner(partner_id:int, db:Session):
    try:
        partner = db.query(Partner).filter(Partner.id == partner_id).first()
        if not partner :
            exceptions.not_found()
        partner_name=partner.partner_name
        partner.is_deleted=True
        db.commit()
        db.refresh(partner)   
        return partner_name
    except:
        exceptions.internal_error() 
    