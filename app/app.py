import os

import customtkinter
from PIL import Image

from app.frames.alerts import AlertsFrame
from app.frames.inventory import InventoryFrame
from app.frames.sales import SalesFrame
from app.frames.suppliers import SuppliersFrame


class AppTop(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Theme configuration

        self.title("Skibidi Inventory Management")
        self.geometry("700x450")

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # load images
        self._load_images()

        # create navigation frame
        self._create_navigation_frame()

        # Create content frames
        self.inventory_frame = InventoryFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        self.suppliers_frame = SuppliersFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        self.sales_frame = SalesFrame(self, corner_radius=0, fg_color="transparent")

        self.alerts_frame = AlertsFrame(self, corner_radius=0, fg_color="transparent")

        # Select default frame
        self.select_frame_by_name("inventory")

    def _load_images(self):
        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_images"
        )
        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
            size=(26, 26),
        )
        self.inventory_image = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "home_light.png")),
            size=(20, 20),
        )
        self.suppliers_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20)
        )
        self.sales_image = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
            size=(20, 20),
        )
        self.alerts_image = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")),
            size=(20, 20),
        )

    def _create_navigation_frame(self):
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0, height=60)
        self.navigation_frame.grid(row=0, column=0, sticky="ew")

        self.navigation_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Logo and title on the left
        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="   Inventory",
            image=self.logo_image,
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=10)

        # Navigation buttons horizontally aligned
        self.inventory_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=6,
            height=40,
            border_spacing=10,
            text="Inventory",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.inventory_image,
            compound="top",  # Image above text
            command=self.inventory_event,
        )
        self.inventory_button.grid(row=0, column=1, padx=10, pady=5)

        self.suppliers_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=6,
            height=40,
            border_spacing=10,
            text="Suppliers",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.suppliers_image,
            compound="top",  # Image above text
            command=self.suppliers_event,
        )
        self.suppliers_button.grid(row=0, column=2, padx=10, pady=5)

        self.sales_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=6,
            height=40,
            border_spacing=10,
            text="Sales",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.sales_image,
            compound="top",  # Image above text
            command=self.sales_event,
        )
        self.sales_button.grid(row=0, column=3, padx=10, pady=5)

        self.alerts_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=6,
            height=40,
            border_spacing=10,
            text="Alerts",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.alerts_image,
            compound="top",  # Image above text
            command=self.alerts_event,
        )
        self.alerts_button.grid(row=0, column=4, padx=10, pady=5)

    def select_frame_by_name(self, name):
        # Configure button colors based on selection
        self.inventory_button.configure(
            fg_color=("gray75", "gray25") if name == "inventory" else "transparent"
        )
        self.suppliers_button.configure(
            fg_color=("gray75", "gray25") if name == "suppliers" else "transparent"
        )
        self.sales_button.configure(
            fg_color=("gray75", "gray25") if name == "sales" else "transparent"
        )
        self.alerts_button.configure(
            fg_color=("gray75", "gray25") if name == "alerts" else "transparent"
        )

        # Show selected frame
        frames = {
            "inventory": self.inventory_frame,
            "suppliers": self.suppliers_frame,
            "sales": self.sales_frame,
            "alerts": self.alerts_frame,
        }

        for frame_name, frame in frames.items():
            if name == frame_name:
                frame.grid(
                    row=1, column=0, sticky="nsew"
                )  # Content appears below navigation
            else:
                frame.grid_forget()

    def inventory_event(self):
        self.select_frame_by_name("inventory")

    def suppliers_event(self):
        self.select_frame_by_name("suppliers")

    def sales_event(self):
        self.select_frame_by_name("sales")

    def alerts_event(self):
        self.select_frame_by_name("alerts")


