from . import models
from sqlalchemy.orm import Session
from src.entities.route import Route
from src import exceptions
from typing import Union

# fungsi get semua data rute, repair: add filter is_deleted di pengambilan data dan return model yang sesuai
def get_all_routes(db:Session):
    try:
        routes = db.query(Route).filter(Route.is_deleted == False).all()
        return [models.Route.model_validate(r) for r in routes]    
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)

# fungsi get rute spesifik
def get_spesific_route(db:Session,route_id:int):
    route = db.query(Route).filter(Route.id == route_id, Route.is_deleted == False).first()
    if not route:
        exceptions.not_found()
    try:
        return models.Route.model_validate(route)    
    except:
        db.rollback()
        exceptions.internal_error()

# fungsi create rute baru
def create_new_route(form_data:models.RequestCreateNewRoute,db:Session):
    try:
        route = Route(
            route_name=form_data.route_name,
            duration = form_data.duration,
            time_schedules = form_data.time_schedules
        )
        db.add(route)
        db.commit()
        return route
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)

# fungsi update rute
def update_route(route_id:int,form_data:models.RequestUpdateRoute,db:Session):
    route = db.query(Route).filter(Route.id == route_id, Route.is_deleted == False).first()
    if not route :
        exceptions.not_found()
    try:
        route.route_name=form_data.route_name
        route.duration=form_data.duration
        route.time_schedules=form_data.time_schedules
        db.commit()
        db.refresh(route)
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)
        
# fungsi soft delete rute
def delete_route(route_id:int, db:Session):
    route = db.query(Route).filter(Route.id == route_id, Route.is_deleted == False).first()
    if not route :
        exceptions.not_found()
    try:
        route_name=route.route_name
        route.is_deleted=True
        db.commit()
        db.refresh(route)   
        return route_name
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e) 
    