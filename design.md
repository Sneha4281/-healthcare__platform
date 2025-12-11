1. Tech Stack Choices
**Q2. Backend Framework**
FastAPI
Very fast
Built-in validation using Pydantic
Auto API docs (/docs)
Easy handling of file upload & responses

Q3. Database
PostgreSQL
Better for production
Supports concurrency
Handles large data safely
Strong SQL support

Q4. Scaling to 1,000 Users
Move file storage to Amazon S3 or Azure Blob
Uvicorn workers

**2. Architecture Overview
Client → FastAPI Backend → PostgreSQL Database
                     ↓
              Local uploads/ folder
Steps:
Patient uploads PDF file
FastAPI validates and stores it inside uploads/
Metadata saved into documents table
Client can list, download, delete documents


**3. API Specification**
POST /patients/upload
Upload a PDF for a patient
Request: multipart form-data
Response:
      {
  "patient_id": "uuid(jdfisjrhg64jkbhjdf7)",
  "document_id": "uuid(djfusdgfbehvbfuwe)",
  "message": "File uploaded"
}


GET /patients/documents?patient_name=Sneha
List all PDFs for that patient
Response:
  {
  "patient_name": "Sneha",
  "documents": [
    {
      "document_id": "abc",
      "filename": "xray.pdf",
      "download_url": "/patients/download/abc"
    }
  ]
}


GET /patients/download/{document_id}
Downloads the PDF file.

DELETE /patients/delete/{document_id}
Deletes the file from disk and database.

4. Data Flow
Upload
Patient name comes in reques
Backend finds patient_id
Validate file type → must be PDF
Save file to /uploads/filename.pdf
Insert metadata into DB
Return success + document_id
Download
Client hits /patients/download/{id}
Backend fetches file path
Returns file via FileResponse

5. Assumptions
Only one role: patient
Only PDF allowed
File stored in local machine (not cloud)
filenames stored as user-given names

