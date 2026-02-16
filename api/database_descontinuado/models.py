from sqlalchemy import Integer, Column, String, func, DateTime, Text, UUID, ForeignKey
from enum import Enum
from api.database_descontinuado.base import Base
from api.database_descontinuado.enums import LogsLvl


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(UUID, primary_key=True)
    name = Column(String) # use case
    data = Column(String) # data used 4 task
    pid = Column(Integer) # task process id
    result = Column(String) # result of task

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Logs(Base):
    __tablename__ = "logs"
    id = Column(UUID, primary_key=True)
    level = Column(String, default=LogsLvl)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    task_id = Column(UUID, ForeignKey('tasks.id'), nullable=False)


