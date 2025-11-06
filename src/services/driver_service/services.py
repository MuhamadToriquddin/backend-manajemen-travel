from . import models
from sqlalchemy.orm import Session
from src.entities.driver import Driver
from src.response_model import response
from sqlalchemy.exc import SQLAlchemyError

# buat driver baru
def create_new_driver(data:models.RequestCreateNewDriver,db:Session):
    try:
        driver = Driver(
            driver_name = data.driver_name,
            phone = data.phone,
            address=data.address
        )    
        db.add(driver)
        db.commit()
        db.refresh(driver)
        return response.success_response(
            message=f"Berhasil menambahkan supir {driver.driver_name}",
        )
    except SQLAlchemyError as e:
        db.rollback()
        return response.error_response(message=f"Gagal menambahkan supir {data.driver_name}:{str(e)}",status_code=400)
    
# update driver
def update_driver(driver_id:int,data:models.RequestUpdateDriver,db:Session):
    driver = db.query(Driver).filter(Driver.id == driver_id,Driver.is_deleted == False).first()
    if not driver:
        return response.error_response(message="supir tidak ditemukan",status_code=404)
    try:
        driver.driver_name = data.driver_name
        driver.phone = data.phone
        driver.address = data.address
        
        db.commit()
        db.refresh(driver)
        
        return response.success_response(message=f"Berhasil mengubah informasi supir {driver.driver_name}")
    except SQLAlchemyError as e:
        db.rollback()
        return response.error_response(message=f"Gagal mengubah informasi supir {data.driver_name}:{str(e)}",status_code=400)
# hapus driver
def delete_driver(driver_id:int,db:Session):
    driver = db.query(Driver).filter(Driver.id == driver_id,Driver.is_deleted == False).first()
    if not driver:
        return response.error_response(message="supir tidak ditemukan",status_code=404)
    driver_name = driver.driver_name
    try:
        driver.is_deleted = True
        
        db.commit()
        db.refresh(driver)
        
        return response.success_response(message=f"Berhasil menghapus supir {driver_name}")
    except SQLAlchemyError as e:
        db.rollback()
        return response.error_response(message=f"Gagal menghapus supir {driver_name}:{str(e)}",status_code=400)

# ambil spesifik driver
def get_driver(driver_id:int,db:Session):
    driver = db.query(Driver).filter(Driver.id == driver_id,Driver.is_deleted == False).first()
    if not driver:
        return response.error_response(message="supir tidak ditemukan",status_code=404)
    try:
        return response.success_response(message=f"Berhasil ambil data supir {driver.driver_name}",data={k: v for k, v in driver.__dict__.items() if k != "_sa_instance_state"})
    except SQLAlchemyError as e:
        return response.error_response(message=f"Gagal mengambil data supir {driver.driver_name}:{str(e)}",status_code=400)     
    
# ambil semua driver
def get_all_drivers(db:Session,q:str=""):
    query = db.query(Driver).filter(Driver.is_deleted == False)

    # Jika ada keyword, filter driver_name menggunakan LIKE (case-insensitive)
    if q:
        query = query.filter(Driver.driver_name.ilike(f"%{q}%"))

    drivers = query.all()

    if not drivers:
        return response.error_response(message="supir tidak ditemukan", status_code=404)

    # Konversi driver ke list of dict agar bisa di-serialize
    drivers_data = [
        {k: v for k, v in driver.__dict__.items() if not k.startswith("_")}
        for driver in drivers
    ]
    try:
        return response.success_response(message=f"Berhasil ambil data supir",data=drivers_data) 
    except SQLAlchemyError as e:
        return response.error_response(message=f"Gagal mengambil data supir:{str(e)}",status_code=400)     
