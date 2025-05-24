from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Subject name")
    description = models.TextField(blank=True, verbose_name="Subject description")

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['name']

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Name")
    last_name = models.CharField(max_length=50, verbose_name="Last name")
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Subject",
        related_name='teachers'
    )

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ['last_name', 'first_name']
        unique_together = ['first_name', 'last_name', 'subject']

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.subject})"


class Class(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Class name")
    year = models.PositiveSmallIntegerField(verbose_name="Year of studying")

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ['year', 'name']
        unique_together = ['name', 'year']

    def __str__(self):
        return f"{self.name} ({self.year} рік)"


class Student(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Name")
    last_name = models.CharField(max_length=50, verbose_name="Last name")
    student_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name="Class",
        related_name='students'
    )

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['last_name', 'first_name']
        unique_together = ['first_name', 'last_name', 'student_class']

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.student_class})"


class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', "Friday"),
    ]

    day = models.CharField(
        max_length=3,
        choices=DAYS_OF_WEEK,
        verbose_name="Day of week"
    )
    start_time = models.TimeField(verbose_name="Start time")
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Subject",
        related_name='schedules'
    )
    student_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name="Class",
        related_name='schedules'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        verbose_name="Teacher",
        related_name='schedules'
    )

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        ordering = ['day', 'start_time']
        unique_together = ['day', 'start_time', 'student_class']

    def __str__(self):
        return f"{self.start_time} - {self.subject} ({self.teacher})"


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

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Student",
        related_name='grades'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Subject",
        related_name='grades'
    )
    grade = models.PositiveSmallIntegerField(
        choices=GRADE_CHOICES,
        verbose_name="Grade"
    )
    date = models.DateField(verbose_name="Date")

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        ordering = ['-date', 'student']
        unique_together = ['student', 'subject', 'date']

    def __str__(self):
        return f"{self.student}: {self.subject} - {self.grade} ({self.date})"