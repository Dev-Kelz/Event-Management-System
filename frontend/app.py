import httpx
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from beeware_app.screens.get_started import build_get_started_screen
from beeware_app.screens.register import build_register_screen

API_BASE_URL = "http://127.0.0.1:8000/api"


class EventManagementApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title="Event Management System")
        self.show_get_started()
        self.main_window.show()

    def show_get_started(self, widget=None):
        self.main_window.content = build_get_started_screen(on_get_started=self.show_register)

    def show_register(self, widget=None):
        self.main_window.content = build_register_screen(on_back=self.show_get_started)

    async def load_events(self, widget=None):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{API_BASE_URL}/events")
                response.raise_for_status()

            payload = response.json()
            events = payload.get("events", [])
            rows = [
                (event.get("title", "-"), event.get("date", "-"), event.get("location") or "-")
                for event in events
            ]
            self.events_table.data = rows
            self.status_label.text = f"Loaded {len(events)} event(s)."
        except Exception as exc:  # pragma: no cover - UI feedback path
            self.status_label.text = f"Unable to load events: {exc}"

    async def login(self, widget):
        email = self.email_input.value.strip()
        password = self.password_input.value.strip()

        if not email or not password:
            self.status_label.text = "Enter both email and password."
            return

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{API_BASE_URL}/login",
                    json={"email": email, "password": password},
                )
                response.raise_for_status()

            payload = response.json()
            self.status_label.text = payload.get("message", "Login successful")
        except Exception as exc:  # pragma: no cover - UI feedback path
            self.status_label.text = f"Login failed: {exc}"


if __name__ == "__main__":
    EventManagementApp(
        formal_name="Event Management System",
        app_id="com.eventmanagement.system",
    ).main_loop()
