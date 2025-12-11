from fastapi import APIRouter,UploadFile,File,Form
from App_Configuration.patients_config import Patients_path
from Modules.patients_module import Patient,Document
from Handlers.patients_handler import PatientsHandler

# router = APIRouter()
router = APIRouter(prefix="/patients")
PH=PatientsHandler()

@router.post(Patients_path.patient_name)
def patient_detail_name(data:Patient):
    try:
        return PH.patient_detail(data)
    except Exception as e:
        return {
            "message":f"{str(e)}",
        }
@router.post(Patients_path.patient_upload)
def patient_upload_file(patient_name: str = Form(...),
    filename: str = Form(...),file: UploadFile = File(...)):
        try:
            return PH.upload_file(patient_name, filename,file)
        except Exception as e:
            return {
                "message":f"{str(e)}",
            }

@router.get("/download/{document_id}")
def download_document(document_id: str):
    try:
        return PH.download(document_id)
    except Exception as e:
        return {
            "message":f"{str(e)}",
        }



@router.get(Patients_path.patient_view_documents)
def patient_view_doc(patient_name:str):
    return PH.patients_documents(patient_name)



@router.delete(Patients_path.delete_file)
def delete_file(document_id:str):
    try:
        return PH.patients_file_delete(document_id)
    except Exception as e:

        return {
            "message":f"{str(e)}",
        }

