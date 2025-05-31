import sys
from django.core.exceptions import ValidationError
from school.models import Subject, Teacher, Class, Student, Schedule, Grade


def add_subject():
    print("\nДодавання нового предмету")
    name = input("Назва предмету: ")
    description = input("Опис (необов'язково): ")

    try:
        subject = Subject(name=name, description=description)
        subject.full_clean()
        subject.save()
        print(f"Предмет '{name}' успішно додано!")
    except ValidationError as e:
        print("Помилка:", e.messages)


def add_teacher():
    print("\nДодавання нового вчителя")
    first_name = input("Ім'я: ")
    last_name = input("Прізвище: ")

    subjects = Subject.objects.all()
    if not subjects:
        print("Спочатку додайте хоча б один предмет!")
        return

    print("Доступні предмети:")
    for i, subject in enumerate(subjects, 1):
        print(f"{i}. {subject.name}")

    try:
        choice = int(input("Виберіть номер предмету: ")) - 1
        subject = subjects[choice]

        teacher = Teacher(first_name=first_name, last_name=last_name, subject=subject)
        teacher.full_clean()
        teacher.save()
        print(f"Вчителя {last_name} {first_name} успішно додано!")
    except (IndexError, ValueError):
        print("Невірний вибір предмету!")
    except ValidationError as e:
        print("Помилка:", e.messages)


def add_class():
    print("\nДодавання нового класу")
    name = input("Назва класу (наприклад, 10-А): ")

    try:
        year = int(input("Рік навчання: "))
        if year < 1 or year > 11:
            raise ValueError

        student_class = Class(name=name, year=year)
        student_class.full_clean()
        student_class.save()
        print(f"Клас '{name}' успішно додано!")
    except ValueError:
        print("Рік навчання має бути числом від 1 до 11")
    except ValidationError as e:
        print("Помилка:", e.messages)


def add_student():
    print("\nДодавання нового учня")
    first_name = input("Ім'я: ")
    last_name = input("Прізвище: ")

    classes = Class.objects.all()
    if not classes:
        print("Спочатку додайте хоча б один клас!")
        return

    print("Доступні класи:")
    for i, cls in enumerate(classes, 1):
        print(f"{i}. {cls.name}")

    try:
        choice = int(input("Виберіть номер класу: ")) - 1
        student_class = classes[choice]

        student = Student(first_name=first_name, last_name=last_name, student_class=student_class)
        student.full_clean()
        student.save()
        print(f"Учня {last_name} {first_name} успішно додано до класу {student_class}!")
    except (IndexError, ValueError):
        print("Невірний вибір класу!")
    except ValidationError as e:
        print("Помилка:", e.messages)


