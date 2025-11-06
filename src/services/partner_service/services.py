from . import models
from sqlalchemy.orm import Session
from src.entities.partner import Partner
from src.response_model import response
from sqlalchemy.exc import SQLAlchemyError

# buat partner baru
def create_new_partner(data:models.RequestCreateNewPartner,db:Session):
    try:
        partner = Partner(
            partner_name = data.partner_name,
            phone = data.phone,
            address=data.address
        )    
        db.add(partner)
        db.commit()
        db.refresh(partner)
        return response.success_response(
            message=f"Berhasil menambahkan mitra {partner.partner_name}",
        )
    except SQLAlchemyError as e:
        db.rollback()
        return response.error_response(message=f"Gagal menambahkan mitra {data.partner_name}:{str(e)}",status_code=400)
    
# update partner
def update_partner(partner_id:int,data:models.RequestUpdatePartner,db:Session):
    partner = db.query(Partner).filter(Partner.id == partner_id,Partner.is_deleted == False).first()
    if not partner:
        return response.error_response(message="Mitra tidak ditemukan",status_code=404)
    try:
        partner.partner_name = data.partner_name
        partner.phone = data.phone
        partner.address = data.address
        
        db.commit()
        db.refresh(partner)
        
        return response.success_response(message=f"Berhasil mengubah informasi mitra {partner.partner_name}")
    except SQLAlchemyError as e:
        db.rollback()
        return response.error_response(message=f"Gagal mengubah informasi mitra {data.partner_name}:{str(e)}",status_code=400)
# hapus partner
def delete_partner(partner_id:int,db:Session):
    partner = db.query(Partner).filter(Partner.id == partner_id,Partner.is_deleted == False).first()
    if not partner:
        return response.error_response(message="Mitra tidak ditemukan",status_code=404)
    if partner.fee != 0:
        return response.error_response(message="Fee mitra masih belum selesai",status_code=400)
    partner_name = partner.partner_name
    try:
        partner.is_deleted = True
        
        db.commit()
        db.refresh(partner)
        
        return response.success_response(message=f"Berhasil menghapus mitra {partner_name}")
    except SQLAlchemyError as e:
        db.rollback()
        return response.error_response(message=f"Gagal menghapus mitra {partner_name}:{str(e)}",status_code=400)
# tambah fee
def increase_fee(data:models.RequestUpdateFeePartner,db:Session):
    partner = db.query(Partner).filter(Partner.id == data.partner_id,Partner.is_deleted == False).first()
    if not partner:
        return response.error_response(message="Mitra tidak ditemukan",status_code=404)
    try:
        partner.fee += data.fee
        
        db.commit()
        db.refresh(partner)
        
        return response.success_response(message=f"Berhasil menambahkan fee yang perlu dibayar mitra {partner.partner_name} sebesar {data.fee}")
    except SQLAlchemyError as e:
        db.rollback()
        return response.error_response(message=f"Gagal menambahkan fee yang perlu dibayar mitra {partner.partner_name} sebesar {data.fee}:{str(e)}",status_code=400) 
# kurangi fee
def decrease_fee(data:models.RequestUpdateFeePartner,db:Session):
    partner = db.query(Partner).filter(Partner.id == data.partner_id,Partner.is_deleted == False).first()
    if not partner:
        return response.error_response(message="Mitra tidak ditemukan",status_code=404)
    try:
        partner.fee -= data.fee
        
        db.commit()
        db.refresh(partner)
        
        return response.success_response(message=f"Berhasil menambahkan fee yang perlu dibayar kantor sebesar {data.fee}")
    except SQLAlchemyError as e:
        db.rollback()
        return response.error_response(message=f"Gagal menambahkan fee yang perlu dibayar kantor sebesar {data.fee}:{str(e)}",status_code=400) 
# ambil spesifik partner
def get_partner(partner_id:int,db:Session):
    partner = db.query(Partner).filter(Partner.id == partner_id,Partner.is_deleted == False).first()
    if not partner:
        return response.error_response(message="Mitra tidak ditemukan",status_code=404)
    try:
        return response.success_response(message=f"Berhasil ambil data mitra {partner.partner_name}",data=partner)
    except SQLAlchemyError as e:
        return response.error_response(message=f"Gagal mengambil data mitra {partner.partner_name}:{str(e)}",status_code=400)     
    
# ambil semua partner
def get_all_partners(db:Session,q:str=""):
    query = db.query(Partner).filter(Partner.is_deleted == False)

    # Jika ada keyword, filter partner_name menggunakan LIKE (case-insensitive)
    if q:
        query = query.filter(Partner.partner_name.ilike(f"%{q}%"))

    partners = query.all()

    if not partners:
        return response.error_response(message="Mitra tidak ditemukan", status_code=404)

    # Konversi partner ke list of dict agar bisa di-serialize
    partners_data = [
        {k: v for k, v in partner.__dict__.items() if not k.startswith("_")}
        for partner in partners
    ]
    try:
        return response.success_response(message=f"Berhasil ambil data mitra",data=partners_data) 
    except SQLAlchemyError as e:
        return response.error_response(message=f"Gagal mengambil data mitra:{str(e)}",status_code=400)     
