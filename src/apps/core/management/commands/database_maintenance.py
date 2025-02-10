from django.core.management.base import BaseCommand
from django.utils import timezone

from src.apps._utils.database_management import DatabaseManager


class Command(BaseCommand):
    help = "Perform SQLite database maintenance tasks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--backup", action="store_true", help="Perform database backup"
        )
        parser.add_argument(
            "--optimize", action="store_true", help="Optimize database performance"
        )
        parser.add_argument(
            "--stats", action="store_true", help="Log database statistics"
        )

    def handle(self, *args, **options):
        start_time = timezone.now()
        self.stdout.write(f"Starting database maintenance at {start_time}")

        # Perform backup if requested
        if options["backup"]:
            self.stdout.write("Performing database backup...")
            backup_path = DatabaseManager.backup_sqlite_database()
            if backup_path:
                self.stdout.write(self.style.SUCCESS(f"Backup created: {backup_path}"))

        # Optimize database if requested
        if options["optimize"]:
            self.stdout.write("Optimizing database...")
            if DatabaseManager.optimize_sqlite_database():
                self.stdout.write(self.style.SUCCESS("Database optimization complete"))

        # Log database statistics if requested
        if options["stats"]:
            self.stdout.write("Retrieving database statistics...")
            DatabaseManager.log_database_stats()

        end_time = timezone.now()
        duration = end_time - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"Database maintenance completed in {duration.total_seconds():.2f} seconds"
            )
        )
