from django.contrib import admin
from .models import Subject, Teacher, Class, Student, Schedule, Grade

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'subject')
    list_filter = ('subject',)
    search_fields = ('last_name', 'first_name')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    search_fields = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'student_class')
    list_filter = ('student_class',)
    search_fields = ('last_name', 'first_name')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'subject', 'student_class', 'teacher')
    list_filter = ('day', 'student_class')
    ordering = ('day', 'start_time')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade', 'date')
    list_filter = ('subject', 'grade')
    date_hierarchy = 'date'