class AppRight(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Skibidi Inventory Management")
        self.geometry("700x450")

        # set grid layout 2x1
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # load images
        self._load_images()

        # create navigation frame
        self._create_navigation_frame()

        # Create content frames
        self.inventory_frame = InventoryFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        self.suppliers_frame = SuppliersFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        self.sales_frame = SalesFrame(self, corner_radius=0, fg_color="transparent")

        self.alerts_frame = AlertsFrame(self, corner_radius=0, fg_color="transparent")

        # Select default frame
        self.select_frame_by_name("inventory")

    def _load_images(self):
        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_images"
        )
        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
            size=(26, 26),
        )
        self.inventory_image = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "home_light.png")),
            size=(20, 20),
        )
        self.suppliers_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20)
        )
        self.sales_image = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
            size=(20, 20),
        )
        self.alerts_image = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")),
            size=(20, 20),
        )

    def _create_navigation_frame(self):
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=1, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="   Inventory",
            image=self.logo_image,
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.inventory_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Inventory",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.inventory_image,
            anchor="w",
            command=self.inventory_event,
        )
        self.inventory_button.grid(row=1, column=0, sticky="ew")

        self.suppliers_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Suppliers",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.alerts_image,
            anchor="w",
            command=self.suppliers_event,
        )
        self.suppliers_button.grid(row=2, column=0, sticky="ew")

        self.sales_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Sales",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.sales_image,
            anchor="w",
            command=self.sales_event,
        )
        self.sales_button.grid(row=3, column=0, sticky="ew")

        self.alerts_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Alerts",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.alerts_image,
            anchor="w",
            command=self.alerts_event,
        )
        self.alerts_button.grid(row=4, column=0, sticky="ew")

    def select_frame_by_name(self, name):
        self.inventory_button.configure(
            fg_color=("gray75", "gray25") if name == "inventory" else "transparent"
        )
        self.suppliers_button.configure(
            fg_color=("gray75", "gray25") if name == "suppliers" else "transparent"
        )
        self.sales_button.configure(
            fg_color=("gray75", "gray25") if name == "sales" else "transparent"
        )
        self.alerts_button.configure(
            fg_color=("gray75", "gray25") if name == "alerts" else "transparent"
        )

        # show selected frame
        frames = {
            "inventory": self.inventory_frame,
            "suppliers": self.suppliers_frame,
            "sales": self.sales_frame,
            "alerts": self.alerts_frame,
        }

        for frame_name, frame in frames.items():
            if name == frame_name:
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                frame.grid_forget()

    def inventory_event(self):
        self.select_frame_by_name("inventory")

    def suppliers_event(self):
        self.select_frame_by_name("suppliers")

    def sales_event(self):
        self.select_frame_by_name("sales")

    def alerts_event(self):
        self.select_frame_by_name("alerts")


class AppLeft(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Skibidi Inventory Management")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images
        self._load_images()

        # create navigation frame
        self._create_navigation_frame()

        # Create content frames
        self.inventory_frame = InventoryFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        self.suppliers_frame = SuppliersFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        self.sales_frame = SalesFrame(self, corner_radius=0, fg_color="transparent")

        self.alerts_frame = AlertsFrame(self, corner_radius=0, fg_color="transparent")

        # Select default frame
        self.select_frame_by_name("inventory")

    def _load_images(self):
        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_images"
        )
        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
            size=(26, 26),
        )
        self.inventory_image = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "home_light.png")),
            size=(20, 20),
        )
        self.suppliers_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20)
        )
        self.sales_image = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
            size=(20, 20),
        )
        self.alerts_image = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")),
            size=(20, 20),
        )

    def _create_navigation_frame(self):
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="   Inventory",
            image=self.logo_image,
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.inventory_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Inventory",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.inventory_image,
            anchor="w",
            command=self.inventory_event,
        )
        self.inventory_button.grid(row=1, column=0, sticky="ew")

        self.suppliers_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Suppliers",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.alerts_image,
            anchor="w",
            command=self.suppliers_event,
        )
        self.suppliers_button.grid(row=2, column=0, sticky="ew")

        self.sales_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Sales",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.sales_image,
            anchor="w",
            command=self.sales_event,
        )
        self.sales_button.grid(row=3, column=0, sticky="ew")

        self.alerts_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Alerts",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.alerts_image,
            anchor="w",
            command=self.alerts_event,
        )
        self.alerts_button.grid(row=4, column=0, sticky="ew")

    def select_frame_by_name(self, name):
        self.inventory_button.configure(
            fg_color=("gray75", "gray25") if name == "inventory" else "transparent"
        )
        self.suppliers_button.configure(
            fg_color=("gray75", "gray25") if name == "suppliers" else "transparent"
        )
        self.sales_button.configure(
            fg_color=("gray75", "gray25") if name == "sales" else "transparent"
        )
        self.alerts_button.configure(
            fg_color=("gray75", "gray25") if name == "alerts" else "transparent"
        )

        # show selected frame
        frames = {
            "inventory": self.inventory_frame,
            "suppliers": self.suppliers_frame,
            "sales": self.sales_frame,
            "alerts": self.alerts_frame,
        }

        for frame_name, frame in frames.items():
            if name == frame_name:
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()

    def inventory_event(self):
        self.select_frame_by_name("inventory")

    def suppliers_event(self):
        self.select_frame_by_name("suppliers")

    def sales_event(self):
        self.select_frame_by_name("sales")

    def alerts_event(self):
        self.select_frame_by_name("alerts")
