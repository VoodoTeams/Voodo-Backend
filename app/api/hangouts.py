from fastapi import APIRouter, Depends, HTTPException, status
from app.services.database import hangouts_collection
from app.models.hangouts import HangoutPost, HangoutPostCreate
from typing import List
import datetime

router = APIRouter(
    prefix="/hangouts",
    tags=["hangouts"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=List[HangoutPost])
async def get_hangouts():
    """Get all hangout posts"""
    hangouts = await hangouts_collection.find().to_list(length=100)
    return hangouts

@router.post("/", response_model=HangoutPost, status_code=status.HTTP_201_CREATED)
async def create_hangout(hangout: HangoutPostCreate):
    """Create a new hangout post (admin only in initial phase)"""
    # For now, we're only allowing admin-created posts as per requirements
    # Later this can be extended to allow user-created posts
    
    new_hangout = hangout.dict()
    new_hangout["created_at"] = datetime.datetime.now()
    
    result = await hangouts_collection.insert_one(new_hangout)
    created_hangout = await hangouts_collection.find_one({"_id": result.inserted_id})
    
    return created_hangout

@router.get("/{hangout_id}", response_model=HangoutPost)
async def get_hangout(hangout_id: str):
    """Get a specific hangout by ID"""
    hangout = await hangouts_collection.find_one({"_id": hangout_id})
    if hangout is None:
        raise HTTPException(status_code=404, detail="Hangout not found")
    return hangout
