from django.core.management.base import BaseCommand
from timetable_app.models import TimeSlot

class Command(BaseCommand):
    help = "Fix TimeSlot order"

    def handle(self, *args, **kwargs):
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

        for day in days:
            slots = TimeSlot.objects.filter(day=day).order_by('start_time')

            for i, slot in enumerate(slots, start=1):
                slot.order = i

            TimeSlot.objects.bulk_update(slots, ['order'])  # 🔥 faster

        self.stdout.write(self.style.SUCCESS("✅ Orders fixed"))