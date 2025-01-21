import time
import threading
import tkinter as tk
from tkinter import ttk

import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw


def create_image():
    """
    Creates a simple PIL Image to use as the tray icon.
    Feel free to replace with a custom .ico or .png.
    """
    width = 64
    height = 64
    color1 = "blue"
    color2 = "white"

    image = Image.new("RGB", (width, height), color1)
    d = ImageDraw.Draw(image)
    d.rectangle(
        [(width // 4, height // 4), (3 * width // 4, 3 * height // 4)],
        fill=color2
    )
    return image


class GoStudyApp:
    def __init__(self):
        """
        Initializes the tkinter root (hidden) and sets up the system tray icon.
        """
        # Create the tkinter root
        self.root = tk.Tk()
        self.root.title("GoStudy (Hidden Window)")
        self.root.withdraw()  # Hide the main window, since we only use the tray icon

        # Create the system tray icon
        self.icon_image = create_image()
        self.icon = pystray.Icon(
            "GoStudyTimer",
            self.icon_image,
            menu=pystray.Menu(
                item("15 min", lambda: self.start_timer(15)),
                item("30 min", lambda: self.start_timer(30)),
                item("45 min", lambda: self.start_timer(45)),
                item("60 min", lambda: self.start_timer(60)),
                item("Quit", self.quit_app)
            )
        )

    def start_timer(self, minutes: int):
        """
        Starts a background thread that waits for 'minutes' minutes and then
        schedules the popup creation on the main thread via root.after().
        """
        def timer_thread():
            time.sleep(minutes * 60)  # Wait for the specified time
            self.root.after(0, self.show_popup)  # Schedule GUI update on main thread

        t = threading.Thread(target=timer_thread, daemon=True)
        t.start()

    def show_popup(self):
        """
        Displays a fullscreen, always-on-top window with a "GO STUDY" message
        and a "Yes" button to close it.
        """
        popup = tk.Toplevel(self.root)
        popup.title("GO STUDY!")
        popup.attributes("-fullscreen", True)
        popup.attributes("-topmost", True)

        frame = ttk.Frame(popup)
        frame.pack(expand=True, fill="both")

        label = ttk.Label(frame, text="GO STUDY", font=("Arial", 48, "bold"))
        label.pack(pady=50)

        yes_button = ttk.Button(frame, text="Yes", command=popup.destroy)
        yes_button.pack(pady=20)

    def run(self):
        """
        1) Run the pystray icon in a detached thread (doesn't block).
        2) Start the tkinter main loop on the main thread.
        """
        self.icon.run_detached()   # Start system tray in a background thread
        self.root.mainloop()       # Keep the main thread active in the Tk event loop

    def quit_app(self, icon, item):
        """
        Callback to stop the tray icon and close the tkinter main loop.
        """
        self.icon.stop()
        self.root.quit()


if __name__ == "__main__":
    app = GoStudyApp()
    app.run()
