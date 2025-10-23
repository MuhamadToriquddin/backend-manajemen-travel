from . import models
from sqlalchemy.orm import Session
from src.entities.route import Route
from src import exceptions

# fungsi pembantu



# fungsi utama
# fungsi get semua data rute
def get_all_routes(db:Session)->models.Routes:
    try:
        routes:models.Routes = db.query(Route).all()
        return routes    
    except:
        exceptions.internal_error()

# fungsi get rute spesifik
def get_spesific_route(db:Session,route_id:int)->models.Route:
    try:
        route:models.Route = db.query(Route).filter(Route.id == route_id).first()
        return route    
    except:
        exceptions.internal_error()

# fungsi create rute baru
def create_new_route(form_data:models.RequestCreateNewRoute,db:Session)->None:
    try:
        if not form_data:
            exceptions.bad_request()
        route = Route(
            route_name=form_data.route_name,
            duration = form_data.duration,
            time_schedules = form_data.time_schedules
        )
        db.add(route)
        db.commit()
        return route
    except:
        exceptions.internal_error

# fungsi update rute
def update_route(route_id:int,form_data:models.RequestUpdateRoute,db:Session):
    try:
        if not form_data:
            exceptions.bad_request()
        route = db.query(Route).filter(Route.id == route_id).first()
        if not route :
            exceptions.not_found()
        route.route_name=form_data.route_name
        route.duration=form_data.duration
        route.time_schedules=form_data.time_schedules
        db.commit()
        db.refresh(route)
    except:
        exceptions.internal_error()
        
# fungsi soft delete rute
def delete_route(route_id:int, db:Session):
    try:
        route = db.query(Route).filter(Route.id == route_id).first()
        if not route :
            exceptions.not_found()
        route_name=route.route_name
        route.is_deleted=True
        db.commit()
        db.refresh(route)   
        return route_name
    except:
        exceptions.internal_error() 
    