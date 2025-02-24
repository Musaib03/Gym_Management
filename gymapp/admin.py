from django.contrib import admin
from .models import Membership, Member, Trainer, Payment, Class, Attendance, Equipment

# Register models
admin.site.register(Membership)
admin.site.register(Member)
admin.site.register(Trainer)
admin.site.register(Payment)
admin.site.register(Class)
admin.site.register(Attendance)
admin.site.register(Equipment)
