from . import models
from sqlalchemy.orm import Session
from src.entities.order_passenger import OrderPassenger
from src.entities.handle_order import HandleOrder
from src import exceptions
from src.partner_service.services import increase_fee

def create_new_order_passenger(db:Session, form_data:models.RequestCreateNewOrderPassenger):
    try:
        order = OrderPassenger(
            passenger_name=form_data.order_details.passenger_name,
            phone=form_data.order_details.phone,
            pickup_address=form_data.order_details.pickup_address,
            destination_address=form_data.order_details.destination_address,
            description=form_data.order_details.description,
            order_date=form_data.order_information.order_date,
            departure_date=form_data.order_information.departure_date,
            route_id=form_data.order_information.route_id,
            departure_time=form_data.order_information.departure_time,
            total_passenger=form_data.order_information.total_passenger,
            price_each=form_data.order_information.price_each,
            discount=form_data.order_information.discount,
        )
        order_name = order.passenger_name
        db.add(order)
        db.commit()
        return order_name
    except Exception as e:
        exceptions.internal_error(e)
    
def handle_order(db:Session,form_data:models.RequestHandleOrder):
    order = db.query(OrderPassenger).filter(OrderPassenger.is_deleted==False,OrderPassenger.id ==form_data.order_id).first()
    if not order:
        exceptions.not_found()
    try:
        handle = HandleOrder(
            driver_id=form_data.driver_id,
            partner_id=form_data.partner_id,
            fee=form_data.fee
        )
        order.status = "UNCOMPLETED"
        db.add(handle)
        db.commit()
        db.refresh(order)
    except:
        db.rollback()
        exceptions.internal_error()
        
def complete_order(db:Session,form_data:models.RequestCompletedOrder):
    handle_info = db.query(HandleOrder).filter(HandleOrder.order_id == form_data.order_id).first()
    order = db.query(OrderPassenger).filter(OrderPassenger.is_deleted == False, OrderPassenger.id == form_data.order_id).first()
    if not handle_info and not order:
        exceptions.not_found()
    try:
        if handle_info.driver_id == None and handle_info.partner_id is not None:
            increase_fee(db=db,partner_id=handle_info.partner_id,type="collected",fee=handle_info.fee)
        elif handle_info.driver_id is not None and handle_info.partner_id is not None:
            increase_fee(db=db,partner_id=handle_info.partner_id,type="billable",fee=handle_info.fee)
        elif handle_info.driver_id is not None and handle_info.partner_id == None:
            increase_fee(db=db,partner_id=handle_info.partner_id,type="billable",fee=0)
        else:
            exceptions.bad_request()
        return f"Pesanan atas nama {order.passenger_name} telah selesai"
    except Exception as e:
        db.rollback()
        exceptions.internal_error(e)