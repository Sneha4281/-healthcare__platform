import uvicorn
from fastapi import FastAPI
from Service import patients_service

app = FastAPI()
@app.get("/")
def root():
    return {
        "message":"Hello world"
    }

app.include_router(patients_service.router, tags=["Patients_detail"])
if __name__=="__main__":
    uvicorn.run("main:app",host="localhost",port=59009)
