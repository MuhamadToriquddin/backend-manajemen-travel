from . import models
from sqlalchemy.orm import Session
from src.entities.partner_payout import PartnerPayout
from src import exceptions
from typing import Union
from uuid import UUID
from src.entities.partner_payout import TypePayout

# fungsi get semua data partner
def get_all_partner_payouts(db:Session):
    try:
        partner_payouts = db.query(PartnerPayout).filter(PartnerPayout.is_deleted == False).all()
        return [models.PartnerPayout.model_validate(p) for p in partner_payouts]    
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)

# fungsi create partner baru
def create_new_partner_payout(form_data:models.RequestCreateNewPartnerPayout,db:Session):
    try:
        partner_payout = PartnerPayout(
            partner_name=form_data.partner_name,
            fee = form_data.fee,
            type = TypePayout(form_data.type.value)
        )
        db.add(partner_payout)
        db.commit()
        return {
            "partner name":form_data.partner_name,
            "tipe":form_data.type.value
        }
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)
        
# fungsi soft delete partner
def delete_partner_payout(partner_payout_id:int, db:Session):
    partner_payout = db.query(PartnerPayout).filter(PartnerPayout.id == partner_payout_id,PartnerPayout.is_deleted == False).first()
    if not partner_payout :
        exceptions.not_found()
    try:
        partner_name=partner_payout.partner_name
        partner_payout.is_deleted=True
        db.commit()
        db.refresh(partner_payout)   
        return partner_name
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e) 
    