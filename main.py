from fastcore.all import method
from fasthtml.common import Div, Img, Link, Span, Title, serve
from monsterui.all import (H1, H2, Button, ButtonT, Card, Container,
                           ContainerT, Form, Input, Theme, fast_app)

app, rt = fast_app(
    hdrs=(
        # page title
        Title("Counter App - FastHTML"),
        Theme.blue.headers(),
        # favicon link
        Link(rel="icon", type="image/x-icon", href="/static/favicon.ico"),
    ),
    default_hdrs=False
)

counter = 0

@rt
def index():
    return Container(
        H1(
            cls="text-3xl text-center font-bold my-6 flex items-center justify-center gap-2"
        )(Img(src="/static/numbers.svg", alt="Logo", cls="w-8 h-8"), "Counter App"),
        Card(cls="p-6 text-center mb-4 rounded-md")(
            H2("Click The Buttons", cls="mb-4"),
            Div(cls="flex items-center justify-center gap-4 mb-1")(
                Button(
                    "-",
                    hx_post="/dec",
                    hx_target="#count",
                    cls="rounded-md border-2 border-blue-950 hover:border-blue-900 px-4 py-2",
                ),
                Span(id="count", cls="text-2xl font-bold")(counter),
                Button(
                    "+",
                    hx_post="/inc",
                    hx_target="#count",
                    cls="rounded-md border-2 border-blue-950 hover:border-blue-900 px-4 py-2",
                ),
            ),
            Button(
                "Reset",
                hx_post="/reset",
                hx_target="#count",
                cls=f"{ButtonT.primary} rounded-md",
            ),
        ),
        Card(cls="p-6 rounded-md")(
            Form(
                hx_post="/hi",
                hx_target="#result",
                **{"hx-on::after-request": "this.reset()"},
            )(
                Input(name="name", placeholder="Your name...", cls="mb-2 rounded-md"),
                Button("Say Hi", cls=f"{ButtonT.primary} rounded-md"),
            ),
            Div(id="result", cls="mt-4 font-bold"),
        ),
        cls=ContainerT.sm,
    )


@rt("/inc", methods=["POST"])
def inc():
    """Increment the counter by 1."""
    global counter
    try:
        counter += 1
        # add bounds
        if counter > 10:
            counter = 10
        return str(counter)
    except Exception:
        return "Error occured"


@rt("/dec", methods=["POST"])
def dec():
    """Decrement the counter by 1."""
    global counter
    try:
        counter -= 1
        # add bounds
        if counter < -10:
            counter = -10
        return str(counter)
    except Exception:
        return "Error occured"


@rt("/reset", methods=["POST"])
def reset():
    """Reset the counter."""
    global counter
    counter = 0
    return str(counter)


@rt("/hi", methods=["POST"])
def hi(name: str):
    """Greetings."""
    # basic input validation
    if not name or not name.strip():
        return "Please enter a name!"
    return f"Hi, {name.strip()}!"


serve()
