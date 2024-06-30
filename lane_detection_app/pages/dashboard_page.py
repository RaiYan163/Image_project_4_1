import tkinter as tk
from tkinter import Label, Scale, HORIZONTAL
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading

class DashboardPage:
    def __init__(self, root, video_path, go_back_callback):
        self.root = root
        self.video_path = video_path
        self.go_back_callback = go_back_callback

        self.root.title("Dashboard")
        self.root.geometry("1200x900")
        self.root.configure(bg="#3e3e3e")

        self.frame = tk.Frame(root, bg="#3e3e3e", width=1200, height=900)
        self.frame.pack(expand=True)

        self.video_frame = tk.Frame(self.frame, bg="#3e3e3e", width=900, height=600)
        self.video_frame.pack(pady=20)

        self.labels = []
        self.label_texts = ["Frame: Original Roadview", "Frame: Bird's Eye View", "Frame: Thresholded Image", "Frame: Sliding Window Applied"]
        for i in range(4):
            label_frame = tk.Frame(self.video_frame, bg="#3e3e3e")
            label_frame.grid(row=i//2, column=i%2, padx=10, pady=10)

            label = Label(label_frame, bg="#3e3e3e", width=400, height=300)
            label.pack()

            text_label = Label(label_frame, text=self.label_texts[i], bg="#3e3e3e", fg="white", font=("Helvetica", 12))
            text_label.pack()

            self.labels.append(label)

        self.stop_event = threading.Event()
        self.paused = threading.Event()
        self.cap = cv2.VideoCapture(self.video_path)

        self.create_trackbars()

        self.speed_scale = Scale(self.frame, from_=0.1, to=1.0, resolution=0.1, orient=HORIZONTAL, label="Speed Control", length=300)
        self.speed_scale.set(1.0)
        self.speed_scale.pack(pady=10)

        self.button_frame = tk.Frame(self.frame, bg="#3e3e3e")
        self.button_frame.pack(pady=20)

        self.go_back_button = tk.Button(self.button_frame, text="Go Back", font=("Arial", 16), command=self.go_back, bg="white", fg="black", relief="raised", bd=3)
        self.go_back_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

        self.exit_button = tk.Button(self.button_frame, text="Exit", font=("Arial", 16), command=self.root.quit, bg="white", fg="black", relief="raised", bd=3)
        self.exit_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

        self.pause_button = tk.Button(self.button_frame, text="Pause", font=("Arial", 16), command=self.pause_video, bg="white", fg="black", relief="raised", bd=3)
        self.pause_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

        self.play_button = tk.Button(self.button_frame, text="Play", font=("Arial", 16), command=self.play_video, bg="white", fg="black", relief="raised", bd=3)
        self.play_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.update_frames()

    def create_trackbars(self):
        cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Trackbars", 300, 50)
        cv2.createTrackbar("L - H", "Trackbars", 0, 255, lambda x: None)
        cv2.createTrackbar("L - S", "Trackbars", 0, 255, lambda x: None)
        cv2.createTrackbar("L - V", "Trackbars", 200, 255, lambda x: None)
        cv2.createTrackbar("U - H", "Trackbars", 255, 255, lambda x: None)
        cv2.createTrackbar("U - S", "Trackbars", 50, 255, lambda x: None)
        cv2.createTrackbar("U - V", "Trackbars", 255, 255, lambda x: None)

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return None, None, None, None

        frame = cv2.resize(frame, (640, 480))

        tl, bl, tr, br = (222, 387), (70, 472), (400, 380), (538, 472)

        cv2.circle(frame, tl, 5, (0, 0, 255), -1)
        cv2.circle(frame, bl, 5, (0, 0, 255), -1)
        cv2.circle(frame, tr, 5, (0, 0, 255), -1)
        cv2.circle(frame, br, 5, (0, 0, 255), -1)

        cv2.line(frame, tl, bl, (0, 255, 0), 2)
        cv2.line(frame, bl, br, (0, 255, 0), 2)
        cv2.line(frame, br, tr, (0, 255, 0), 2)
        cv2.line(frame, tr, tl, (0, 255, 0), 2)

        pts1 = np.float32([tl, bl, tr, br])
        pts2 = np.float32([[0, 0], [0, 480], [640, 0], [640, 480]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        transformed_frame = cv2.warpPerspective(frame, matrix, (640, 480))

        hsv_transformed_frame = cv2.cvtColor(transformed_frame, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        u_h = cv2.getTrackbarPos("U - H", "Trackbars")
        u_s = cv2.getTrackbarPos("U - S", "Trackbars")
        u_v = cv2.getTrackbarPos("U - V", "Trackbars")

        lower = np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(hsv_transformed_frame, lower, upper)

        histogram = np.sum(mask[mask.shape[0] // 2:, :], axis=0)
        midpoint = int(histogram.shape[0] / 2)
        left_base = np.argmax(histogram[:midpoint])
        right_base = np.argmax(histogram[midpoint:]) + midpoint

        y = 472
        lx, rx = [], []
        msk = mask.copy()

        while y > 0:
            img = mask[y - 40:y, left_base - 50:left_base + 50]
            contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    lx.append(left_base - 50 + cx)
                    left_base = left_base - 50 + cx

            img = mask[y - 40:y, right_base - 50:right_base + 50]
            contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    rx.append(right_base - 50 + cx)
                    right_base = right_base - 50 + cx

            cv2.rectangle(msk, (left_base - 50, y), (left_base + 50, y - 40), (255, 255, 255), 2)
            cv2.rectangle(msk, (right_base - 50, y), (right_base + 50, y - 40), (255, 255, 255), 2)
            y -= 40

        return frame, transformed_frame, mask, msk

    def update_frames(self):
        if not self.stop_event.is_set():
            if not self.paused.is_set():
                frames = self.process_frame()
                if frames[0] is not None:
                    for label, img in zip(self.labels, frames):
                        img = cv2.resize(img, (400, 300))
                        if len(img.shape) == 2:  # If the image is grayscale
                            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
                        else:
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(img)
                        img = ImageTk.PhotoImage(image=img)
                        label.config(image=img)
                        label.image = img
            speed = self.speed_scale.get()
            delay = int(10 / speed)
            self.root.after(delay, self.update_frames)
        else:
            self.cap.release()

    def on_closing(self):
        self.stop_event.set()
        self.root.after(10, self.root.destroy)
        cv2.destroyAllWindows()

    def go_back(self):
        self.stop_event.set()
        self.cap.release()
        cv2.destroyAllWindows()
        self.go_back_callback()

    def pause_video(self):
        self.paused.set()

    def play_video(self):
        self.paused.clear()