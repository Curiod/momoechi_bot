from sqlalchemy import ForeignKey, BigInteger, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Document(Base):
    __tablename__ = 'documents'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)


# class Question(Base):
#     __tablename__ = 'questions'
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     context_id: Mapped[int] = mapped_column(ForeignKey('documents.id'))
#     question: Mapped[str] = mapped_column(Text, nullable=False)


# class Answer(Base):
#     __tablename__ = 'answers'
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
#     text: Mapped[str] = mapped_column(Text, nullable=False)
#     answer_start: Mapped[int] = mapped_column()
