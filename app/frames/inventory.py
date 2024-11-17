from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry
from tkinter import ttk
from app.frames.style import configure_treeview_style


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
            columns=("Product", "Stock", "Price", "Total", "Updated", "Supplier"),
            show="headings",
            height=15,
        )

        self.tree.heading("Product", text="Product")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Updated", text="Updated")
        self.tree.heading("Supplier", text="Supplier")

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
        self.supplier_entry = CTkEntry(self.entry_frame, width=120)
        self.supplier_entry.grid(row=0, column=7, padx=5, pady=5)

        self.hsb.grid(row=3, column=0, sticky="ew", padx=10)

        self.sample_data = [
            ["Apple", "100", "$1.99", "$199.00", "2024-03-20", "FreshFruit Co"],
            ["Banana", "150", "$0.99", "$148.50", "2024-03-19", "Tropical Imports"],
            ["Orange", "75", "$1.49", "$111.75", "2024-03-18", "CitrusWorld"],
            ["Mango", "50", "$2.99", "$149.50", "2024-03-17", "Tropical Imports"],
            ["Pear", "80", "$1.79", "$143.20", "2024-03-16", "FreshFruit Co"],
        ]

        for item in self.sample_data:
            self.tree.insert("", "end", values=item)

        # Button Frame with centering
        self.button_frame = CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        self.button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.add_button = CTkButton(
            self.button_frame, text="Add Item", command=self.add_item, width=120
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

    def clear_entries(self):
        """Clear all entry fields"""
        self.product_entry.delete(0, "end")
        self.stock_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.supplier_entry.delete(0, "end")

    def on_tree_select(self, event):
        """Fill entry boxes when a row is selected"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item)["values"]

            # Clear existing entries
            self.clear_entries()

            # Fill entries with selected values
            self.product_entry.insert(0, values[0])
            self.stock_entry.insert(0, values[1].replace("$", ""))
            self.price_entry.insert(0, values[2].replace("$", ""))
            self.supplier_entry.insert(0, values[5])

    def add_item(self):
        """Add new item to the tree"""
        # Get values from entries
        product = self.product_entry.get()
        stock = self.stock_entry.get()
        price = self.price_entry.get()

        # Calculate total
        try:
            total = float(stock) * float(price.replace("$", ""))
            total_formatted = f"${total:.2f}"
        except ValueError:
            total_formatted = "$0.00"

        # Format price with $
        if not price.startswith("$"):
            price = f"${price}"

        # Get current date
        from datetime import datetime

        current_date = datetime.now().strftime("%Y-%m-%d")

        supplier = self.supplier_entry.get()

        # Insert into tree
        if product and stock and price and supplier:
            self.tree.insert(
                "",
                "end",
                values=(product, stock, price, total_formatted, current_date, supplier),
            )
            self.clear_entries()

    def edit_item(self):
        selected_items = self.tree.selection()
        if selected_items:
            item_id = selected_items[0]

            # Get values from entries
            product = self.product_entry.get()
            stock = self.stock_entry.get()
            price = self.price_entry.get()

            # Calculate total
            try:
                total = float(stock) * float(price.replace("$", ""))
                total_formatted = f"${total:.2f}"
            except ValueError:
                total_formatted = "$0.00"

            # Format price with $
            if not price.startswith("$"):
                price = f"${price}"

            # Get current date
            from datetime import datetime

            current_date = datetime.now().strftime("%Y-%m-%d")

            supplier = self.supplier_entry.get()

            # Update the item
            if product and stock and price and supplier:
                self.tree.item(
                    item_id,
                    values=(
                        product,
                        stock,
                        price,
                        total_formatted,
                        current_date,
                        supplier,
                    ),
                )
                self.clear_entries()

    def delete_item(self):
        selected_items = self.tree.selection()
        if selected_items:
            for item_id in selected_items:
                self.tree.delete(item_id)
            self.clear_entries()

    def on_search_change(self, _event=None):
        """Handle real-time search as user types"""
        search_term = self.search_entry.get().lower()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for item in self.sample_data:
            if search_term == "" or any(
                search_term in str(value).lower() for value in item
            ):
                self.tree.insert("", "end", values=item)
