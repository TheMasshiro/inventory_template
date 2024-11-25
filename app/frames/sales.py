from tkinter import ttk

import customtkinter
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkOptionMenu

from app.frames.style import configure_treeview_style
from app.models.sales import Sales


class SalesFrame(customtkinter.CTkFrame):
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
        self.tree.heading("Sold", text="Sold")
        self.tree.heading("Supplier", text="Supplier")

        self.tree.column("ID", width=70, anchor="center")
        self.tree.column("Product", width=150, anchor="center")
        self.tree.column("Sold", width=100, anchor="center")
        self.tree.column("Supplier", width=100, anchor="center")

        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.vsb.grid(row=1, column=1, sticky="ns", pady=10)

        # Entry Frame with centering
        self.entry_frame = CTkFrame(self, fg_color="transparent")
        self.entry_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.entry_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # Get Product Name
        product_names = Sales().get_all_product_name()
        if not product_names:
            product_names = []
        product_names = [product[0] for product in product_names]

        if not product_names:
            product_names = ["No Products"]

        self.product_name = CTkLabel(self.entry_frame, text="Product:")
        self.product_name.grid(row=0, column=0, padx=5, pady=5)
        self.product_options = CTkOptionMenu(
            self.entry_frame, values=product_names, width=120
        )
        self.product_options.grid(row=0, column=1, padx=5, pady=5)

        self.sold_label = CTkLabel(self.entry_frame, text="Sold:")
        self.sold_label.grid(row=0, column=2, padx=5, pady=5)
        self.sold_entry = CTkEntry(self.entry_frame, width=120)
        self.sold_entry.grid(row=0, column=3, padx=5, pady=5)

        self.hsb.grid(row=3, column=0, sticky="ew", padx=10)

        # Button Frame with centering
        self.button_frame = CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        self.button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.add_button = CTkButton(
            self.button_frame, text="Add Item", command=self.add_supplier, width=120
        )
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = CTkButton(
            self.button_frame, text="Edit Item", command=self.edit_item, width=120
        )
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = CTkButton(
            self.button_frame,
            text="Delete Item",
            command=self.delete_item,
            fg_color="red",
            hover_color="darkred",
            width=120,
        )
        self.delete_button.grid(row=0, column=2, padx=5)

        self.clear_button = CTkButton(
            self.button_frame,
            text="Clear Fields",
            command=self.clear_entries,
            width=120,
        )
        self.clear_button.grid(row=0, column=3, padx=5)

        # Bind selection event to tree
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Load Data
        self.refresh_tree()

    def clear_entries(self):
        """Clear all entry fields"""
        self.product_options.set("")
        self.sold_entry.delete(0, "end")

    def on_tree_select(self, event):
        """Fill entry boxes when a row is selected"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item)["values"]

            self.clear_entries()

            self.product_options.set(values[1])
            self.sold_entry.insert(0, str(values[2]))

    def refresh_tree(self):
        """Refresh the tree with updated data"""
        all_sales = Sales().get_all_sales()
        if not all_sales:
            for item in self.tree.get_children():
                self.tree.delete(item)
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in all_sales:
            formatted_row = (
                row[0],  # id
                row[1],  # product
                row[2],  # sold
                row[3],  # supplier
            )
            self.tree.insert("", "end", values=formatted_row)

    def add_supplier(self):
        """Add new supplier to the tree"""
        product_name = self.product_options.get()
        sold = self.sold_entry.get()
        from tkinter import messagebox

        try:
            sold = int(sold)
            if product_name and sold:
                if Sales().add_sales(product_name, sold):
                    self.refresh_tree()
                    self.clear_entries()
                else:
                    messagebox.showerror("Cannot Add Sales", "Sales already exists")
        except ValueError:
            messagebox.showerror("Invalid Input", "Invalid sold number")

    def edit_item(self):
        """Edit selected sales in the tree"""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        values = self.tree.item(item)["values"]
        supplier_id = values[0]

        sold = self.sold_entry.get()
        from tkinter import messagebox

        if not sold:
            return

        try:
            sold = int(sold)
            if not messagebox.askyesno(
                "Confirm Edit", "Are you sure you want to edit this item?"
            ):
                if Sales().edit_sales(
                    supplier_id,
                    sold,
                ):
                    self.refresh_tree()
                    self.clear_entries()
                else:
                    messagebox.showerror("Cannot Edit Sales", "Sales not found")

        except ValueError:
            messagebox.showerror("Invalid Input", "Invalid email and contact number")

    def delete_item(self):
        """Delete selected supplier from the tree"""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        values = self.tree.item(item)["values"]
        supplier_id = values[0]

        from tkinter import messagebox

        if messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this item?"
        ):
            if Sales().delete_sales(supplier_id):
                self.refresh_tree()
                self.clear_entries()
            else:
                messagebox.showerror("Cannot Delete Product", "Product not found")

    def on_search_change(self, _event=None):
        """Handle real-time search as user types"""
        search_term = self.search_entry.get().lower()
        all_sales = Sales().get_all_sales()
        if not all_sales:
            for item in self.tree.get_children():
                self.tree.delete(item)
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in all_sales:
            formatted_row = (
                row[0],  # id
                row[1],  # product
                row[2],  # sold
                row[3],  # supplier
            )

            search_row = tuple(
                str(value).lower()
                for value in (
                    row[0],  # id
                    row[1],  # product
                    row[2],  # sold
                    row[3],  # supplier
                )
            )

            if search_term == "" or any(search_term in field for field in search_row):
                self.tree.insert("", "end", values=formatted_row)
