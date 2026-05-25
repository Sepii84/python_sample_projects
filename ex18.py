# course enrollment system with JSON persistence.
import json


class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name.strip()
        self.age = age

    def display(self, index):
        print(f"[{index}] "
              f"Student: {self.name} | "
              f"ID: {self.student_id} | "
              f"Age: {self.age}")

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age
        }

class Course:
    def __init__(self, course_id, title, capacity, enrolled_student_ids):
        self.course_id = course_id
        self.title = title
        self.capacity = capacity
        self.enrolled_student_ids = enrolled_student_ids

    def display(self, index):
        print(f"[{index}] ", end="")

    def has_space(self):
        return len(self.enrolled_student_ids) < self.capacity

    def enroll(self, student_id):
        self.enrolled_student_ids.append(student_id)

    def remove_student(self, student_id):
        self.enrolled_student_ids.remove(student_id)

class OnlineCourse(Course):
    def __init__(self, course_id, title, capacity, enrolled_student_ids, platform):
        super().__init__(course_id, title, capacity, enrolled_student_ids)
        self.platform = platform

    def display(self, index):
        super().display(index)
        print(f"Online Course: {self.title} | "
              f"ID: {self.course_id} | "
              f"Capacity: {self.capacity} | "
              f"Enrolled: {len(self.enrolled_student_ids)} | "
              f"Platform: {self.platform}")

    def to_dict(self):
        return {
            "type": "online",
            "course_id": self.course_id,
            "title": self.title,
            "capacity": self.capacity,
            "enrolled_student_ids": self.enrolled_student_ids,
            "platform": self.platform
        }

class InPersonCourse(Course):
    def __init__(self, course_id, title, capacity, enrolled_student_ids, room):
        super().__init__(course_id, title, capacity, enrolled_student_ids)
        self.room = room

    def display(self, index):
        super().display(index)
        print(f"In-Person Course: {self.title} | "
              f"ID: {self.course_id} | "
              f"Capacity: {self.capacity} | "
              f"Enrolled: {len(self.enrolled_student_ids)} | "
              f"Room: {self.room}")

    def to_dict(self):
        return {
            "type": "in_person",
            "course_id": self.course_id,
            "title": self.title,
            "capacity": self.capacity,
            "enrolled_student_ids": self.enrolled_student_ids,
            "room": self.room
        }

def add_student(students):
    student_id = input("Enter student ID: ").strip()
    if not student_id:
        print("Invalid student data")
        return
    if find_student(students, student_id):
        print("Student ID already exists")
        return
    name = input("Enter student name: ").strip()
    if not name:
        print("Invalid student data")
        return
    try:
        age = int(input("Enter student age: "))
    except ValueError:
        print("Invalid student data")
        return
    if age <= 0:
        print("Invalid student data")
        return
    students.append(Student(student_id, name, age))
    print("Student added.")

def get_common_course_data(courses):
    course_id = input("Enter course ID: ").strip()
    if not course_id:
        print("Invalid course data")
        return None
    if find_course(courses, course_id):
        print("Course ID already exists")
        return None
    title = input("Enter course title: ").strip()
    if not title:
        print("Invalid course data")
        return None
    try:
        capacity = int(input("Enter capacity of the classroom: "))
    except ValueError:
        print("Invalid course data")
        return None
    if capacity <= 0:
        print("Invalid course data")
        return None
    return course_id, title, capacity, []

def add_online_course(courses):
    data = get_common_course_data(courses)
    if not data:
        return
    course_id, title, capacity, enrolled_student_ids = data
    platform = input("Enter the platform: ").strip()
    if not platform:
        print("Invalid platform")
        return
    courses.append(OnlineCourse(course_id, title, capacity, enrolled_student_ids, platform))
    print("Online course added.")

def add_in_person_course(courses):
    data = get_common_course_data(courses)
    if not data:
        return
    course_id, title, capacity, enrolled_student_ids = data
    room = input("Enter the room: ").strip()
    if not room:
        print("Invalid room")
        return
    courses.append(InPersonCourse(course_id, title, capacity, enrolled_student_ids, room))
    print("In-person course added.")

def show_students(students):
    if not students:
        print("No students available")
        return
    for index, student in enumerate(students, start=1):
        student.display(index)

def show_courses(courses):
    if not courses:
        print("No courses available")
        return
    for index, course in enumerate(courses, start=1):
        course.display(index)

def find_course(courses, course_id):
    for course in courses:
        if course.course_id == course_id:
            return course
    return None

def find_student(students, student_id):
    for student in students:
        if student.student_id == student_id:
            return student
    return None

