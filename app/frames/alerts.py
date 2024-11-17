import customtkinter
from PIL import Image
import os


class AlertsFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        # Add widgets
        self.label = customtkinter.CTkLabel(
            self,
            text="Inventory Alerts",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.label.grid(row=0, column=0, padx=20, pady=20)
