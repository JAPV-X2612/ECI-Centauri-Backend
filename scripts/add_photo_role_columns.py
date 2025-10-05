"""
Script to add photo_url and role columns to users table.

Run this script once to update the database schema.
"""

from sqlalchemy import text
from app.database import engine


def add_columns():
    """Add photo_url and role columns to users table."""
    with engine.connect() as connection:
        try:
            # Add photo_url column
            connection.execute(text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS photo_url TEXT"
            ))
            print("✓ Added photo_url column")

            # Add role column
            connection.execute(text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50)"
            ))
            print("✓ Added role column")

            connection.commit()
            print("\n✅ Database migration completed successfully!")

        except Exception as e:
            print(f"❌ Error during migration: {e}")
            connection.rollback()


if __name__ == "__main__":
    print("Starting database migration...\n")
    add_columns()
