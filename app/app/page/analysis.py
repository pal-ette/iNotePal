import reflex as rx
import reflex_local_auth

from app.component.navbar import navbar
from app.state.analysis_state import AnalysisState
from app.state.calendar_state import calendar_component
from app.app_state import AppState
from app.routes import ANALYSIS_ROUTE
from reflex_wordcloud import wordcloud

# 공포 기쁨 놀람 분노 슬픔 중립 혐오


@rx.page(route=ANALYSIS_ROUTE, on_load=AppState.on_load)
@reflex_local_auth.require_login
def analysis_page() -> rx.Component:

    calendar = calendar_component(
        rx.hstack(
            rx.popover.close(
                rx.button(
                    "닫기",
                    size="1",
                    color_scheme="tomato",
                ),
            ),
        ),
        select_date=AnalysisState.range_select_date,
        accent_dates=AnalysisState.dates_has_closed_chat,
        on_change_date=AnalysisState.on_change_date,
        allow_future=False,
    )

    return rx.fragment(
        navbar(),
        rx.cond(
            AnalysisState.is_hydrated,
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
                                on_click=AnalysisState.reset_date_valid_check,
                            ),
                        ),
                        spacing="3",
                    ),
                ),
                open=~AnalysisState.date_valid_check,
            ),
        ),
        rx.container(
            margin_top="120px",
        ),
        rx.container(
            rx.hstack(
                rx.flex(
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.button(
                                rx.hstack(
                                    "시작일",
                                    rx.icon(
                                        "calendar-check",
                                        size=18,
                                    ),
                                    rx.heading(
                                        f"{AnalysisState.start_year}년 {AnalysisState.start_month}월 {AnalysisState.start_day}일",
                                        high_contrast=True,
                                    ),
                                    align="center",
                                ),
                                variant="ghost",
                            ),
                        ),
                        rx.popover.content(
                            calendar,
                        ),
                        strategy="fixed",
                        return_focus_on_close=True,
                        match_width=True,
                        on_open_change=[
                            AnalysisState.on_open_change_start_date,
                            lambda is_open: calendar.State.set_display_month(
                                rx.cond(
                                    is_open,
                                    AnalysisState.start_year,
                                    calendar.State.year,
                                ),
                                rx.cond(
                                    is_open,
                                    AnalysisState.start_month,
                                    calendar.State.month,
                                ),
                            ),
                        ],
                    ),
                ),
                rx.flex(
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.button(
                                rx.hstack(
                                    "종료일",
                                    rx.icon(
                                        "calendar-check",
                                        size=18,
                                    ),
                                    rx.heading(
                                        f"{AnalysisState.end_year}년 {AnalysisState.end_month}월 {AnalysisState.end_day}일",
                                        high_contrast=True,
                                    ),
                                    align="center",
                                ),
                                variant="ghost",
                            )
                        ),
                        rx.popover.content(
                            calendar,
                        ),
                        strategy="fixed",
                        return_focus_on_close=True,
                        match_width=True,
                        on_open_change=[
                            AnalysisState.on_open_change_end_date,
                            lambda is_open: calendar.State.set_display_month(
                                rx.cond(
                                    is_open,
                                    AnalysisState.end_year,
                                    calendar.State.year,
                                ),
                                rx.cond(
                                    is_open,
                                    AnalysisState.end_month,
                                    calendar.State.month,
                                ),
                            ),
                        ],
                    ),
                ),
            ),
            rx.heading("위 기간동안 당신의 감정상태는", size="4", color_scheme="gray"),
            rx.vstack(
                rx.grid(
                    rx.flex(
                        wordcloud(
                            words=AnalysisState.display_words,
                            options={
                                "colors": [
                                    "#49312d",
                                    "#91615a",
                                    "#af625c",
                                    "#de776c",
                                    "#e5988e",
                                    "#ebb9b0",
                                    "#f2ebc8",
                                ],
                                "rotations": 2,
                                "rotationAngles": [-90, 0],
                                "fontFamily": "impact",
                                "padding": 1,
                                "scale": "sqrt",
                                "fontSizes": [10, 60],
                                "fontStyle": "normal",
                            },
                        ),
                        grid_column="span 2",
                    ),
                    rx.flex(
                        rx.recharts.radar_chart(
                            rx.recharts.radar(
                                data_key="전체",
                                stroke="#DCDCDC",
                                fill="#DCDCDC",
                                fill_opacity=0.8,
                            ),
                            rx.recharts.radar(
                                data_key="기간",
                                stroke="#de776c",
                                fill="#e5988e",
                            ),
                            rx.recharts.polar_grid(),
                            rx.recharts.polar_angle_axis(data_key="emotion"),
                            rx.recharts.graphing_tooltip(),
                            rx.recharts.legend(),
                            data=AnalysisState.data_emotion_radar,
                            width="100%",
                            height="100%",
                        ),
                        height="30em",
                        width="100%",
                    ),
                    rx.flex(
                        rx.recharts.funnel_chart(
                            rx.recharts.funnel(
                                rx.recharts.label_list(
                                    position="right",
                                    data_key="name",
                                    fill="#000",
                                    stroke="none",
                                ),
                                data_key="count",
                                data=AnalysisState.data_emotion_funnel,
                            ),
                            rx.recharts.graphing_tooltip(),
                            width="100%",
                            height="100%",
                        ),
                        height="30em",
                        width="100%",
                        align="center",
                        justify="center",
                    ),
                    rx.flex(
                        rx.recharts.bar_chart(
                            rx.foreach(
                                [
                                    "기쁨",
                                    "공포",
                                    "슬픔",
                                    "혐오",
                                    "분노",
                                    "놀람",
                                    "중립",
                                ],
                                lambda key: rx.recharts.bar(
                                    data_key=key,
                                    stroke=AnalysisState.emotion_color_map[key],
                                    fill=AnalysisState.emotion_color_map[key],
                                ),
                            ),
                            rx.recharts.brush(
                                data_key="date", height=20, stroke="#e5988e"
                            ),
                            rx.recharts.x_axis(data_key="date"),
                            rx.recharts.y_axis(),
                            rx.recharts.legend(),
                            data=AnalysisState.data_emotion_bar,
                        ),
                        height="30em",
                        width="100%",
                        grid_column="span 2",
                    ),
                    rx.box(
                        rx.recharts.line_chart(
                            rx.foreach(
                                [
                                    "기쁨",
                                    "공포",
                                    "슬픔",
                                    "혐오",
                                    "분노",
                                    "놀람",
                                    "중립",
                                ],
                                lambda key: rx.recharts.line(
                                    data_key=key,
                                    stroke=AnalysisState.emotion_color_map[key],
                                ),
                            ),
                            rx.recharts.x_axis(data_key="date"),
                            rx.recharts.y_axis(),
                            rx.recharts.legend(),
                            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                            margin={
                                "left": 10,
                                "right": 0,
                                "top": 20,
                                "bottom": 10,
                            },
                            data=AnalysisState.data_emotion_bar,
                        ),
                        height="30em",
                        width="100%",
                        grid_column="span 2",
                    ),
                    grid_template_columns=[
                        "repeat(1, 1fr)",
                        "repeat(1, 1fr)",
                        "repeat(2, 1fr)",
                        "repeat(2, 1fr)",
                        "repeat(2, 1fr)",
                        "repeat(2, 1fr)",
                    ],
                    spacing="2",
                    width="100%",
                ),
                width="100%",
            ),
            size="4",
            width="100%",
        ),
    )
