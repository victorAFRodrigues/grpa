from sqlalchemy import Column, Integer, String, Text, DateTime, func

from api.database_descontinuado.base import Base


class AutomationConfig(Base):

    __tablename__ = "automation_configs"

    id = Column(Integer, primary_key=True)

    name = Column(String(100))
    api_url = Column(String(255))

    token_encrypted = Column(Text)
    password_encrypted = Column(Text)

    executor = Column(String(100))
    system_url = Column(String(255))

    created_at = Column(DateTime, default=func.now())
