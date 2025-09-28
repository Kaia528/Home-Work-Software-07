from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from db import get_session
from models import Student, Group, Teacher, Subject, Grade


def select_1(session: Session):
    q = (
        session.query(
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return q


def select_2(session: Session, subject_id: int):
    q = (
        session.query(
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
        .all()
    )
    return q


def select_3(session: Session, subject_id: int):
    q = (
        session.query(
            Group.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student, Student.id == Grade.student_id)
        .join(Group, Group.id == Student.group_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .order_by(Group.name)
        .all()
    )
    return q


def select_4(session: Session):
    q = session.query(func.round(func.avg(Grade.grade), 2)).scalar()
    return q


def select_5(session: Session, teacher_id: int):
    q = (
        session.query(Subject.name)
        .filter(Subject.teacher_id == teacher_id)
        .order_by(Subject.name)
        .all()
    )
    return q


def select_6(session: Session, group_id: int):
    q = (
        session.query(Student.fullname)
        .filter(Student.group_id == group_id)
        .order_by(Student.fullname)
        .all()
    )
    return q


def select_7(session: Session, group_id: int, subject_id: int):
    q = (
        session.query(Student.fullname, Grade.grade)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .order_by(Student.fullname)
        .all()
    )
    return q


def select_8(session: Session, teacher_id: int):
    q = (
        session.query(func.round(func.avg(Grade.grade), 2))
        .select_from(Grade)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    return q


def select_9(session: Session, student_id: int):
    q = (
        session.query(Subject.name)
        .join(Grade, Grade.subject_id == Subject.id)
        .filter(Grade.student_id == student_id)
        .group_by(Subject.id)
        .order_by(Subject.name)
        .all()
    )
    return q


def select_10(session: Session, teacher_id: int, student_id: int):
    q = (
        session.query(Subject.name)
        .join(Grade, Grade.subject_id == Subject.id)
        .filter(Subject.teacher_id == teacher_id, Grade.student_id == student_id)
        .group_by(Subject.id)
        .order_by(Subject.name)
        .all()
    )
    return q

if __name__ == "__main__":
    with get_session() as s:
        print("1:", select_1(s))
