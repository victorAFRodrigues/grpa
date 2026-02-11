from sqlalchemy import Integer, Column, String, func, DateTime, Text

class AutomationConfig(Base):
    __tablename__ = "automation_configs"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    api_url = Column(String)

    token_encrypted = Column(Text)
    password_encrypted = Column(Text)

    executor = Column(String)
    system_url = Column(String)

    created_at = Column(DateTime, default=func.now())
