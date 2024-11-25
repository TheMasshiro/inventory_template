from tkinter import ttk


def configure_treeview_style():
    style = ttk.Style()

    style.theme_use("default")

    style.configure(
        "Treeview",
        background="#2a2d2e",
        foreground="white",
        rowheight=25,
        fieldbackground="#343638",
        bordercolor="#343638",
        borderwidth=0,
    )
    style.map("Treeview", background=[("selected", "#22559b")])

    style.configure(
        "Treeview.Heading", background="#565b5e", foreground="white", relief="flat"
    )
    style.map("Treeview.Heading", background=[("active", "#3484F0")])

    return style


def configure_treeview_light_style():
    style = ttk.Style()

    style.theme_use("default")

    style.configure(
        "Treeview",
        background="white",
        foreground="black",
        rowheight=25,
        fieldbackground="white",
        bordercolor="white",
        borderwidth=0,
    )
    style.map("Treeview", background=[("selected", "#22559b")])

    style.configure(
        "Treeview.Heading", background="#f0f0f0", foreground="black", relief="flat"
    )
    style.map("Treeview.Heading", background=[("active", "#3484F0")])

    return style
