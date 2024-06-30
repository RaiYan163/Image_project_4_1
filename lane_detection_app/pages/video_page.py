import tkinter as tk
from tkinter import Listbox
import os

class VideoPage:
    def __init__(self, root, show_dashboard_page_callback):
        self.root = root
        self.show_dashboard_page_callback = show_dashboard_page_callback

        self.root.title("Select a Video")
        self.root.configure(bg="#3e3e3e")

        self.frame = tk.Frame(root, bg="#3e3e3e", width=900, height=600)
        self.frame.pack(expand=True)

        self.video_frame = tk.Frame(self.frame, bg="#3e3e3e", width=800, height=400, relief=tk.SUNKEN, bd=2)
        self.video_frame.pack(pady=20)

        self.listbox = Listbox(self.video_frame, width=50, height=15, font=("Arial", 18))
        self.listbox.pack()

        self.load_videos()

        self.button_frame = tk.Frame(self.frame, bg="#3e3e3e")
        self.button_frame.pack(pady=20)

        self.load_button = tk.Button(self.button_frame, text="Load Video", font=("Arial", 16), command=self.load_selected_video, bg="white", fg="black", relief="raised", bd=3)
        self.load_button.pack(side=tk.LEFT, padx=20, ipadx=10, ipady=5)

        self.back_button = tk.Button(self.button_frame, text="Go Back", font=("Arial", 16), command=self.back, bg="white", fg="black", relief="raised", bd=3)
        self.back_button.pack(side=tk.LEFT, padx=20, ipadx=10, ipady=5)

    def load_videos(self):
        video_dir = "./video/"
        videos = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
        for video in videos:
            self.listbox.insert(tk.END, video)

    def load_selected_video(self):
        selected_video = self.listbox.get(tk.ACTIVE)
        if selected_video:
            video_path = os.path.join("./video/", selected_video)
            self.show_dashboard_page_callback(video_path)

    def back(self):
        self.show_dashboard_page_callback(None)
