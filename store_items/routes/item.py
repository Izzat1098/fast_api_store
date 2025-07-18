from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app_models import Item
from store_items.schemas import ItemCreate, ItemOut

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=ItemOut)
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> ItemOut:
    """
    Create a new item in the database.
    """
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return ItemOut.model_validate(db_item)


@router.get("/", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)) -> list[ItemOut]:
    """
    Retrieve a list of all items.
    """
    items = db.query(Item).all()

    return [ItemOut.model_validate(i) for i in items]


@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ItemOut:
    """
    Retrieve a single item by its ID.
    Raises 404 if the item is not found.
    """
    item = db.query(Item).filter(Item.item_id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return ItemOut.model_validate(item)