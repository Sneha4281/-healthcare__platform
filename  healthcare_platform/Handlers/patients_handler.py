import os
from fastapi.responses import FileResponse
from Modules.patients_module import Patient
from Database.patients_db import get_db
from Utility.generate_uuid import generate_uuid
UPLOAD_DIR = "uploads/"
class PatientsHandler:
        def patient_detail(self,data):
            try:
                patient_id=str(generate_uuid())
                conn = get_db()
                cur=conn.cursor()
                cur.execute("select 1 from patients where patient_name=%s",(data.patient_name,))
                patient=cur.fetchone()
                if patient:
                    return {
                        "message":"patient is already registered",
                    }
                else:
                    cur.execute("insert into patients(patient_id,patient_name) values(%s,%s)",(patient_id,data.patient_name))
                    conn.commit()
                    cur.close()
                    conn.close()
                    return {
                        "patient_name":data.patient_name,
                        "message":"patient registered",
                    }
            except Exception as e:
                return {
                    "message":f"{str(e)}",
                }


        def upload_file(self,patient_name: str, filename: str, file):
            try:

                conn = get_db()
                cur=conn.cursor()
                cur.execute("select patient_id from patients where patient_name=%s",(patient_name,))
                patient=cur.fetchone()
                if not patient:
                    return {
                        "message":"patient is not registered",
                    }
                patient_id=patient[0]
                if file.content_type != "application/pdf":
                    return {
                        "message":f"{file.content_type} is not supported",
                    }
                document_id=str(generate_uuid())
                filename =f"{filename}.pdf"
                file_path = os.path.join(UPLOAD_DIR, filename)

                os.makedirs(UPLOAD_DIR, exist_ok=True)
                # save file to the disk
                with open(file_path, "wb") as f:
                    f.write(file.file.read())
                cur.execute("insert into documents(patient_id,document_id,filename, filepath, filesize) values(%s, %s, %s, %s, %s)",(patient_id,document_id,filename,file_path,file.size))
                conn.commit()
                cur.close()
                conn.close()
                return {
                    "patient_id":patient_id,
                    "document_id":document_id,
                    "filename":filename,
                    "message":"file uploaded",
                }
            except Exception as e:
                return {
                    "message":f"{str(e)}",

                }

        def download(self,document_id):
            try:
                conn = get_db()
                cur=conn.cursor()
                cur.execute("SELECT filename, filepath FROM documents WHERE document_id=%s", (document_id,))
                result = cur.fetchone()
                if not result:
                    return {
                        "message":"no file found",
                    }
                filename = result[0]
                filename, filepath = result
                if not os.path.exists(filepath):
                   return{
                       "message":"file not found",
                   }
                cur.close()
                conn.close()
                return FileResponse(
                  path=filepath,
                  media_type="application/pdf",
                  filename=filename
                )
            except Exception as e:
                return {
                    "message":f"{str(e)}",
                }


        def patients_documents(self,patient_name:str):
            try:
                conn = get_db()
                cur=conn.cursor()
                cur.execute("select patient_id from patients where patient_name=%s",(patient_name,))
                patient=cur.fetchone()
                if not patient:
                    return {
                        "message":"patient is not registered",
                    }
                patient_id=patient[0]
                cur.execute("select document_id,filename from documents where patient_id=%s",(patient_id,))
                rows=cur.fetchall()
                if not rows:
                    return {
                        "patient_name": patient_name,
                        "documents": [],
                        "message": "No documents found"
                    }
                doc_list=[]
                for doc in rows:
                    document_id, filename=doc
                    download_url =  f"/patients/download/{document_id}"
                    doc_list.append({
                        "document_id":document_id,
                        "filename":filename,
                        "download_url":download_url,
                    })
                cur.close()
                conn.close()

                return{
                    "patient_name": patient_name,
                    "documents": doc_list,
                }
            except Exception as e:
                return {
                    "message":f"{str(e)}",
                }




        def patients_file_delete(self,document_id:str):
            try:
                conn = get_db()
                cur=conn.cursor()
                cur.execute("select filepath from documents where document_id=%s",(document_id,))
                result=cur.fetchone()
                if not result:
                    return {
                        "message":"no file found",
                    }
                filepath = result[0]
                if os.path.exists(filepath):
                    os.remove(filepath)
                cur.execute("delete from documents where document_id=%s",(document_id,))
                conn.commit()
                cur.close()
                conn.close()
                return {
                    "message":"file deleted",
                }
            except Exception as e:
                return {
                    "message":f"{str(e)}",
                }













