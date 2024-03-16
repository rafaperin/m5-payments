from sqlalchemy import Column, UUID, String, func, DateTime

from src.external.postgresql_database import Base


class Payments(Base):
    order_id = Column(UUID, primary_key=True, index=True)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    payment_status = Column(String(30), nullable=False)
