from faker import Faker
from random import randint, choice, sample
from datetime import date, timedelta

from db import get_session
from models import Base, Group, Student, Teacher, Subject, Grade
from sqlalchemy import select, func
from sqlalchemy.orm import Session

fake = Faker()

NUM_STUDENTS = randint(30, 50)
NUM_GROUPS = 3
NUM_SUBJECTS = randint(5, 8)
NUM_TEACHERS = randint(3, 5)
MAX_GRADES_PER_STUDENT = 20

GROUP_NAMES = ["A-1", "B-1", "C-1"]
SUBJECT_NAMES_POOL = [
    "Math Analysis", "Linear Algebra", "Databases",
    "Networks", "Operating Systems", "Algorithms",
    "Python", "Web Dev", "Statistics", "AI Basics"
]

def run():
    with get_session() as session:  # type: Session

        for model in [Grade, Subject, Teacher, Student, Group]:
            session.query(model).delete()
        session.commit()


        groups = [Group(name=GROUP_NAMES[i]) for i in range(NUM_GROUPS)]
        session.add_all(groups); session.flush()


        teachers = [Teacher(fullname=fake.name()) for _ in range(NUM_TEACHERS)]
        session.add_all(teachers); session.flush()


        subj_names = sample(SUBJECT_NAMES_POOL, NUM_SUBJECTS)
        subjects = [Subject(name=n, teacher=choice(teachers)) for n in subj_names]
        session.add_all(subjects); session.flush()


        students = [
            Student(fullname=fake.name(), group=choice(groups))
            for _ in range(NUM_STUDENTS)
        ]
        session.add_all(students); session.flush()


        start = date.today() - timedelta(days=365)
        for st in students:
            k = randint(10, MAX_GRADES_PER_STUDENT)
            for _ in range(k):
                sub = choice(subjects)
                g = randint(40, 100)
                d = start + timedelta(days=randint(0, 365))
                session.add(Grade(student=st, subject=sub, grade=g, date_received=d))

        session.commit()

        total = session.scalar(select(func.count(Grade.id)))
        print(f"Done. Students={len(students)}, Subjects={len(subjects)}, Grades={total}")

if __name__ == "__main__":
    run()
