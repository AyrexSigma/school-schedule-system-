from django.db import models
from django.core.exceptions import ValidationError


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Class(models.Model):
    name = models.CharField(max_length=20, unique=True)
    year = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.student_class})"


class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
    ]

    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('day', 'start_time', 'student_class')

    def __str__(self):
        return f"{self.get_day_display()} {self.start_time} - {self.subject} ({self.student_class})"


class Grade(models.Model):
    GRADE_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(choices=GRADE_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.student}: {self.grade} in {self.subject} ({self.date})"