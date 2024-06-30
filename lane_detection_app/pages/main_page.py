import tkinter as tk
from pages.video_page import VideoPage

class MainPage:
    def __init__(self, root, show_video_page_callback):
        self.root = root
        self.show_video_page_callback = show_video_page_callback

        self.root.title("Vehicle Road Zone Detection System")
        self.root.configure(bg="#3e3e3e")

        self.frame = tk.Frame(root, bg="#3e3e3e", width=900, height=600)
        self.frame.pack(expand=True)

        self.title_label = tk.Label(self.frame, text="Demo Of Road Lane Detection", font=("Helvetica", 24, "bold"), bg="#3e3e3e", fg="white")
        self.title_label.pack(pady=(60, 10))

        self.subtitle_label = tk.Label(self.frame, text="Welcome to Vehicle Road Lane Detection System..\n"
                                                       "In this project, you can copy and paste a video in the video\n"
                                                       "folder and then run it by using this app and use various filters\n"
                                                       "while detecting road lane.", font=("Helvetica", 14), bg="#3e3e3e", fg="white")
        self.subtitle_label.pack(pady=(0, 40))

        self.button_frame = tk.Frame(self.frame, bg="#3e3e3e")
        self.button_frame.pack(pady=10)

        self.load_button = tk.Button(self.button_frame, text="Load Video", font=("Helvetica", 16), command=self.load_video, bg="white", fg="black", relief="raised", bd=3)
        self.load_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

        self.exit_button = tk.Button(self.button_frame, text="Exit", font=("Helvetica", 16), command=root.quit, bg="white", fg="black", relief="raised", bd=3)
        self.exit_button.pack(side=tk.LEFT, padx=10, ipadx=30, ipady=5)

    def load_video(self):
        self.frame.destroy()
        self.show_video_page_callback()
