# app/models/vendor.py

from sqlmodel import SQLModel, Field
from typing import Optional

class Vendor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    contact_info: str
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
