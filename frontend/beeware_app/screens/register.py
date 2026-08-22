import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


PURPLE = "#6542D8"
PURPLE_DARK = "#24165F"
TEXT = "#151A35"
MUTED = "#5D6686"


def _field(label, placeholder, icon):
    return toga.Box(
        children=[
            toga.Box(
                children=[
                    toga.Label(icon, style=Pack(width=28, font_size=18, color=MUTED, padding_left=11)),
                    toga.TextInput(placeholder=placeholder, style=Pack(flex=1, padding=10)),
                ],
                style=Pack(direction=ROW, height=52, background_color="#FFFFFF"),
            ),
        ],
        style=Pack(direction=COLUMN, padding_bottom=14),
    )


def _benefit(icon, title, description, color):
    return toga.Box(
        children=[
            toga.Box(
                children=[
                    toga.Label(title, style=Pack(font_size=12, font_weight="bold", color=PURPLE_DARK)),
                    toga.Label(description, style=Pack(font_size=10, color=MUTED, padding_top=3)),
                ],
                style=Pack(direction=COLUMN, padding_left=13, flex=1),
            ),
        ],
        style=Pack(direction=ROW, padding=(14, 0), align_items="center"),
    )


def build_register_screen(on_back=None, on_login=None):
    left_panel = toga.Box(
        children=[
            toga.Label("▣  Event Manager", style=Pack(font_size=18, font_weight="bold", color="#FFFFFF")),
            toga.Label("Plan. Organize. Track. Succeed.", style=Pack(font_size=11, color="#EDE9FF", padding_top=7)),
            toga.Label("Create Your\nAccount", style=Pack(font_size=30, font_weight="bold", color="#FFFFFF", padding_top=70)),
            toga.Label("Join thousands of users\nmanaging events and tasks\nmore efficiently.", style=Pack(font_size=15, color="#FFFFFF", padding_top=18)),
            toga.Label("▱\n\n   ✓     ★     ✓", style=Pack(font_size=43, color="#FFFFFF", text_align="center", padding_top=55, flex=1)),
            toga.Box(
                children=[
                    _benefit("▣", "Organize Events", "Keep everything in one place.", "#7045E8"),
                    _benefit("●", "Collaborate Easily", "Work with your team.", "#36B778"),
                    _benefit("♧", "Stay Notified", "Never miss an update.", "#4785F0"),
                ],
                style=Pack(direction=COLUMN, padding=(10, 20), background_color="#FFFFFF"),
            ),
        ],
        style=Pack(direction=COLUMN, width=390, padding=(55, 48, 30), background_color=PURPLE),
    )
    right_panel = toga.Box(
        children=[
            toga.Box(children=[toga.Button("◎  English  ⌄", style=Pack(color=TEXT, background_color="#FFFFFF", padding=9))], style=Pack(direction=ROW, justify_content="end")),
            toga.Label("◉  ◯", style=Pack(font_size=28, color=PURPLE, text_align="center", padding_top=28)),
            toga.Label("Register", style=Pack(font_size=29, font_weight="bold", color=TEXT, text_align="center", padding_top=7)),
            toga.Label("Create your account to get started", style=Pack(font_size=13, color=MUTED, text_align="center", padding_top=7, padding_bottom=28)),
            _field("Full Name", "Enter your full name", "♙"),
            _field("Email Address", "Enter your email address", "✉"),
            _field("Phone Number", "Enter your phone number", "⌕"),
            _field("Password", "Create a password", "▣"),
            _field("Confirm Password", "Confirm your password", "▣"),
            toga.Button("♙  Register", style=Pack(padding=13, color="#FFFFFF", background_color=PURPLE, font_size=14, font_weight="bold")),
            toga.Label("────────────    or    ────────────", style=Pack(text_align="center", color="#969DB4", padding=(16, 0, 10))),
            toga.Button("G   Sign up with Google", style=Pack(padding=11, color=TEXT, background_color="#FFFFFF")),
            toga.Button("▦   Sign up with Microsoft", style=Pack(padding=11, color=TEXT, background_color="#FFFFFF", padding_top=8)),
            toga.Box(children=[toga.Label("Already have an account?", style=Pack(color=MUTED, font_size=11)), toga.Button("Login", on_press=on_login, style=Pack(color=PURPLE, background_color="#FFFFFF", font_size=11, padding_left=8))], style=Pack(direction=ROW, justify_content="center", padding_top=17)),
            toga.Button("← Back", on_press=on_back, style=Pack(color=MUTED, background_color="#FFFFFF", padding_top=14)),
        ],
        style=Pack(direction=COLUMN, flex=1, padding=(35, 55, 25), background_color="#FFFFFF"),
    )
    return toga.Box(children=[left_panel, right_panel], style=Pack(direction=ROW, flex=1, background_color="#FFFFFF"))
