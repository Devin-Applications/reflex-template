from rxconfig import config
import reflex as rx
from typing import List, Dict

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

# Add state and page to the app.

class AppState(rx.State):
    vendors: List[Dict[str, str]] = []

    def register_vendor(self, form_data: Dict[str, str]):
        self.vendors.append(form_data)

    def get_vendors(self) -> List[Dict[str, str]]:
        return self.vendors

    @rx.var
    def vendor_count(self) -> int:
        return len(self.vendors)

    def render_vendor_form(self) -> rx.Component:
        return rx.vstack(
            rx.form(
                rx.vstack(
                    rx.input(name="name", placeholder="Vendor Name"),
                    rx.input(name="contact_info", placeholder="Contact Information"),
                    rx.input(name="address", placeholder="Address"),
                    rx.input(name="email", placeholder="Email"),
                    rx.input(name="phone", placeholder="Phone Number"),
                    rx.button("Register", type="submit")
                ),
                on_submit=self.register_vendor
            )
        )

    def render_vendor_list(self) -> rx.Component:
        return rx.cond(
            self.vendor_count == 0,
            rx.text("No vendors registered yet."),
            rx.vstack(
                rx.heading("Vendor List"),
                rx.foreach(
                    self.vendors,
                    lambda vendor: rx.box(vendor.get("name", "Unknown Vendor"))
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
            AppState.render_vendor_form(),  # Call the method to return a component
            spacing="1.5em",
            padding_top="10%",
        ),
    )

def vendor_listing_page() -> rx.Component:
    return rx.fragment(
        rx.color_mode_button(rx.color_mode_icon(), float="right"),
        rx.vstack(
            rx.heading("Vendor List", font_size="2em"),
            AppState.render_vendor_list(),  # Call the method to return a component
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
