import reflex as rx
from reflex.event import passthrough_event_spec


class ColorPicker(rx.Component):
    library = "react-colorful"
    tag = "HexColorPicker"
    color: rx.Var[str]
    on_change: rx.EventHandler[passthrough_event_spec(str)]


color_picker = ColorPicker.create
