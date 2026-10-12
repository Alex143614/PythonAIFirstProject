"""
db.py
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///navigator.db"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)


# ============================================================
# МОДЕЛЬ: ТАБЛИЦА routes
# ============================================================

class Route(Base):
    __tablename__ = "__routes__"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # что запрашивал пользователь
    start_point = Column(String, nullable=False)
    finish_point = Column(String, nullable=False)

    # какой путь выбрал (например "A,C,F,G")
    route = Column(String, nullable=False)

    # прогноз из карты (Dijkstra)
    time = Column(Integer, nullable=False)
    distance = Column(Integer, nullable=False)

    # факт, который ввёл пользователь после поездки
    actual_time = Column(Integer, nullable=False)
    actual_distance = Column(Integer, nullable=False)

    # мёртвый груз (по заданию), ни на что не влияет
    traffic = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)

    # дата создания записи
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================================
# ФУНКЦИИ
# ============================================================

def init_db():
    """Создаёт таблицу routes, если её ещё нет."""
    Base.metadata.create_all(engine)


def get_session():
    """Возвращает новую сессию для работы с БД."""
    return SessionLocal()