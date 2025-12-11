# -healthcare__platform

Patient Document Management Backend (FastAPI + PostgreSQL)
This project is a backend service for a healthcare platform where patients can upload, view, download, and manage their medical PDF documents.
The system stores PDFs in a local folder (uploads/) and stores metadata in PostgreSQL.


Patient Management
Register a new patient
Check if a patient already exists

Document Upload
Upload PDF files only
Custom filename allowed
Each patient can have multiple documents

Document Retrieval
Fetch all documents for a specific patient
Includes downloadable link for each document

Document Download
Download file using document_id

PROJECT STRUCUTRE
healthcare__platform/
│
├── main.py
├── Service/
│   └── patients_service.py
├── Handlers/
│   └── patients_handler.py
├── Modules/
│   └── patients_module.py
├── Database/
│   └── patients_db.py
├── Utility/
│   └── generate_uuid.py
└── uploads/     # (auto-created)



API Endpoints
Register Patient
POST /patients/register
Request Body (JSON):
{
  "patient_name": "sneha_2001"
}
Response
{
  "patient_name": "sneha_2001",
  "message": "patient registered"
}

Upload PDF File
POST /patients/upload
Form-Data:
patient_name: sneha_2001
filename: xray
file: <PDF File>

RESPONSE:
{
  "patient_id": "uuid123",
  "document_id": "uuid456",
  "filename": "xray",
  "message": "file uploaded"
}

View All Documents of Patient
GET /patients/view?patient_name=sneha_2001
Response:
{
  "patient_name": "sneha_2001",
  "documents": [
    {
      "document_id": "0168bf8d...",
      "filename": "xray",
      "download_url": "/patients/download/0168bf8d..."
    }
  ]
}

Download a PDF
GET /patients/download/{document_id}
http://localhost:59009/patients/download/0168bf8d-27bb-4981-90f5-8177da714b5d

Install Dependencies
pip install fastapi uvicorn psycopg2 python-dotenv

Configure .env
DB_NAME=your_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

Start Server
uvicorn main:app --reload --port 59009


Future Enhancements
JWT authentication
Delete document endpoint
Pagination of documents
Store files on AWS S3 instead of local folder
