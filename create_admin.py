from getpass import getpass

from app.database.database import SessionLocal
from app.database.models import User, UserRole
from app.core.security import hash_password


def create_admin():
    name = input("Enter admin name: ").strip()
    email = input("Enter admin email: ").strip().lower()
    password = getpass("Enter admin password: ")
    confirm_password = getpass("Confirm admin password: ")

    if not name or not email or not password:
        print("Error: All fields are required.")
        return

    if password != confirm_password:
        print("Error: Passwords do not match.")
        return

    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            print("Error: A user with this email already exists.")
            return

        admin = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=UserRole.ADMIN
        )

        db.add(admin)
        db.commit()

        print("Admin account created successfully!")

    except Exception:
        db.rollback()
        print("Error: Could not create admin account.")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()