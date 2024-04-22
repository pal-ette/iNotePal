import reflex as rx
from app import style
from app.page.login import require_login
from app.state.chat_state import ChatState


def qa(question: str, answer: str) -> rx.Component:
    return rx.chakra.box(
        rx.chakra.box(
            rx.chakra.text(
                question,
                text_align="right",
            ),
            style=style.question_style,
        ),
        rx.chakra.box(
            rx.chakra.text(
                answer,
                text_align="left",
            ),
            style=style.answer_style,
        ),
    )


def chat_history() -> rx.Component:
    return rx.chakra.box(
        rx.foreach(
            ChatState.chat_history,
            lambda messages: qa(
                messages[0],
                messages[1],
            ),
        )
    )


def action_bar() -> rx.Component:
    return rx.chakra.hstack(
        rx.chakra.input(
            value=ChatState.question,
            placeholder="Ask a question",
            on_change=ChatState.set_question,
            style=style.input_style,
        ),
        rx.chakra.button(
            "Ask",
            on_click=ChatState.answer,
            style=style.button_style,
        ),
    )


@require_login
def chat() -> rx.Component:
    """Render a chat page.

    The `require_login` decorator will redirect to the login page if the user is
    not authenticated.

    Returns:
        A reflex component.
    """
    return rx.chakra.vstack(
        rx.chakra.heading("Chat", font_size="2em"),
        rx.chakra.link("Home", href="/"),
        rx.chakra.link("Logout", href="/", on_click=ChatState.do_logout),
        chat_history(),
        rx.divider(),
        action_bar(),
        align="center",
    )
