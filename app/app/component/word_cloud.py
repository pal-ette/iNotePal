import reflex as rx
from typing import List, Dict


class WordCloud(rx.Component):
    """WordCloud component."""

    tag = "ReactWordcloud options={options}"

    words: rx.Var[List[Dict[str, str | int]]] = []
    is_default = True

    lib_dependencies: List[str] = [
        "react-wordcloud",
    ]

    def _get_custom_code(self) -> str | None:
        return """import dynamic from 'next/dynamic'
const ReactWordcloud = dynamic(() => import('react-wordcloud'), {
  ssr: false,
})
const options = {
  colors: ["#49312d", "#91615a", "#af625c", "#de776c", "#e5988e", "#ebb9b0", "#f2ebc8"],
  rotations: 2,
  rotationAngles: [-90, 0],
  fontFamily: "impact",
  padding: 1,
  scale: "sqrt",
  fontSizes: [10, 60],
  fontStyle: "normal",
}
"""


# const size = [600, 600]


word_cloud = WordCloud.create
