from django.contrib import admin

from periodicals import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Payment)
admin.site.register(models.Subscription)
admin.site.register(models.Magazine)