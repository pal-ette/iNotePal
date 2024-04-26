import reflex as rx

# from app.routes import ANALYSIS_ROUTE, REGISTER_ROUTE
from app.state.login_state import LoginState
from app.component.navbar import navbar
from app.state import analysis_state

# 그래프 그리기 위한 임시 데이터.

# ["is_user"],
# ["message"],
# ["emotion"],

# 공포 기쁨 놀람 분노 슬픔 중립 혐오
dummy1 = [
    {
        "is_user": True,
        "message": "안녕",
        "emotion": "공포",
        "created_at": "2022-02-22 10:11:12.000",
    },
    {
        "is_user": True,
        "message": "안녕2",
        "emotion": "기쁨",
        "created_at": "2022-02-22 10:11:23.000",
    },
    {
        "is_user": True,
        "message": "안녕3",
        "emotion": "중립",
        "created_at": "2022-02-22 10:11:33.000",
    },
    {
        "is_user": True,
        "message": "안녕4",
        "emotion": "놀람",
        "created_at": "2022-02-22 10:11:40.000",
    },
    {
        "is_user": True,
        "message": "안녕5",
        "emotion": "분노",
        "created_at": "2022-02-22 10:12:12.000",
    },
    {
        "is_user": True,
        "message": "안녕6",
        "emotion": "슬픔",
        "created_at": "2022-02-22 10:12:42.000",
    },
    {
        "is_user": True,
        "message": "안녕7",
        "emotion": "혐오",
        "created_at": "2022-02-22 10:13:12.000",
    },
    {
        "is_user": True,
        "message": "안녕8",
        "emotion": "분노",
        "created_at": "2022-02-22 10:13:30.000",
    },
]

dummy2 = [
    {
        "is_user": True,
        "message": "날씨 좋아",
        "emotion": "기쁨",
        "created_at": "2022-02-22 10:11:12.000",
    },
    {
        "is_user": True,
        "message": "기분 좋아",
        "emotion": "기쁨",
        "created_at": "2022-02-22 10:11:23.000",
    },
    {
        "is_user": True,
        "message": "뭘까",
        "emotion": "중립",
        "created_at": "2022-02-22 10:11:33.000",
    },
    {
        "is_user": True,
        "message": "바람이 좋아",
        "emotion": "기쁨",
        "created_at": "2022-02-22 10:11:40.000",
    },
    {
        "is_user": True,
        "message": "안녕5",
        "emotion": "기쁨",
        "created_at": "2022-02-22 10:12:12.000",
    },
    {
        "is_user": True,
        "message": "안녕6",
        "emotion": "중립",
        "created_at": "2022-02-22 10:12:42.000",
    },
    {
        "is_user": True,
        "message": "안녕7",
        "emotion": "기쁨",
        "created_at": "2022-02-22 10:13:12.000",
    },
    {
        "is_user": True,
        "message": "안녕8",
        "emotion": "기쁨",
        "created_at": "2022-02-22 10:13:30.000",
    },
]


def analysis_page() -> rx.Component:

    start_calendar_form = rx.chakra.popover(
        rx.chakra.popover_trigger(
            rx.chakra.button("시작일", variant="ghost"),
        ),
        rx.chakra.popover_content(
            rx.chakra.popover_body(
                analysis_state.demo(),
            ),
            rx.chakra.popover_close_button(),
        ),
        strategy="fixed",
        return_focus_on_close=True,
        match_width=True,
        on_close=analysis_state.aCalendar.setStartDay,
    )

    end_calendar_form = rx.chakra.popover(
        rx.chakra.popover_trigger(rx.chakra.button("종료일", variant="ghost")),
        rx.chakra.popover_content(
            rx.chakra.popover_body(
                analysis_state.demo(),
            ),
            rx.chakra.popover_close_button(),
        ),
        strategy="fixed",
        return_focus_on_close=True,
        match_width=True,
        on_close=analysis_state.aCalendar.setEndDay,
    )

    return rx.fragment(
        navbar(),
        rx.container(
            margin_top="120px",
        ),
        rx.chakra.wrap(
            # rx.heading("기간별 감정 분석"),
            # rx.chakra.hstack(
            rx.chakra.wrap_item(
                start_calendar_form,
                rx.heading(analysis_state.aCalendar.start_day),
                # ),
            ),
            # rx.chakra.hstack(
            rx.chakra.wrap_item(
                end_calendar_form,
                rx.heading(analysis_state.aCalendar.end_day),
                # ),
            ),
            align="center",
            width="100%",
            spacing="2em",
        ),
        # analysis_state.logs(),
        # rx.cond(
        #     LoginState.is_hydrated,
        #     rx.chakra.vstack(
        #         rx.chakra.flex(
        #             rx.chakra.text(
        #                 "text텍스트", size="md", weight="bold", align="left"
        #             ),
        #             rx.chakra.table_container(
        #                 rx.chakra.table(
        #                     headers=["Name", "Age", "Location"],
        #                     rows=[
        #                         ("John", 30, "New York"),
        #                         ("Jane", 31, "San Francisco"),
        #                         ("Joe", 32, "Los Angeles"),
        #                     ],
        #                     footers=["Footer 1", "Footer 2", "Footer 3"],
        #                     variant="striped",
        #                 ),
        #                 rx.chakra.table(
        #                     rx.chakra.thead(
        #                         rx.chakra.tr(
        #                             rx.chakra.th("Name"),
        #                             rx.chakra.th("Age"),
        #                         )
        #                     ),
        #                     rx.chakra.tbody(
        #                         rx.chakra.tr(
        #                             rx.chakra.td("John"),
        #                             rx.chakra.td(30),
        #                         )
        #                     ),
        #                 ),
        #             ),
        #         ),
        #     ),
        # ),
    )
