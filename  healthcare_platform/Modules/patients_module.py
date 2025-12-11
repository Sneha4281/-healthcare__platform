from pydantic import BaseModel
from datetime import datetime

class Patient(BaseModel):
    # patient_id: str
    patient_name: str



class Document(BaseModel):
    patient_name: str
    filename: str

