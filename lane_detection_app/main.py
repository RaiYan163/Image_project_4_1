import tkinter as tk
from pages.main_page import MainPage
from pages.video_page import VideoPage
from pages.dashboard_page import DashboardPage

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Road Zone Detection System")
        self.root.geometry("1200x900")
        self.show_main_page()

    def show_main_page(self):
        self.clear_frame()
        self.main_page = MainPage(self.root, self.show_video_page)

    def show_video_page(self):
        self.clear_frame()
        self.video_page = VideoPage(self.root, self.show_dashboard_page_or_main_page)

    def show_dashboard_page(self, video_path):
        self.clear_frame()
        self.dashboard_page = DashboardPage(self.root, video_path, self.show_video_page)

    def show_dashboard_page_or_main_page(self, video_path):
        if video_path is None:
            self.show_main_page()
        else:
            self.show_dashboard_page(video_path)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
