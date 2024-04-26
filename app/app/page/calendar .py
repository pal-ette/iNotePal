import reflex as rx

# difine a method to toffle form
def task_form():
    return rx.model(
        rx.model
    )


@rx.page(route="/calender")
def index() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(tag="add", cursor="pointer"),
            rx.color_mode_button(),
            rx.color_mode_icon(),
            color_scheme="none",
            _dark={"color": " white"},
            _ligth={"color": "black"},
        ),
        width="100%",
        display="flex",
        justify_content = "end",
        padding="0.75 rem 2rem"
    )



# app = rx.App()