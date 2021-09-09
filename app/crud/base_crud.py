from typing import Generic, List, Optional, Type, TypeVar, Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, new_obj_data: CreateSchemaType) -> ModelType:
        db_obj = self.model(**new_obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read(self, db: Session, obj_id) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def read_all(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def update(self, db: Session, obj_id, new_obj_data: Union[UpdateSchemaType, Dict[str, Any]]):
        db_obj = db.query(self.model).filter(self.model.id == obj_id).first()
        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in new_obj_data:
                setattr(db_obj, field, new_obj_data[field])
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, obj_id) -> ModelType:
        db_obj = db.query(self.model).filter(self.model.id == obj_id)
        db_obj.delete(synchronize_session=False)
        db.commit()
        return db_obj
