import reflex as rx
from reflex.event import passthrough_event_spec


class ColorfulBase(rx.Component):
    library = "react-colorful"
    color: rx.Var[str]
    on_change: rx.EventHandler[passthrough_event_spec(str)]


class ColorPicker(ColorfulBase):
    tag = "HexColorPicker"


class ColorInput(ColorfulBase):
    tag = "HexColorInput"


color_picker = ColorPicker.create
color_input = ColorInput.create
