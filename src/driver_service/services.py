from . import models
from sqlalchemy.orm import Session
from src.entities.driver import Driver
from src import exceptions
from typing import Union
# fungsi pembantu


# fungsi utama
# fungsi get semua data supir, repair: add filter is_deleted di pengambilan data dan return model yang sesuai
def get_all_drivers(db:Session):
    try:
        drivers = db.query(Driver).filter(Driver.is_deleted == False).all()
        return [models.Driver.model_validate(d) for d in drivers]
    except:
        db.rollback()
        exceptions.internal_error()
    
        
# fungsi get spesifik supir
def get_spesific_driver(db:Session,driver_id:int):
    driver:models.Driver=db.query(Driver).filter(Driver.id == driver_id,Driver.is_deleted == False).first()
    if not driver:
        exceptions.not_found()
    try:
        return models.Driver.model_validate(driver)
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)
        
# fungsi create supir baru
def create_new_driver(form_data:models.RequestCreateNewDriver,db:Session):
    try:
        driver = Driver(
            driver_name=form_data.driver_name,
            phone = form_data.phone,
            address = form_data.address
        )
        db.add(driver)
        db.commit()
        return form_data.driver_name
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)

# fungsi update driver
def update_driver(driver_id:int,form_data:models.RequestUpdateDriver,db:Session)->Union[None,dict]:
    driver = db.query(Driver).filter(Driver.id == driver_id,Driver.is_deleted == False).first()
    if not driver :
        exceptions.not_found()
    try:
        driver.driver_name=form_data.driver_name
        driver.phone=form_data.phone
        driver.address=form_data.address
        db.commit()
        db.refresh(driver)
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)
        
# fungsi soft delete driver
def delete_driver(driver_id:int, db:Session)->Union[str,dict]:
    driver = db.query(Driver).filter(Driver.id == driver_id,Driver.is_deleted == False).first()
    if not driver :
        exceptions.not_found()
    try:
        driver_name=driver.driver_name
        driver.is_deleted=True
        db.commit()
        db.refresh(driver)   
        return driver_name
    except exceptions as e:
        db.rollback()
        exceptions.internal_error(e) 
    