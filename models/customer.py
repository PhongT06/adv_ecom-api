from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(320))
    phone: Mapped[str] = mapped_column(db.String(15))
    username: Mapped[str] = mapped_column(db.String(255))
    password: Mapped[str] = mapped_column(db.String(255))
    orders: Mapped[List['Order']] = db.relationship(back_populates='customer')
    # role_id: Mapped[int] = mapped_column(db.ForeignKey('roles.id'), default=1)
    # role: Mapped["Role"] = db.relationship(back_populates='customers')

    def __repr__(self):
        return f"<Customer {self.id}|{self.name}>"

