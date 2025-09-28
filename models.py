from __future__ import annotations

from datetime import date as dt_date

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    Date,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):

    pass


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)


    students: Mapped[list["Student"]] = relationship(back_populates="group")

    def __repr__(self) -> str:
        return f"<Group id={self.id} name={self.name!r}>"


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)

    group: Mapped["Group"] = relationship(back_populates="students")
    grades: Mapped[list["Grade"]] = relationship(back_populates="student")

    def __repr__(self) -> str:
        return f"<Student id={self.id} fullname={self.fullname!r}>"


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    subjects: Mapped[list["Subject"]] = relationship(back_populates="teacher")

    def __repr__(self) -> str:
        return f"<Teacher id={self.id} fullname={self.fullname!r}>"


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)

    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")
    grades: Mapped[list["Grade"]] = relationship(back_populates="subject")


    __table_args__ = (
        UniqueConstraint("name", "teacher_id", name="uq_subject_by_teacher"),
    )

    def __repr__(self) -> str:
        return f"<Subject id={self.id} name={self.name!r} teacher_id={self.teacher_id}>"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)

    grade: Mapped[int] = mapped_column(Integer, nullable=False)  # 0..100

    date_received: Mapped[dt_date] = mapped_column(Date, nullable=False)

    student: Mapped["Student"] = relationship(back_populates="grades")
    subject: Mapped["Subject"] = relationship(back_populates="grades")

    def __repr__(self) -> str:
        return (
            f"<Grade id={self.id} student_id={self.student_id} "
            f"subject_id={self.subject_id} grade={self.grade} date={self.date_received}>"
        )

