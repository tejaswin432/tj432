import customtkinter as ctk
from tkinter import filedialog
import pandas as pd
from data_processor import load_data, validate_columns, process_data, generate_pie_chart
from PIL import Image, ImageTk
import os
import threading
import time
import shutil

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Data Analyzer")
        self.geometry("800x600")

        self.screen1 = ctk.CTkFrame(self)
        self.screen1.pack(fill="both", expand=True)

        self.screen2 = ctk.CTkFrame(self)
        # Screen 2 is not packed initially

        self.car_animation_running = False
        self.setup_screen1()

    def setup_screen1(self):
        # Clear previous widgets
        for widget in self.screen1.winfo_children():
            widget.destroy()

        # Canvas for background and animation
        self.canvas = ctk.CTkCanvas(self.screen1, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        try:
            self.track_image = Image.open("assets/track.png")
            self.track_photo = ImageTk.PhotoImage(self.track_image.resize((800, 600), Image.Resampling.LANCZOS))
            self.canvas.create_image(0, 0, anchor="nw", image=self.track_photo)
        except FileNotFoundError:
            self.canvas.create_text(400, 100, text="Add 'track.png' to 'assets' folder", font=("Arial", 20), fill="white")


        try:
            self.car_image = Image.open("assets/car.png")
            self.car_photo = ImageTk.PhotoImage(self.car_image.resize((150, 75), Image.Resampling.LANCZOS))
            self.car = self.canvas.create_image(325, 250, anchor="nw", image=self.car_photo)
        except FileNotFoundError:
            self.canvas.create_text(400, 300, text="Add 'car.png' to 'assets' folder", font=("Arial", 20), fill="white")

        self.drop_label = ctk.CTkLabel(self.screen1, text="Drop your file here or click to upload", bg_color="transparent", fg_color="#4a4a4a", corner_radius=10)
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        self.upload_button = ctk.CTkButton(self.screen1, text="Upload File", command=self.upload_file)
        self.upload_button.place(relx=0.5, rely=0.58, anchor="center")


    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")]
        )
        if file_path:
            self.start_car_animation()
            # Run data processing in a separate thread to keep the UI responsive
            threading.Thread(target=self.process_file_thread, args=(file_path,)).start()

    def process_file_thread(self, file_path):
        try:
            df = load_data(file_path)
            if not validate_columns(df):
                self.show_error("Low Fuel: 'Description' and 'Comments' columns are required.")
                self.stop_car_animation()
                return

            self.processed_df = process_data(df.copy())
            self.stop_car_animation()
            # Schedule screen2 to be shown in the main thread
            self.after(0, self.show_screen2)

        except Exception as e:
            self.stop_car_animation()
            self.show_error(f"An error occurred: {e}")

    def start_car_animation(self):
        self.car_animation_running = True
        self.upload_button.configure(state="disabled")
        self.animate_car()

    def stop_car_animation(self):
        self.car_animation_running = False
        self.upload_button.configure(state="normal")


    def animate_car(self):
        if self.car_animation_running:
            # Simple placeholder animation: move car slightly
            self.canvas.move(self.car, 2, 0)
            x, _ = self.canvas.coords(self.car)
            if x > 800:
                self.canvas.move(self.car, -850, 0) # Reset position
            self.after(20, self.animate_car)

    def show_error(self, message):
        # In a real app, this would be a popup on the car
        error_label = ctk.CTkLabel(self.screen1, text=message, text_color="red", fg_color="#4a4a4a", corner_radius=6)
        error_label.place(relx=0.5, rely=0.65, anchor="center")
        self.after(3000, error_label.destroy)

    def show_screen2(self):
        self.screen1.pack_forget()
        self.screen2.pack(fill="both", expand=True)
        self.setup_screen2()

    def setup_screen2(self):
        # Clear previous widgets
        for widget in self.screen2.winfo_children():
            widget.destroy()

        # Split screen 2 into two frames
        left_frame = ctk.CTkFrame(self.screen2)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = ctk.CTkFrame(self.screen2)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Left side: Pie chart
        pie_chart_path = "pie_chart.png"
        generate_pie_chart(self.processed_df, pie_chart_path)

        try:
            pie_image = Image.open(pie_chart_path)
            pie_photo = ImageTk.PhotoImage(pie_image)

            chart_label = ctk.CTkLabel(left_frame, image=pie_photo, text="")
            chart_label.image = pie_photo
            chart_label.pack(pady=10, expand=True)
        except FileNotFoundError:
            chart_label = ctk.CTkLabel(left_frame, text="Could not load pie chart.")
            chart_label.pack(pady=10, expand=True)


        # Right side: Download and email options
        download_report_button = ctk.CTkButton(right_frame, text="Download Report", command=self.download_report)
        download_report_button.pack(pady=10, padx=20, fill="x")

        download_chart_button = ctk.CTkButton(right_frame, text="Download Pie Chart", command=self.download_pie_chart)
        download_chart_button.pack(pady=10, padx=20, fill="x")

        email_label = ctk.CTkLabel(right_frame, text="Email Report:")
        email_label.pack(pady=(20, 5), padx=20, anchor="w")
        self.email_entry = ctk.CTkEntry(right_frame, placeholder_text="Enter your email")
        self.email_entry.pack(pady=5, padx=20, fill="x")
        send_button = ctk.CTkButton(right_frame, text="Send", command=self.send_email)
        send_button.pack(pady=5, padx=20, fill="x")

        # Close button
        close_button = ctk.CTkButton(self.screen2, text="X", command=self.show_screen1_setup, width=30, height=30, corner_radius=15)
        close_button.place(relx=0.98, rely=0.02, anchor="ne")

    def download_report(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            self.processed_df.to_excel(save_path, index=False)

    def download_pie_chart(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            try:
                shutil.copy("pie_chart.png", save_path)
            except Exception as e:
                self.show_error(f"Error saving chart: {e}")


    def send_email(self):
        # Placeholder for email functionality
        email = self.email_entry.get()
        print(f"Sending report to {email}")


    def show_screen1_setup(self):
        self.screen2.pack_forget()
        self.screen1.pack(fill="both", expand=True)
        self.setup_screen1()

if __name__ == "__main__":
    app = App()
    app.mainloop()