import toga

from beeware_app.screens.get_started import build_get_started_screen
from beeware_app.screens.register import build_register_screen


class EventManagementApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title="Event Management System")
        self.show_get_started()
        self.main_window.show()

    def show_get_started(self, widget=None):
        self.main_window.content = build_get_started_screen(on_get_started=self.show_register)

    def show_register(self, widget=None):
        self.main_window.content = build_register_screen(on_back=self.show_get_started)


def main():
    return EventManagementApp(
        formal_name="Event Management System",
        app_id="com.eventmanagement.system",
    )


if __name__ == "__main__":
    main().main_loop()
