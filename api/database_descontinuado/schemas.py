from pydantic import BaseModel
from sqlalchemy import Integer, Column, String, func, DateTime, Text


# Aqui estão armazenados os modelos de dados necessários para validação e padronização
class GetTaskModel(BaseModel):
    RPA_EXECUTOR: str

class ResetTaskModel(GetTaskModel):
    RPA_GUID: str

class FinishTaskModel(BaseModel):
    RPA_EXECUTOR: str
    RPA_RESULT: str
    RPA_GUID: str

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
