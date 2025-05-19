import taipy.gui.builder as tgb
import numpy as np
from data.data import data


selector_country = list(np.sort(data["Country/Region"].astype(str).unique()))
selected_country = "France"


def creates_pages(pages):
    return [(f"/{page}", page.replace("_", " ").title()) for page in list(pages)[1:]]


with tgb.Page() as root:
    tgb.toggle(theme=True)

    with tgb.part("header sticky"):
        with tgb.layout(
            "100px 12rem 1 8rem 150px",
            columns__mobile="100px 12rem 1 8rem 150px",
            class_name="header-content",
        ):
            tgb.image("favicon.png", width="50px")
            tgb.text("Covid **Dashboard**", mode="md")

            with tgb.part("text-center"):
                tgb.navbar(
                    lov=lambda pages: creates_pages(pages),
                    inline=True,
                )

            tgb.part()

            tgb.text(
                "Welcome **back**!",
                mode="md",
            )

    with tgb.part("content"):
        tgb.html("br")

        tgb.content()
