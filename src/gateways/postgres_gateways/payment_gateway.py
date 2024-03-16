import uuid
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.config import settings

from src.entities.models.payment_entity import payment_factory, Payment
from src.gateways.orm.payment_orm import Payments
from src.interfaces.gateways.payment_gateway_interface import IPaymentGateway

connection_uri = settings.db.SQLALCHEMY_DATABASE_URI

engine = create_engine(
    connection_uri
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class PostgresDBPaymentRepository(IPaymentGateway):
    @staticmethod
    def payment_to_entity(payment: Payments) -> Payment:
        payment = payment_factory(
            payment.order_id,
            payment.creation_date,
            payment.payment_status,
        )
        return payment

    def get_by_id(self, order_id: uuid.UUID) -> Optional[Payment]:
        with SessionLocal() as db:
            payment_db = db.query(Payments).filter(Payments.order_id == order_id).first()

        if payment_db:
            return self.payment_to_entity(payment_db)  # type: ignore
        else:
            return None

    def get_all(self) -> List[Payment]:
        result = []
        with SessionLocal() as db:
            payments = db.query(Payments).order_by(Payments.creation_date).all()
            if payments:
                for payment in payments:
                    payment_entity = self.payment_to_entity(payment)  # type: ignore
                    result.append(payment_entity)
        return result

    def create_payment(self, obj_in: Payment) -> Payment:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = Payments(**obj_in_data)  # type: ignore

        with SessionLocal() as db:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        new_payment = self.payment_to_entity(db_obj)
        return new_payment

    def update_payment(self, order_id: uuid.UUID, obj_in: Payment) -> Payment:
        payment_in = vars(obj_in)
        with SessionLocal() as db:
            db_obj = db.query(Payments).filter(Payments.order_id == order_id).first()
            obj_data = jsonable_encoder(db_obj, by_alias=False)
            for field in obj_data:
                if field in payment_in:
                    setattr(db_obj, field, payment_in[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        updated_payment = self.payment_to_entity(db_obj)  # type: ignore
        return updated_payment

    def remove_payment(self, order_id: uuid.UUID) -> None:
        with SessionLocal() as db:
            payment = db.query(Payments).filter(Payments.order_id == order_id).first()
            db.delete(payment)
            db.commit()
