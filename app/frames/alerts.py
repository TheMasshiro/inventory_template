from tkinter import ttk

import customtkinter
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkOptionMenu

from app.frames.style import configure_treeview_style
from app.models.products import Products


class AlertsFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.style = configure_treeview_style()

        self.top_frame = CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.title_label = CTkLabel(
            self.top_frame, text="Inventory Alerts", font=("Arial Bold", 20)
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=5)

        self.search_entry = CTkEntry(
            self.top_frame,
            placeholder_text="Search inventory...",
        )
        self.search_entry.grid(row=0, column=1, sticky="e", padx=5)

        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Product", "Stock", "Status"),
            show="headings",
            height=15,
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=70, anchor="center")
        self.tree.column("Product", width=150, anchor="center")
        self.tree.column("Stock", width=100, anchor="center")
        self.tree.column("Status", width=100, anchor="center")

        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.vsb.grid(row=1, column=1, sticky="ns", pady=10)

        self.hsb.grid(row=3, column=0, sticky="ew", padx=10)

        # Button Frame with centering
        self.button_frame = CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.refresh_button = CTkButton(
            self.button_frame, text="Edit Sale", command=self.refresh_all, width=120
        )
        self.refresh_button.grid(row=0, column=0, padx=5)

        # Load Data
        self.refresh_tree()

    def refresh_all(self):
        """Refresh all data in the frame"""
        self.refresh_tree()

    def refresh_tree(self):
        """Refresh the tree with updated data"""
        all_alerts = Products().get_low_stock_products()
        if not all_alerts:
            for item in self.tree.get_children():
                self.tree.delete(item)
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in all_alerts:
            formatted_row = (
                row[0],  # id
                row[2],  # product
                row[4],  # stock
            )
            if row[4] < 10:
                formatted_row += ("Low Stock",)
            elif row[4] <= 0:
                formatted_row += ("Out of Stock",)
            self.tree.insert("", "end", values=formatted_row)

    def on_search_change(self, _event=None):
        """Handle real-time search as user types"""
        search_term = self.search_entry.get().lower()
        all_alerts = Products().get_low_stock_products()
        if not all_alerts:
            for item in self.tree.get_children():
                self.tree.delete(item)
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in all_alerts:
            formatted_row = (
                row[0],  # id
                row[2],  # product
                row[4],  # stock
            )
            if row[4] < 10:
                formatted_row += ("Low Stock",)
            elif row[4] <= 0:
                formatted_row += ("Out of Stock",)

            search_row = tuple(
                str(value).lower()
                for value in (
                    row[0],  # id
                    row[2],  # product
                    row[4],  # stock
                )
            )

            if search_term == "" or any(search_term in field for field in search_row):
                self.tree.insert("", "end", values=formatted_row)
