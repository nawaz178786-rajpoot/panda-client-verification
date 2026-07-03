import os
import shutil
from datetime import datetime

# Database location
DB_FILE = "data/clients.db"

# Backup folder
BACKUP_FOLDER = "backups"

# Number of backups to keep
MAX_BACKUPS = 30


def create_backup():
    """
    Create a timestamped backup of the SQLite database.
    """

    # Create backup folder if it doesn't exist
    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    # Check database exists
    if not os.path.exists(DB_FILE):
        print("❌ Database not found. Backup skipped.")
        return None

    # Backup filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_name = f"clients_{timestamp}.db"

    backup_path = os.path.join(
        BACKUP_FOLDER,
        backup_name,
    )

    # Copy database
    shutil.copy2(DB_FILE, backup_path)

    print(f"✅ Backup created: {backup_name}")

    # Delete old backups
    cleanup_backups()

    return backup_path


def cleanup_backups():
    """
    Keep only the newest MAX_BACKUPS files.
    """

    files = [
        os.path.join(BACKUP_FOLDER, f)
        for f in os.listdir(BACKUP_FOLDER)
        if f.endswith(".db")
    ]

    files.sort(
        key=os.path.getmtime,
        reverse=True,
    )

    old_files = files[MAX_BACKUPS:]

    for file in old_files:
        try:
            os.remove(file)
            print(f"🗑 Deleted old backup: {os.path.basename(file)}")
        except Exception as e:
            print(f"❌ Couldn't delete {file}: {e}")