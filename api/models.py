from pydantic import BaseModel

# Aqui estão armazenados os modelos de dados necessários para validação e padronização 
class GetTaskModel(BaseModel):
    RPA_EXECUTOR: str

class ResetTaskModel(GetTaskModel):
    RPA_GUID: str

class FinishTaskModel(BaseModel):
    RPA_EXECUTOR: str
    RPA_RESULT: str
    RPA_GUID: str
