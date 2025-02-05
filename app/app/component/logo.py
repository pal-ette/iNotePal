import reflex as rx


def logo(title="iNotePal", **kwargs) -> rx.Component:
    result_kwargs = {
        **{
            "as_": "h1",
            "size": "6",
            "weight": "bold",
            "align": "left",
            "background": "linear-gradient(to left, #f2ebc8, #de776c, #49312d)",
            "background_clip": "text",
            "color": "transparent",
        },
        **kwargs,
    }

    return rx.heading(
        title,
        **result_kwargs,
    )
