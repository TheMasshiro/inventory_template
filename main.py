from app.app import (
    AppRight,
)  # Change this to AppLeft, AppRight, or AppTop for navigation
from app.db import init_db

if __name__ == "__main__":
    init_db()
    app = AppRight()  # Change this to AppLeft, AppRight, or AppTop for navigation
    app.mainloop()
