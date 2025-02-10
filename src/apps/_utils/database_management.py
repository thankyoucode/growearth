import os
import sqlite3
import shutil
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    @staticmethod
    def backup_sqlite_database(db_path=None):
        """
        Create periodic backups of SQLite database
        """
        if not db_path:
            db_path = settings.DATABASES['default']['NAME']
        
        backup_dir = os.path.join(settings.BASE_DIR, 'database_backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f'db_backup_{timestamp}.sqlite3'
        backup_path = os.path.join(backup_dir, backup_filename)
        
        try:
            shutil.copy2(db_path, backup_path)
            logger.info(f"Database backed up to {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return None

    @staticmethod
    def optimize_sqlite_database(db_path=None):
        """
        Optimize SQLite database performance
        """
        if not db_path:
            db_path = settings.DATABASES['default']['NAME']
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Vacuum database to reclaim unused space
            cursor.execute('VACUUM')
            
            # Analyze database for query optimization
            cursor.execute('ANALYZE')
            
            conn.commit()
            conn.close()
            
            logger.info("Database optimized successfully")
            return True
        except sqlite3.Error as e:
            logger.error(f"Database optimization error: {e}")
            return False

    @staticmethod
    def log_database_stats(db_path=None):
        """
        Log database statistics
        """
        if not db_path:
            db_path = settings.DATABASES['default']['NAME']
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get database size
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]
            
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            
            database_size = page_count * page_size
            
            logger.info(f"Database Size: {database_size / (1024 * 1024):.2f} MB")
            logger.info(f"Page Count: {page_count}")
            logger.info(f"Page Size: {page_size} bytes")
            
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"Unable to retrieve database stats: {e}")
