from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app_models import Order, OrderItem
from orders.schemas import OrderCreate, OrderOut, OrderItemCreate, OrderItemOut

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order in the database from the provided order data.
    """
    try:
        # Create the order first without the items
        db_order = Order(user_id=order.user_id)
        db.add(db_order)
        
        # Flush to get the order_id without committing
        # This assigns the ID but keeps everything in the transaction
        db.flush()
        
        # Now create the order items with the order_id from the new order
        order_items = []
        for item_data in order.items:
            db_order_item = OrderItem(
                order_id=db_order.order_id,
                item_id=item_data.item_id,
                quantity=item_data.quantity
            )
            db.add(db_order_item)
            order_items.append(db_order_item)
        
        # Commit the entire transaction only after all entities are created
        db.commit()
        
        # Refresh the order to get the updated relationships
        db.refresh(db_order)
    except Exception as e:
        # If any error occurs, roll back the entire transaction
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")
    
    # Create the response with the complete order and items
    order_out = OrderOut.model_validate(db_order)
    order_out.items = [OrderItemOut.model_validate(item) for item in order_items]
    
    return order_out


@router.get("/", response_model=list[OrderOut])
def get_orders(db: Session = Depends(get_db)):
    """
    Retrieve a list of all orders from the database.
    """
    orders = db.query(Order).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    
    order_out_list = []

    for order in orders:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.order_id).all()
        order_list = []
        for order_item in order_items:
            order_list.append(OrderItemOut.model_validate(order_item))
        # order_list.extend(OrderItemOut.model_validate(order_item) for order_item in order_items)

        order_out = OrderOut.model_validate(order)
        order_out.items = order_list
        order_out_list.append(order_out)
    
    return order_out_list


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific order by its ID.
    Raises 404 if the order is not found.
    """
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.order_id).all()
    order_out = OrderOut.model_validate(order)
    order_out.items = [OrderItemOut.model_validate(item) for item in order_items]

    return order_out