from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.favorite import Favorite
from app.models.train import Train

router = APIRouter(prefix="/me", tags=["Favorites"])


@router.post("/favorites/{train_no}")
def add_favorite(
    train_no: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    train = db.query(Train).filter(Train.train_no == train_no).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    exists = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == current_user.id,
            Favorite.train_id == train.id
        )
        .first()
    )

    if exists:
        return {"message": "Train already in favorites"}

    fav = Favorite(
        user_id=current_user.id,
        train_id=train.id
    )

    db.add(fav)
    db.commit()

    return {"message": "Train added to favorites"}


@router.get("/favorites")
def get_favorites(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    rows = (
        db.query(Train)
        .join(Favorite, Favorite.train_id == Train.id)
        .filter(Favorite.user_id == current_user.id)
        .all()
    )

    return [
        {
            "train_no": t.train_no,
            "train_name": t.name
        }
        for t in rows
    ]

@router.delete("/favorites/{train_no}")
def remove_favorite(
    train_no: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    train = db.query(Train).filter(Train.train_no == train_no).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    favorite = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == current_user.id,
            Favorite.train_id == train.id
        )
        .first()
    )

    if not favorite:
        return {"message": "Train not in favorites"}

    db.delete(favorite)
    db.commit()

    return {"message": "Train removed from favorites"}