def student_enrollment(students, courses):
    student_id = input("Enter student ID: ").strip()
    if not student_id:
        print("Invalid student data")
        return
    student = find_student(students, student_id)
    if not student:
        print("Student not found")
        return
    course_id = input("Enter course ID: ").strip()
    if not course_id:
        print("Invalid course data")
        return
    course = find_course(courses, course_id)
    if not course:
        print("Course not found")
        return
    if student_id in course.enrolled_student_ids:
        print("Student already enrolled")
        return
    if not course.has_space():
        print("Course is full")
        return
    course.enroll(student_id)
    print("Student enrolled.")

def show_student_courses(students, courses):
    student_id = input("Enter student ID: ").strip()
    if not student_id:
        print("Invalid student data")
        return
    student = find_student(students, student_id)
    if not student:
        print("Student not found")
        return
    student_courses = []
    for course in courses:
        if student_id in course.enrolled_student_ids:
            student_courses.append(course)
    if not student_courses:
        print("No courses found for this student")
        return
    for index, course in enumerate(student_courses, start=1):
        course.display(index)

def show_students_in_a_course(students, courses):
    course_id = input("Enter course ID: ").strip()
    if not course_id:
        print("Invalid course data")
        return
    course = find_course(courses, course_id)
    if not course:
        print("Course not found")
        return
    enrolled_students = []
    for student_id in course.enrolled_student_ids:
        enrolled_students.append(student_id)
    if not enrolled_students:
        print("No students enrolled in this course")
        return
    for index, student_id in enumerate(enrolled_students, start=1):
        student = find_student(students, student_id)
        if student:
            student.display(index)

def remove_enrollment(students, courses):
    student_id = input("Enter student ID: ").strip()
    if not student_id:
        print("Invalid student data")
        return
    student = find_student(students, student_id)
    if not student:
        print("Student not found")
        return
    course_id = input("Enter course ID: ").strip()
    if not course_id:
        print("Invalid course data")
        return
    course = find_course(courses, course_id)
    if not course:
        print("Course not found")
        return
    if student_id not in course.enrolled_student_ids:
        print("Enrollment not found")
        return
    course.remove_student(student_id)
    print("Enrollment removed.")

def save_to_json(students, courses):
    file_path = "enrollments.json"
    try:
        with open(file_path, "w") as file:
            data = {
                "students": [student.to_dict() for student in students],
                "courses": [course.to_dict() for course in courses]
            }
            json.dump(data, file, indent=4)
    except PermissionError:
        print("Permission denied")
        return
    print("Data saved.")

def load_from_json():
    file_path = "enrollments.json"
    students = []
    courses = []
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            for student in data.get("students", []):
                try:
                    students.append(Student(
                        student["student_id"],
                        student["name"],
                        student["age"]
                    ))
                except KeyError:
                    continue
            for course in data.get("courses", []):
                try:
                    if course["type"] == "online":
                        courses.append(OnlineCourse(
                            course["course_id"],
                            course["title"],
                            course["capacity"],
                            course["enrolled_student_ids"],
                            course["platform"]
                        ))
                    elif course["type"] == "in_person":
                        courses.append(InPersonCourse(
                            course["course_id"],
                            course["title"],
                            course["capacity"],
                            course["enrolled_student_ids"],
                            course["room"]
                        ))
                except KeyError:
                    continue
    except FileNotFoundError:
        print("File not found")
        return
    except PermissionError:
        print("Permission denied")
        return
    except json.JSONDecodeError:
        print("Invalid JSON file")
        return
    print("Data loaded.")
    return students, courses

def main():
    students = []
    courses = []
    while True:
        try:
            choice = int(input("1) Add student\n"
                               "2) Add online course\n"
                               "3) Add in-person course\n"
                               "4) Show all students\n"
                               "5) Show all courses\n"
                               "6) Enroll student in course\n"
                               "7) Show courses of a student\n"
                               "8) Show students in a course\n"
                               "9) Remove enrollment\n"
                               
                               "10) Save to JSON\n"
                               "11) Load from JSON\n"
                               "12) Exit\n"))
        except ValueError:
            print("Invalid choice! choose between 1 and 12.")
            continue
        match choice:
            case 1:
                add_student(students)
            case 2:
                add_online_course(courses)
            case 3:
                add_in_person_course(courses)
            case 4:
                show_students(students)
            case 5:
                show_courses(courses)
            case 6:
                student_enrollment(students, courses)
            case 7:
                show_student_courses(students, courses)
            case 8:
                show_students_in_a_course(students, courses)
            case 9:
                remove_enrollment(students, courses)
            case 10:
                save_to_json(students, courses)
            case 11:
                loaded_data = load_from_json()
                if loaded_data is not None:
                    students, courses = loaded_data
            case 12:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice! choose between 1 and 12.")

if __name__ == "__main__":
    main()