def add_schedule():
    print("\nДодавання заняття в розклад")

    # Вибір класу
    classes = Class.objects.all()
    if not classes:
        print("Спочатку додайте хоча б один клас!")
        return

    print("Доступні класи:")
    for i, cls in enumerate(classes, 1):
        print(f"{i}. {cls.name}")

    try:
        class_choice = int(input("Виберіть номер класу: ")) - 1
        student_class = classes[class_choice]
    except (IndexError, ValueError):
        print("Невірний вибір класу!")
        return

    # Вибір предмету
    subjects = Subject.objects.all()
    if not subjects:
        print("Спочатку додайте хоча б один предмет!")
        return

    print("Доступні предмети:")
    for i, subject in enumerate(subjects, 1):
        print(f"{i}. {subject.name}")

    try:
        subject_choice = int(input("Виберіть номер предмету: ")) - 1
        subject = subjects[subject_choice]
    except (IndexError, ValueError):
        print("Невірний вибір предмету!")
        return

    # Вибір вчителя для цього предмету
    teachers = Teacher.objects.filter(subject=subject)
    if not teachers:
        print(f"Немає вчителів для предмету {subject.name}!")
        return

    print("Доступні вчителі:")
    for i, teacher in enumerate(teachers, 1):
        print(f"{i}. {teacher.last_name} {teacher.first_name}")

    try:
        teacher_choice = int(input("Виберіть номер вчителя: ")) - 1
        teacher = teachers[teacher_choice]
    except (IndexError, ValueError):
        print("Невірний вибір вчителя!")
        return

    # Вибір дня тижня
    print("\nДні тижня:")
    days = [day[1] for day in Schedule.DAYS_OF_WEEK]
    for i, day in enumerate(days, 1):
        print(f"{i}. {day}")

    try:
        day_choice = int(input("Виберіть номер дня: ")) - 1
        day_code = Schedule.DAYS_OF_WEEK[day_choice][0]
    except (IndexError, ValueError):
        print("Невірний вибір дня!")
        return

    # Введення часу
    try:
        time_str = input("Час початку (формат HH:MM): ")
        hours, minutes = map(int, time_str.split(':'))
        if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
            raise ValueError
        start_time = f"{hours:02d}:{minutes:02d}"
    except ValueError:
        print("Невірний формат часу!")
        return

    try:
        schedule = Schedule(
            day=day_code,
            start_time=start_time,
            subject=subject,
            student_class=student_class,
            teacher=teacher
        )
        schedule.full_clean()
        schedule.save()
        print("Заняття успішно додано до розкладу!")
    except ValidationError as e:
        print("Помилка:", e.messages)


def add_grade():
    print("\nДодавання оцінки")

    # Вибір учня
    students = Student.objects.all()
    if not students:
        print("Спочатку додайте хоча б одного учня!")
        return

    print("Доступні учні:")
    for i, student in enumerate(students, 1):
        print(f"{i}. {student.last_name} {student.first_name} ({student.student_class})")

    try:
        student_choice = int(input("Виберіть номер учня: ")) - 1
        student = students[student_choice]
    except (IndexError, ValueError):
        print("Невірний вибір учня!")
        return

    # Вибір предмету
    subjects = Subject.objects.all()
    if not subjects:
        print("Спочатку додайте хоча б один предмет!")
        return

    print("Доступні предмети:")
    for i, subject in enumerate(subjects, 1):
        print(f"{i}. {subject.name}")

    try:
        subject_choice = int(input("Виберіть номер предмету: ")) - 1
        subject = subjects[subject_choice]
    except (IndexError, ValueError):
        print("Невірний вибір предмету!")
        return

    # Введення оцінки
    print("\nДоступні оцінки: 1-12")
    try:
        grade = int(input("Оцінка: "))
        if grade < 1 or grade > 12:
            raise ValueError
    except ValueError:
        print("Оцінка має бути числом від 1 до 12!")
        return

    # Введення дати
    try:
        date_str = input("Дата (формат YYYY-MM-DD): ")
        year, month, day = map(int, date_str.split('-'))
        date = f"{year:04d}-{month:02d}-{day:02d}"
    except ValueError:
        print("Невірний формат дати!")
        return

    try:
        grade_obj = Grade(
            student=student,
            subject=subject,
            grade=grade,
            date=date
        )
        grade_obj.full_clean()
        grade_obj.save()
        print("Оцінку успішно додано!")
    except ValidationError as e:
        print("Помилка:", e.messages)


def show_menu():
    while True:
        print("\n=== Система керування шкільним розкладом ===")
        print("1. Додати предмет")
        print("2. Додати вчителя")
        print("3. Додати клас")
        print("4. Додати учня")
        print("5. Додати заняття в розклад")
        print("6. Додати оцінку")
        print("0. Вийти")

        choice = input("Виберіть опцію: ")

        if choice == '1':
            add_subject()
        elif choice == '2':
            add_teacher()
        elif choice == '3':
            add_class()
        elif choice == '4':
            add_student()
        elif choice == '5':
            add_schedule()
        elif choice == '6':
            add_grade()
        elif choice == '0':
            print("До побачення!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    import django

    django.setup()
    show_menu()