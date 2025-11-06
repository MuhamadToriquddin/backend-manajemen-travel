from . import models
from sqlalchemy.orm import Session
from src.entities.route import Route
from src.response_model import response
from sqlalchemy.exc import SQLAlchemyError

# buat rute baru
def create_new_route(data:models.RequestCreateNewRoute,db:Session):
    try:
        route = Route(
            route_name=data.route_name,
            duration=data.duration,
            time_schedules=data.time_schedules
        )    
        db.add(route)
        db.commit()
        db.refresh(route)
        return response.success_response(
            message=f"Berhasil menambahkan rute",
        )
    except SQLAlchemyError as e:
        db.rollback()
        return response.error_response(message=f"Gagal menambahkan rute:{str(e)}",status_code=400)
    
# update rute
def update_route(route_id:int,data:models.RequestUpdateRoute,db:Session):
    route = db.query(Route).filter(Route.id == route_id,Route.is_deleted == False).first()
    if not route:
        return response.error_response(message="rute tidak ditemukan",status_code=404)
    try:
        route.route_name = data.route_name
        route.duration = data.duration
        route.time_schedules = data.time_schedules
        
        db.commit()
        db.refresh(route)
        
        return response.success_response(message=f"Berhasil mengubah informasi rute")
    except SQLAlchemyError as e:
        db.rollback()
        return response.error_response(message=f"Gagal mengubah informasi rute:{str(e)}",status_code=400)
# hapus rute
def delete_route(route_id:int,db:Session):
    route = db.query(Route).filter(Route.id == route_id,Route.is_deleted == False).first()
    if not route:
        return response.error_response(message="rute tidak ditemukan",status_code=404)
    
    try:
        route.is_deleted = True
        
        db.commit()
        db.refresh(route)
        
        return response.success_response(message=f"Berhasil menghapus rute")
    except SQLAlchemyError as e:
        db.rollback()
        return response.error_response(message=f"Gagal menghapus rute:{str(e)}",status_code=400)

# ambil spesifik rute
def get_route(route_id:int,db:Session):
    route = db.query(Route).filter(Route.id == route_id,Route.is_deleted == False).first()
    if not route:
        return response.error_response(message="rute tidak ditemukan",status_code=404)
    try:
        return response.success_response(message=f"Berhasil ambil data rute {route.route_name}",data={k: v for k, v in route.__dict__.items() if k != "_sa_instance_state"})
    except SQLAlchemyError as e:
        return response.error_response(message=f"Gagal mengambil data rute {route.route_name}:{str(e)}",status_code=400)     
    
# ambil semua rute
def get_all_routes(db:Session,q:str=""):
    query = db.query(Route).filter(Route.is_deleted == False)

    # Jika ada keyword, filter driver_name menggunakan LIKE (case-insensitive)
    if q:
        query = query.filter(Route.route_name.ilike(f"%{q}%"))

    routes = query.all()

    if not routes:
        return response.error_response(message="rute tidak ditemukan", status_code=404)

    # Konversi driver ke list of dict agar bisa di-serialize
    routes_data = [
        {k: v for k, v in route.__dict__.items() if not k.startswith("_")}
        for route in routes
    ]
    try:
        return response.success_response(message=f"Berhasil ambil data rute",data=routes_data) 
    except SQLAlchemyError as e:
        return response.error_response(message=f"Gagal mengambil data rute:{str(e)}",status_code=400)     
