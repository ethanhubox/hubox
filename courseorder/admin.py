from django.contrib import admin

from .models import CourseOrder


class CourseOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'name',)
    readonly_fields = ('timestamp',)

admin.site.register(CourseOrder, CourseOrderAdmin)
