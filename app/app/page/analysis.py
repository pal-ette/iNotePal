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
        on_close=[
            analysis_state.AnalysisState.setStartDay,
            analysis_state.AnalysisState.getDataDay,
        ],
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
        on_close=[
            analysis_state.AnalysisState.setEndDay,
            analysis_state.AnalysisState.getDataDay,
        ],
    )

    show_buttons_form = rx.chakra.button_group(
        rx.chakra.button(
            "Radar chart",
            # is_loading=True,
            # loading_text="Loading...",
            # spinner_placement="start",
            on_click=[
                analysis_state.AnalysisState.radar_chart_status,
                analysis_state.AnalysisState.emotion_count_day,
            ],
        ),
        rx.chakra.button(
            "Funnel chart",
            on_click=[
                analysis_state.AnalysisState.funnel_chart_status,
                analysis_state.AnalysisState.getDataFunnels,
            ],
        ),
        rx.chakra.button(
            "Bar chart", on_click=analysis_state.AnalysisState.bar_chart_status
        ),
        rx.chakra.button(
            "Line chart", on_click=analysis_state.AnalysisState.line_chart_status
        ),
        is_attached=True,
        variant="outline",
        size="lg",
        # spacing=5,
    )

    # show_radio_buttons_form = (rx.radio(["1", "2", "3"], default_value=1),)

    return rx.fragment(
        navbar(),
        rx.cond(
            analysis_state.AnalysisState.is_hydrated,
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
                                on_click=analysis_state.AnalysisState.reset_date_valid_check,
                            ),
                        ),
                        spacing="3",
                    ),
                ),
                open=~analysis_state.AnalysisState.date_valid_check,
            ),
        ),
        rx.container(
            margin_top="120px",
        ),
        rx.chakra.wrap(
            rx.chakra.wrap_item(
                start_calendar_form,
                rx.heading(analysis_state.AnalysisState.start_day),
            ),
            rx.chakra.wrap_item(
                end_calendar_form,
                rx.heading(analysis_state.AnalysisState.end_day),
            ),
            align="center",
            width="100%",
            spacing="2em",
        ),
        # analysis_state.logs(),
        rx.chakra.wrap(
            rx.cond(
                analysis_state.AnalysisState.graph_valid_check,
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
                            analysis_state.AnalysisState.radar_chart_check,
                            rx.vstack(
                                rx.heading("위 기간동안 당신의 감정상태는", size="4"),
                                rx.recharts.radar_chart(
                                    rx.recharts.radar(
                                        data_key="count",
                                        stroke="#8884d8",
                                        fill="#8884d8",
                                        # linear(to-l, #f2ebc8, #de776c, #49312d)",
                                    ),
                                    rx.recharts.polar_grid(),
                                    rx.recharts.polar_angle_axis(data_key="emotion"),
                                    rx.recharts.graphing_tooltip(),
                                    data=analysis_state.AnalysisState.data_emotion_frequency,
                                    width="100%",
                                    height=400,
                                ),
                                align="center",
                                width="100%",
                                margin_top="10px",
                            ),
                        ),
                        rx.cond(
                            ~analysis_state.AnalysisState.radar_chart_check,
                            rx.chakra.text(" "),
                        ),
                        rx.cond(
                            analysis_state.AnalysisState.funnel_chart_check,
                            rx.recharts.funnel_chart(
                                rx.recharts.funnel(
                                    rx.recharts.label_list(
                                        position="right",
                                        data_key="emotion",
                                        fill="#000",
                                        stroke="none",
                                    ),
                                    data_key="count",
                                    data=analysis_state.AnalysisState.data_funnel,
                                ),
                                rx.recharts.graphing_tooltip(),
                                width=500,
                                height=400,
                            ),
                        ),
                        rx.cond(
                            ~analysis_state.AnalysisState.funnel_chart_check,
                            rx.chakra.text(""),
                        ),
                        rx.cond(
                            analysis_state.AnalysisState.bar_chart_check,
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
                            ~analysis_state.AnalysisState.bar_chart_check,
                            rx.chakra.text(""),
                        ),
                        rx.cond(
                            analysis_state.AnalysisState.line_chart_check,
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
                            ~analysis_state.AnalysisState.line_chart_check,
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
