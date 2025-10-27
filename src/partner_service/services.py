from . import models
from sqlalchemy.orm import Session
from src.entities.partner import Partner
from src import exceptions
from typing import Union
# fungsi pembantu
def increase_fee(db:Session,partner_id:int,type:str,fee:int):
    try:
        partner = db.query(Partner).filter(Partner.id == partner_id).first()
        if type == "billable":
            partner.billable_fee += fee
        elif type == "collected":
            partner.collected_fee += fee
        else:
            exceptions.bad_request()
        db.commit()
        db.refresh(partner)
    except Exception as e:
        exceptions.internal_error(e)


# fungsi utama
# fungsi get semua data partner
def get_all_partners(db:Session):
    try:
        partners = db.query(Partner).filter(Partner.is_deleted == False).all()
        return [models.Partner.model_validate(p) for p in partners]    
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)

# fungsi get partner spesifik
def get_spesific_partner(db:Session,partner_id:int):
    partner = db.query(Partner).filter(Partner.id == partner_id,Partner.is_deleted == False).first()
    if not partner:
        exceptions.not_found()
    try:
        return models.Partner.model_validate(partner)    
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)

# fungsi create partner baru
def create_new_partner(form_data:models.RequestCreateNewPartner,db:Session):
    try:
        partner = Partner(
            partner_name=form_data.partner_name,
            phone = form_data.phone,
            address = form_data.address
        )
        db.add(partner)
        db.commit()
        return form_data.partner_name
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)

# fungsi update partner
def update_partner(partner_id:int,form_data:models.RequestUpdatePartner,db:Session):
    partner = db.query(Partner).filter(Partner.id == partner_id,Partner.is_deleted == False).first()
    if not partner :
        exceptions.not_found()
    try:
        partner.partner_name=form_data.partner_name
        partner.phone=form_data.phone
        partner.address=form_data.address
        db.commit()
        db.refresh(partner)
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)
        
# fungsi soft delete partner
def delete_partner(partner_id:int, db:Session):
    partner = db.query(Partner).filter(Partner.id == partner_id,Partner.is_deleted == False).first()
    if not partner :
        exceptions.not_found()
    try:
        partner_name=partner.partner_name
        partner.is_deleted=True
        db.commit()
        db.refresh(partner)   
        return partner_name
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e) 
    