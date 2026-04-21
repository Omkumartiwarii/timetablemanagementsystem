from django.core.management.base import BaseCommand
from timetable_app.seed_data import seed_database


class Command(BaseCommand):
    help = "Seed database with initial data (Departments, Faculty, Subjects, etc.)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        try:
            seed_database()
            self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))