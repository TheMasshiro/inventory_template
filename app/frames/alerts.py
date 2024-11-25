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
            self.top_frame, text="Sales List", font=("Arial Bold", 20)
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
            columns=("ID", "Product", "Sold", "Supplier"),
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

        # Entry Frame with centering
        self.entry_frame = CTkFrame(self, fg_color="transparent")
        self.entry_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.entry_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        self.product_name = CTkLabel(self.entry_frame, text="Product:")
        self.product_name.grid(row=0, column=0, padx=5, pady=5)
        self.product_options = CTkOptionMenu(self.entry_frame, width=120)
        self.product_options.grid(row=0, column=1, padx=5, pady=5)

        self.sold_label = CTkLabel(self.entry_frame, text="Sold:")
        self.sold_label.grid(row=0, column=2, padx=5, pady=5)
        self.sold_entry = CTkEntry(self.entry_frame, width=120)
        self.sold_entry.grid(row=0, column=3, padx=5, pady=5)

        self.hsb.grid(row=3, column=0, sticky="ew", padx=10)

        # Load Data
        self.refresh_tree()

    def refresh_all(self):
        """Refresh all data in the frame"""
        self.refresh_tree()
        self.clear_entries()

    def clear_entries(self):
        """Clear all entry fields"""
        self.product_options.set("")
        self.sold_entry.delete(0, "end")

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
            self.tree.insert("", "end", values=formatted_row)

    def on_tree_select(self, event):
        """Fill entry boxes when a row is selected"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item)["values"]

            self.clear_entries()

            self.product_options.set(values[1])
            self.sold_entry.insert(0, str(values[2]))

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
