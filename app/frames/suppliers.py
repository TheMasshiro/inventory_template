from tkinter import ttk

from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel

from app.frames.style import configure_treeview_style
from app.models.suppliers import Suppliers


class SuppliersFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.style = configure_treeview_style()

        self.top_frame = CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.title_label = CTkLabel(
            self.top_frame, text="Supplier List", font=("Arial Bold", 20)
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
            columns=("ID", "Company", "Supplier Name", "Email", "Contact No."),
            show="headings",
            height=15,
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Company", text="Company")
        self.tree.heading("Supplier Name", text="Supplier Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Contact No.", text="Contact No.")

        self.tree.column("ID", width=70, anchor="center")
        self.tree.column("Company", width=150, anchor="center")
        self.tree.column("Supplier Name", width=100, anchor="center")
        self.tree.column("Email", width=100, anchor="center")
        self.tree.column("Contact No.", width=100, anchor="center")

        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.vsb.grid(row=1, column=1, sticky="ns", pady=10)

        # Entry Frame with centering
        self.entry_frame = CTkFrame(self, fg_color="transparent")
        self.entry_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.entry_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        self.company_label = CTkLabel(self.entry_frame, text="Company:")
        self.company_label.grid(row=0, column=0, padx=5, pady=5)
        self.company_entry = CTkEntry(self.entry_frame, width=120)
        self.company_entry.grid(row=0, column=1, padx=5, pady=5)

        self.supplier_label = CTkLabel(self.entry_frame, text="Supplier:")
        self.supplier_label.grid(row=0, column=2, padx=5, pady=5)
        self.supplier_entry = CTkEntry(self.entry_frame, width=120)
        self.supplier_entry.grid(row=0, column=3, padx=5, pady=5)

        self.email_label = CTkLabel(self.entry_frame, text="Email:")
        self.email_label.grid(row=0, column=4, padx=5, pady=5)
        self.email_entry = CTkEntry(self.entry_frame, width=120)
        self.email_entry.grid(row=0, column=5, padx=5, pady=5)

        self.contact_label = CTkLabel(self.entry_frame, text="Contact No.:")
        self.contact_label.grid(row=0, column=6, padx=5, pady=5)
        self.contact_entry = CTkEntry(self.entry_frame, width=120)
        self.contact_entry.grid(row=0, column=7, padx=5, pady=5)

        self.hsb.grid(row=3, column=0, sticky="ew", padx=10)

        # Button Frame with centering
        self.button_frame = CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        self.button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.add_button = CTkButton(
            self.button_frame, text="Add Supplier", command=self.add_supplier, width=120
        )
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = CTkButton(
            self.button_frame, text="Edit Supplier", command=self.edit_item, width=120
        )
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = CTkButton(
            self.button_frame,
            text="Delete Supplier",
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
        self.company_entry.delete(0, "end")
        self.supplier_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.contact_entry.delete(0, "end")

    def on_tree_select(self, event):
        """Fill entry boxes when a row is selected"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item)["values"]

            self.clear_entries()

            self.company_entry.insert(0, values[1])
            self.supplier_entry.insert(0, values[2])
            self.email_entry.insert(0, values[3])
            self.contact_entry.insert(0, values[4])

    def refresh_tree(self):
        """Refresh the tree with updated data"""
        all_suppliers = Suppliers().get_all_suppliers()
        if not all_suppliers:
            for item in self.tree.get_children():
                self.tree.delete(item)
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in all_suppliers:
            formatted_row = (
                row[0],  # id
                row[1],  # company
                row[3],  # supplier
                row[2],  # email
                row[4],  # contact
            )
            self.tree.insert("", "end", values=formatted_row)

    def add_supplier(self):
        """Add new supplier to the tree"""
        company = self.company_entry.get()
        supplier = self.supplier_entry.get()
        email = self.email_entry.get()
        contact = self.contact_entry.get()
        from tkinter import messagebox

        valid_email = "@" in email and "." in email
        valid_contact = (
            contact.isdigit()
            and len(contact) == 11
            and contact[0] == "0"
            and contact[1] == "9"
        )

        if not valid_email and not valid_contact:
            messagebox.showerror("Invalid Email", "Invalid email and contact number")
        else:
            if company and supplier and email and contact:
                if Suppliers().add_supplier(company, email, supplier, contact):
                    self.refresh_tree()
                    self.clear_entries()
                else:
                    messagebox.showerror(
                        "Cannot Add Supplier", "Supplier already exists"
                    )

    def edit_item(self):
        """Edit selected supplier in the tree"""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        values = self.tree.item(item)["values"]
        supplier_id = values[0]

        company = self.company_entry.get()
        supplier = self.supplier_entry.get()
        email = self.email_entry.get()
        contact = self.contact_entry.get()
        from tkinter import messagebox

        valid_email = "@" in email and "." in email
        valid_contact = (
            contact.isdigit()
            and len(contact) == 11
            and contact[0] == "0"
            and contact[1] == "9"
        )

        if valid_email and valid_contact:
            messagebox.showerror("Invalid Email", "Invalid email and contact number")
        else:
            if not all([company, supplier, email, contact]):
                return

            try:
                email = float(email)
                supplier = int(supplier)

                if messagebox.askyesno(
                    "Confirm Edit", "Are you sure you want to edit this item?"
                ):
                    if Suppliers().edit_supplier(
                        supplier_id, company, email, supplier, contact
                    ):
                        self.refresh_tree()
                        self.clear_entries()
                    else:
                        messagebox.showerror(
                            "Cannot Edit Supplier", "Supplier not found"
                        )

            except ValueError:
                messagebox.showerror(
                    "Invalid Input", "Invalid email and contact number"
                )

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
            if Suppliers().delete_supplier(supplier_id):
                self.refresh_tree()
                self.clear_entries()
            else:
                messagebox.showerror("Cannot Delete Product", "Product not found")

    def on_search_change(self, _event=None):
        """Handle real-time search as user types"""
        search_term = self.search_entry.get().lower()
        all_supplier = Suppliers().get_all_suppliers()
        if not all_supplier:
            for item in self.tree.get_children():
                self.tree.delete(item)
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in all_supplier:
            formatted_row = (
                row[0],  # id
                row[1],  # company
                row[3],  # supplier
                row[2],  # email
                row[4],  # contact
            )

            search_row = tuple(
                str(value).lower()
                for value in (
                    row[0],  # id
                    row[1],  # company
                    row[3],  # supplier
                    row[2],  # email
                    row[4],  # contact
                )
            )

            if search_term == "" or any(search_term in field for field in search_row):
                self.tree.insert("", "end", values=formatted_row)
