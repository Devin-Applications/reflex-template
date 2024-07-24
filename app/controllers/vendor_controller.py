# app/controllers/vendor_controller.py

from app.models.vendor import Vendor
from sqlmodel import Session, select
from reflex import Controller

class VendorController(Controller):
    def register_vendor(self, form_data):
        with Session(self.engine) as session:
            vendor = Vendor(
                name=form_data["name"],
                contact_info=form_data["contact_info"],
                address=form_data.get("address"),
                email=form_data.get("email"),
                phone=form_data.get("phone")
            )
            session.add(vendor)
            session.commit()

    def get_vendors(self):
        with Session(self.engine) as session:
            statement = select(Vendor)
            results = session.exec(statement)
            return results.all()

    def update_vendor(self, vendor_id, form_data):
        with Session(self.engine) as session:
            vendor = session.get(Vendor, vendor_id)
            if vendor:
                vendor.name = form_data["name"]
                vendor.contact_info = form_data["contact_info"]
                vendor.address = form_data.get("address")
                vendor.email = form_data.get("email")
                vendor.phone = form_data.get("phone")
                session.commit()

    def delete_vendor(self, vendor_id):
        with Session(self.engine) as session:
            vendor = session.get(Vendor, vendor_id)
            if vendor:
                session.delete(vendor)
                session.commit()
