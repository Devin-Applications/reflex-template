from rxconfig import config
import reflex as rx
from typing import List, Dict

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

# Add state and page to the app.

class AppState(rx.State):
    vendors: List[Dict[str, str]] = []
    name: str = ""
    contact_info: str = ""
    address: str = ""
    email: str = ""
    phone: str = ""

    def register_vendor(self):
        new_vendor = {
            "name": self.name,
            "contact_info": self.contact_info,
            "address": self.address,
            "email": self.email,
            "phone": self.phone
        }
        self.vendors.append(new_vendor)
        self.clear_form()

    def clear_form(self):
        self.name = ""
        self.contact_info = ""
        self.address = ""
        self.email = ""
        self.phone = ""

    def get_vendors(self) -> List[Dict[str, str]]:
        return self.vendors

    @rx.var
    def vendor_count(self) -> int:
        return len(self.vendors)

    def render_vendor_form(self) -> rx.Component:
        return rx.vstack(
            rx.input(placeholder="Vendor Name", value=self.name, on_change=self.set_name),
            rx.input(placeholder="Contact Information", value=self.contact_info, on_change=self.set_contact_info),
            rx.input(placeholder="Address", value=self.address, on_change=self.set_address),
            rx.input(placeholder="Email", value=self.email, on_change=self.set_email),
            rx.input(placeholder="Phone Number", value=self.phone, on_change=self.set_phone),
            rx.button("Register", on_click=self.register_vendor),
            width="100%",
            spacing="1em",
        )

    def render_vendor_list(self) -> rx.Component:
        return rx.cond(
            self.vendor_count == 0,
            rx.text("No vendors registered yet."),
            rx.vstack(
                rx.foreach(
                    self.vendors,
                    lambda vendor, i: rx.box(
                        rx.vstack(
                            rx.text(f"Name: {vendor['name']}"),
                            rx.text(f"Contact: {vendor['contact_info']}"),
                            rx.text(f"Address: {vendor['address']}"),
                            rx.text(f"Email: {vendor['email']}"),
                            rx.text(f"Phone: {vendor['phone']}"),
                            align_items="start",
                            spacing="0.5em",
                        ),
                        padding="1em",
                        border="1px solid #eaeaea",
                        border_radius="5px",
                        margin_bottom="1em",
                    )
                )
            )
        )

def index() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Welcome to Reflex on Railway!", font_size="2em"),
            rx.box("Get started by editing ", rx.code(filename, font_size="1em")),
            rx.link(
                "Check out our docs!",
                href=docs_url,
                border="0.1em solid",
                padding="0.5em",
                border_radius="0.5em",
                _hover={
                    "color": rx.color_mode_cond(
                        light="rgb(107,99,246)",
                        dark="rgb(179, 175, 255)",
                    )
                },
            ),
            spacing="1.5em",
            font_size="2em",
            padding_top="10%",
        ),
    )

def health() -> rx.Component:
    return rx.text("healthy")

def not_found(page_text: str = "404 - Page not found") -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading(page_text, font_size="2em"),
            spacing="1.5em",
            padding_top="10%",
        ),
    )

def vendor_registration_page() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Vendor Registration", font_size="2em"),
            AppState.render_vendor_form,  # Pass the method reference
            spacing="1.5em",
            padding_top="10%",
        ),
    )

def vendor_listing_page() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Vendor List", font_size="2em"),
            AppState.render_vendor_list,  # Pass the method reference
            spacing="1.5em",
            padding_top="10%",
        ),
    )

app = rx.App(state=AppState)
app.add_page(index, route="/")
app.add_page(health, route="/health")
app.add_page(vendor_registration_page, route="/vendor/register")
app.add_page(vendor_listing_page, route="/vendor/list")
app.add_page(not_found, route="*")
app.compile()
