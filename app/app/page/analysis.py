import reflex as rx

from app.component.navbar import navbar
from app.state.analysis_state import AnalysisState
from app.page.login import require_login
from app.state.calendar_state import calendar_component
from app.app_state import AppState
from app.routes import ANALYSIS_ROUTE
from reflex_wordcloud import wordcloud

# 공포 기쁨 놀람 분노 슬픔 중립 혐오


@rx.page(route=ANALYSIS_ROUTE, on_load=AppState.check_login)
@require_login
def analysis_page() -> rx.Component:

    calendar = calendar_component(
        year=AnalysisState.year,
        select_year=AnalysisState.select_year,
        month=AnalysisState.month,
        select_month=AnalysisState.select_month,
        day=AnalysisState.day,
        on_next_month=AnalysisState.on_next_month,
        on_prev_month=AnalysisState.on_prev_month,
        on_change_day=AnalysisState.on_change_day,
        monthdayscalendar=AnalysisState.monthdayscalendar,
    )
    start_calendar_form = rx.popover.root(
        rx.popover.trigger(
            rx.button("시작일", rx.icon("calendar-check"), variant="ghost"),
        ),
        rx.popover.content(
            calendar,
            rx.popover.close(
                rx.button("Close"),
            ),
            style={"width": 450},
        ),
        strategy="fixed",
        return_focus_on_close=True,
        match_width=True,
        on_open_change=AnalysisState.onOpenChangeStartDay,
    )

    end_calendar_form = rx.popover.root(
        rx.popover.trigger(
            rx.button("종료일", rx.icon("calendar-check"), variant="ghost")
        ),
        rx.popover.content(
            calendar,
            rx.popover.close(
                rx.button("Close"),
            ),
            style={"width": 450},
        ),
        strategy="fixed",
        return_focus_on_close=True,
        match_width=True,
        on_open_change=AnalysisState.onOpenChangeEndDay,
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
                    start_calendar_form,
                    rx.heading(AnalysisState.print_start_day_text),
                ),
                rx.flex(
                    end_calendar_form,
                    rx.heading(AnalysisState.print_end_day_text),
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
                                data_key="total",
                                stroke="#DCDCDC",
                                fill="#DCDCDC",
                                fill_opacity=0.8,
                            ),
                            rx.recharts.radar(
                                data_key="period",
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
                                    data_key="emotion",
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
