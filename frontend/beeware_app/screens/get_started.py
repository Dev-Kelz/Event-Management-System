from pathlib import Path

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


PURPLE = "#6542D8"
TEXT = "#151A35"
MUTED = "#5D6686"
BORDER = "#E5E7F0"


def _feature_card(icon, title, description, icon_color, icon_background):
	icon_view = toga.Label(
		icon,
		style=Pack(
			width=58,
			height=58,
			padding_top=16,
			text_align="center",
			font_size=22,
			color=icon_color,
			background_color=icon_background,
		),
	)
	copy = toga.Box(
		children=[
			toga.Label(title, style=Pack(font_size=14, font_weight="bold", color=TEXT)),
			toga.Label(
				description,
				style=Pack(font_size=11, color=MUTED, padding_top=5, flex=1),
			),
		],
		style=Pack(direction=COLUMN, padding_left=18, flex=1),
	)
	return toga.Box(
		children=[icon_view, copy],
		style=Pack(
			direction=ROW,
			padding=18,
			margin_bottom=12,
			background_color="#FFFFFF",
		),
	)


def build_get_started_screen(on_get_started=None, on_login=None):
	"""Build the onboarding screen shown before account setup."""
	image_path = Path(__file__).with_name("ChatGPT Image Aug 19, 2026, 01_58_31 PM.png")
	illustration = toga.ImageView(
		toga.Image(data=image_path.read_bytes()),
		style=Pack(flex=1, width=390, height=720),
	)

	language_button = toga.Button(
		"◎  English ⌄",
		style=Pack(
			width=128,
			padding=(9, 14),
			color=TEXT,
			background_color="#FFFFFF",
		),
	)
	feature_list = toga.Box(
		children=[
			_feature_card(
				"▣", "Create & Manage Events",
				"Create events, set dates, invite attendees and keep everything organized.",
				"#6240D8", "#F0EBFF",
			),
			_feature_card(
				"✓", "Track Tasks & Stages",
				"Break your event into stages and tasks. Track progress and stay on schedule.",
				"#14A77A", "#E7F7F1",
			),
			_feature_card(
				"●", "Get Notified",
				"Receive reminders and push notifications for important updates and deadlines.",
				"#EAA719", "#FFF7E3",
			),
			_feature_card(
				"♣", "Collaborate Easily",
				"Invite team members and work together to make your event a success.",
				"#218DDA", "#E8F4FF",
			),
		],
		style=Pack(direction=COLUMN, flex=1, padding_top=24),
	)

	get_started_button = toga.Button(
		"Get Started       →",
		on_press=on_get_started,
		style=Pack(
			padding=13,
			color="#FFFFFF",
			background_color=PURPLE,
			font_size=14,
			font_weight="bold",
		),
	)
	existing_account_button = toga.Button(
		"⇥  I already have an account",
		on_press=on_login,
		style=Pack(
			padding=11,
			color=PURPLE,
			background_color="#FFFFFF",
			font_size=12,
		),
	)

	welcome_panel = toga.Box(
		children=[
			toga.Box(children=[language_button], style=Pack(direction=ROW, justify_content="end")),
			toga.Label("👋 Welcome!", style=Pack(font_size=28, font_weight="bold", color=TEXT, padding_top=54)),
			toga.Label("Let's get you started with Event Manager", style=Pack(font_size=13, color=MUTED, padding_top=4)),
			feature_list,
			get_started_button,
			toga.Label("──────────────    or    ──────────────", style=Pack(text_align="center", color="#9AA1B7", padding=(17, 0))),
			existing_account_button,
			toga.Label("●  •  •  •", style=Pack(text_align="center", color=PURPLE, padding_top=48, font_size=13)),
		],
		style=Pack(direction=COLUMN, flex=1, padding=(66, 54, 28)),
	)

	return toga.Box(
		children=[illustration, welcome_panel],
		style=Pack(direction=ROW, flex=1, background_color="#FFFFFF"),
	)
