from tkinter import ttk

from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkOptionMenu

from app.frames.style import configure_treeview_style
from app.models.products import Products
from app.models.suppliers import Suppliers


class InventoryFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.style = configure_treeview_style()

        self.top_frame = CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.title_label = CTkLabel(
            self.top_frame, text="Product List", font=("Arial Bold", 20)
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
            columns=("ID", "Product", "Stock", "Price", "Total", "Updated", "Supplier"),
            show="headings",
            height=15,
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Updated", text="Updated")
        self.tree.heading("Supplier", text="Supplier")

        self.tree.column("ID", width=70, anchor="center")
        self.tree.column("Product", width=150, anchor="center")
        self.tree.column("Stock", width=100, anchor="center")
        self.tree.column("Price", width=100, anchor="center")
        self.tree.column("Total", width=100, anchor="center")
        self.tree.column("Updated", width=150, anchor="center")
        self.tree.column("Supplier", width=150, anchor="center")

        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.vsb.grid(row=1, column=1, sticky="ns", pady=10)

        # Entry Frame with centering
        self.entry_frame = CTkFrame(self, fg_color="transparent")
        self.entry_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.entry_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        self.product_label = CTkLabel(self.entry_frame, text="Product:")
        self.product_label.grid(row=0, column=0, padx=5, pady=5)
        self.product_entry = CTkEntry(self.entry_frame, width=120)
        self.product_entry.grid(row=0, column=1, padx=5, pady=5)

        self.stock_label = CTkLabel(self.entry_frame, text="Stock:")
        self.stock_label.grid(row=0, column=2, padx=5, pady=5)
        self.stock_entry = CTkEntry(self.entry_frame, width=120)
        self.stock_entry.grid(row=0, column=3, padx=5, pady=5)

        self.price_label = CTkLabel(self.entry_frame, text="Price:")
        self.price_label.grid(row=0, column=4, padx=5, pady=5)
        self.price_entry = CTkEntry(self.entry_frame, width=120)
        self.price_entry.grid(row=0, column=5, padx=5, pady=5)

        self.supplier_label = CTkLabel(self.entry_frame, text="Supplier:")
        self.supplier_label.grid(row=0, column=6, padx=5, pady=5)
        self.supplier_options = CTkOptionMenu(self.entry_frame, width=120)
        self.supplier_options.grid(row=0, column=7, padx=5, pady=5)

        self.hsb.grid(row=3, column=0, sticky="ew", padx=10)

        # Button Frame with centering
        self.button_frame = CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        self.button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.add_button = CTkButton(
            self.button_frame, text="Add Product", command=self.add_item, width=120
        )
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = CTkButton(
            self.button_frame, text="Edit Product", command=self.edit_item, width=120
        )
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = CTkButton(
            self.button_frame,
            text="Delete Product",
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
        self.load_suppliers()

    def clear_entries(self):
        """Clear all entry fields"""
        self.product_entry.delete(0, "end")
        self.stock_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.supplier_options.set("")

    def on_tree_select(self, event):
        """Fill entry boxes when a row is selected"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item)["values"]

            self.clear_entries()

            self.product_entry.insert(0, values[1])
            self.stock_entry.insert(0, str(values[2]))
            self.price_entry.insert(0, str(values[3]).replace("₱", ""))
            self.supplier_options.set(values[6])

    def load_suppliers(self):
        """Load suppliers to the option menu"""
        suppliers = Suppliers().get_all_suppliers()
        if not suppliers:
            return

        supplier_names = [supplier[1] for supplier in suppliers]
        self.supplier_options.configure(values=supplier_names)

    def refresh_tree(self):
        """Refresh the tree with updated data"""
        from datetime import datetime

        products = Products().get_all_products()
        if not products:
            for item in self.tree.get_children():
                self.tree.delete(item)
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in products:
            total = float(row[2]) * float(row[3])
            total_formatted = f"₱{total:.2f}"
            price_formatted = f"₱{float(row[2]):.2f}"

            try:
                date_obj = datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S")
                date_formatted = date_obj.strftime("%d/%m/%Y")
            except (ValueError, TypeError):
                date_formatted = row[5]

            self.tree.insert(
                "",
                "end",
                values=(
                    row[0],  # id
                    row[1],  # name
                    row[3],  # stock
                    price_formatted,  # price
                    total_formatted,  # total
                    date_formatted,  # updated date in DD/MM/YYYY format
                    row[4],  # supplier
                ),
            )

    def add_item(self):
        """Add new item to the tree"""
        product = self.product_entry.get()
        stock = self.stock_entry.get()
        price = self.price_entry.get()
        supplier = self.supplier_options.get()

        if product and stock and price and supplier:
            if Products().add_product(product, price, stock, supplier):
                self.refresh_tree()
                self.load_suppliers()
                self.clear_entries()
            else:
                from tkinter import messagebox

                messagebox.showerror("Cannot Add Product", "Product already exists")

    def edit_item(self):
        """Edit selected item in the tree"""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        values = self.tree.item(item)["values"]
        product_id = values[0]

        product = self.product_entry.get()
        stock = self.stock_entry.get()
        price = self.price_entry.get()
        supplier = self.supplier_options.get()

        if not all([product, stock, price, supplier]):
            return

        try:
            price = float(price)
            stock = int(stock)

            from tkinter import messagebox

            if not messagebox.askyesno(
                "Confirm Edit", "Are you sure you want to edit this item?"
            ):
                if Products().edit_product(product_id, product, price, stock, supplier):
                    self.refresh_tree()
                    self.load_suppliers()
                    self.clear_entries()
                else:
                    messagebox.showerror("Cannot Add Product", "Product already exists")

        except ValueError:
            print("Invalid price or stock value")

    def delete_item(self):
        """Delete selected item from the tree"""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        values = self.tree.item(item)["values"]
        product_id = values[0]

        from tkinter import messagebox

        if messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this item?"
        ):
            if Products().delete_product(product_id):
                self.refresh_tree()
                self.load_suppliers()
                self.clear_entries()
            else:
                messagebox.showerror("Cannot Delete Product", "Product not found")

    def on_search_change(self, _event=None):
        """Handle real-time search as user types"""
        from datetime import datetime

        search_term = self.search_entry.get().lower()
        products = Products().get_all_products()
        if not products:
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in products:
            total = float(row[2]) * float(row[3])
            total_formatted = f"₱{total:.2f}"
            price_formatted = f"₱{float(row[2]):.2f}"

            try:
                date_obj = datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S")
                date_formatted = date_obj.strftime("%d/%m/%Y")
            except (ValueError, TypeError):
                date_formatted = row[5]

            formatted_row = (
                row[0],  # id
                row[1],  # name
                row[3],  # stock
                price_formatted,  # price
                total_formatted,  # total
                date_formatted,  # updated date
                row[4],  # supplier
            )

            search_row = tuple(
                str(value).lower()
                for value in (
                    row[0],  # id
                    row[1],  # name
                    row[3],  # stock
                    price_formatted,  # price
                    total_formatted,  # total
                    date_formatted,  # updated date
                    row[4],  # supplier
                )
            )

            if search_term == "" or any(search_term in field for field in search_row):
                self.tree.insert("", "end", values=formatted_row)
