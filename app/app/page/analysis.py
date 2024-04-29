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

# 그래프 확인용 연동 데이터
data = [
    {
        "emotion": "기쁨",
        "count": 120,
        "fullMark": 150,
    },
    {
        "emotion": "놀람",
        "count": 98,
        "fullMark": 150,
    },
    {
        "emotion": "분노",
        "count": 86,
        "fullMark": 150,
    },
    {
        "emotion": "슬픔",
        "count": 99,
        "fullMark": 150,
    },
    {
        "emotion": "중립",
        "count": 85,
        "fullMark": 150,
    },
    {
        "emotion": "혐오",
        "count": 65,
        "fullMark": 150,
    },
    {
        "emotion": "공포",
        "count": 65,
        "fullMark": 150,
    },
]


data2 = [
    {
        "emotion": "기쁨",
        "count": 120,
    },
    {
        "emotion": "놀람",
        "count": 98,
    },
    {
        "emotion": "분노",
        "count": 86,
    },
    {
        "emotion": "슬픔",
        "count": 99,
    },
    {
        "emotion": "중립",
        "count": 85,
    },
    {
        "emotion": "혐오",
        "count": 65,
    },
    {
        "emotion": "공포",
        "count": 65,
    },
]

data3 = [
    {
        "date": "0410",
        "count": 1,
        "count2": 3,
    },
    {
        "date": "0411",
        "count": 2,
        "count2": 1,
    },
    {
        "date": "0412",
        "count": 1,
        "count2": 5,
    },
    {
        "date": "0413",
        "count": 3,
        "count2": 1,
    },
    {
        "date": "0414",
        "count": 1,
        "count2": 1,
    },
]


def analysis_page() -> rx.Component:

    start_calendar_form = rx.chakra.popover(
        rx.chakra.popover_trigger(
            rx.chakra.button("시작일", rx.icon("calendar-check"), variant="ghost"),
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
        rx.chakra.popover_trigger(
            rx.chakra.button("종료일", rx.icon("calendar-check"), variant="ghost")
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
        on_close=analysis_state.aCalendar.setEndDay,
    )

    show_buttons_form = rx.chakra.button_group(
        rx.chakra.button(
            "Radar chart",
            # is_loading=True,
            # loading_text="Loading...",
            # spinner_placement="start",
            on_click=analysis_state.chart.radar_chart_status,
        ),
        rx.chakra.button(
            "Funnel chart", on_click=analysis_state.chart.funnel_chart_status
        ),
        rx.chakra.button("Bar chart", on_click=analysis_state.chart.bar_chart_status),
        rx.chakra.button("Line chart", on_click=analysis_state.chart.line_chart_status),
        is_attached=True,
        variant="outline",
        size="lg",
        # spacing=5,
    )

    # show_radio_buttons_form = (rx.radio(["1", "2", "3"], default_value=1),)

    return rx.fragment(
        navbar(),
        rx.cond(
            analysis_state.aCalendar.is_hydrated,
            rx.alert_dialog.root(
                rx.alert_dialog.content(
                    rx.alert_dialog.title("날짜 선택"),
                    rx.alert_dialog.description(
                        "종료 날짜가 시작 날짜보다 앞섭니다. 다시 입력하세요.",
                    ),
                    rx.flex(
                        rx.alert_dialog.action(
                            rx.button(
                                "확인",
                                on_click=analysis_state.aCalendar.reset_date_valid_check,
                            ),
                        ),
                        spacing="3",
                    ),
                ),
                open=~analysis_state.aCalendar.date_valid_check,
            ),
        ),
        rx.container(
            margin_top="120px",
        ),
        rx.chakra.wrap(
            rx.chakra.wrap_item(
                start_calendar_form,
                rx.heading(analysis_state.aCalendar.start_day),
            ),
            rx.chakra.wrap_item(
                end_calendar_form,
                rx.heading(analysis_state.aCalendar.end_day),
            ),
            align="center",
            width="100%",
            spacing="2em",
        ),
        # analysis_state.logs(),
        rx.chakra.wrap(
            rx.cond(
                analysis_state.aCalendar.graph_valid_check,
                rx.chakra.flex(
                    rx.container(
                        margin_top="20px",
                    ),
                    show_buttons_form,
                    rx.container(
                        margin_top="10px",
                    ),
                    rx.chakra.vstack(
                        rx.cond(
                            analysis_state.chart.radar_chart_check,
                            rx.vstack(
                                rx.heading("당신의 감정", size="4"),
                                rx.recharts.radar_chart(
                                    rx.recharts.radar(
                                        data_key="count",
                                        stroke="#8884d8",
                                        fill="#8884d8",
                                    ),
                                    rx.recharts.polar_grid(),
                                    rx.recharts.polar_angle_axis(data_key="emotion"),
                                    data=data2,
                                    width="100%",
                                    height=400,
                                ),
                                align="center",
                                width="100%",
                            ),
                        ),
                        rx.cond(
                            ~analysis_state.chart.radar_chart_check,
                            rx.chakra.text(" "),
                        ),
                        rx.cond(
                            analysis_state.chart.funnel_chart_check,
                            rx.recharts.funnel_chart(
                                rx.recharts.funnel(
                                    rx.recharts.label_list(
                                        position="right",
                                        data_key="name",
                                        fill="#000",
                                        stroke="none",
                                    ),
                                    data_key="value",
                                    data=analysis_state.data_funnel,
                                ),
                                rx.recharts.graphing_tooltip(),
                                width=1000,
                                height=250,
                            ),
                        ),
                        rx.cond(
                            ~analysis_state.chart.funnel_chart_check,
                            rx.chakra.text(""),
                        ),
                        rx.cond(
                            analysis_state.chart.bar_chart_check,
                            rx.recharts.bar_chart(
                                rx.recharts.bar(
                                    data_key="count2", stroke="#8884d8", fill="#8884d8"
                                ),
                                rx.recharts.x_axis(data_key="date"),
                                rx.recharts.y_axis(),
                                data=data3,
                            ),
                        ),
                        rx.cond(
                            ~analysis_state.chart.bar_chart_check,
                            rx.chakra.text(""),
                        ),
                        rx.cond(
                            analysis_state.chart.line_chart_check,
                            rx.recharts.line_chart(
                                rx.recharts.line(
                                    data_key="count",
                                    stroke="#8884d8",
                                ),
                                rx.recharts.line(
                                    data_key="count2",
                                    stroke="#82ca9d",
                                ),
                                rx.recharts.x_axis(data_key="date"),
                                rx.recharts.y_axis(),
                                data=data3,
                            ),
                        ),
                        rx.cond(
                            ~analysis_state.chart.line_chart_check,
                            rx.chakra.text(""),
                        ),
                        # rx.chakra.table(
                        #     headers=["날짜", "정서"],
                        #     rows=[
                        #         ("20240412", "기쁨"),
                        #         ("20240413", "중립"),
                        #     ],
                        #     variant="striped",
                        # ),
                    ),
                    direction="column",
                    width="100%",
                ),
            ),
        ),
    )
