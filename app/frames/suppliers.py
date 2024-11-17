import customtkinter
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry
from app.frames.style import configure_treeview_style
from tkinter import ttk


class SuppliersFrame(customtkinter.CTkFrame):
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
            columns=("Product", "Stock", "Price", "Total", "Updated"),
            show="headings",
            height=15,
        )

        self.tree.heading("Product", text="Product")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Updated", text="Updated")

        self.tree.column("Product", width=150)
        self.tree.column("Stock", width=100)
        self.tree.column("Price", width=100)
        self.tree.column("Total", width=100)
        self.tree.column("Updated", width=150)

        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.vsb.grid(row=1, column=1, sticky="ns", pady=10)
        self.hsb.grid(row=2, column=0, sticky="ew", padx=10)

        self.sample_data = [
            ["Apple", "100", "$1.99", "$199.00", "2024-03-20"],
            ["Banana", "150", "$0.99", "$148.50", "2024-03-19"],
            ["Orange", "75", "$1.49", "$111.75", "2024-03-18"],
            ["Mango", "50", "$2.99", "$149.50", "2024-03-17"],
            ["Pear", "80", "$1.79", "$143.20", "2024-03-16"],
        ]

        for item in self.sample_data:
            self.tree.insert("", "end", values=item)

        self.button_frame = CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

        self.add_button = CTkButton(
            self.button_frame, text="Add Item", command=self.add_item
        )
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = CTkButton(
            self.button_frame, text="Edit Item", command=self.edit_item
        )
        self.edit_button.grid(row=0, column=1, padx=5)

        # Delete button
        self.delete_button = CTkButton(
            self.button_frame,
            text="Delete Item",
            command=self.delete_item,
            fg_color="red",
            hover_color="darkred",
        )
        self.delete_button.grid(row=0, column=2, padx=5)

    def add_item(self):
        print("Add item clicked")

    def edit_item(self):
        selected_items = self.tree.selection()
        if selected_items:
            item_id = selected_items[0]
            values = self.tree.item(item_id)["values"]
            print("Editing item:")
            print(f"Product: {values[0]}")
            print(f"Stock: {values[1]}")
            print(f"Price: {values[2]}")
            print(f"Total: {values[3]}")
            print(f"Updated: {values[4]}")

    def delete_item(self):
        selected_items = self.tree.selection()
        if selected_items:
            for item_id in selected_items:
                self.tree.delete(item_id)

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
