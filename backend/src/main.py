from fastapi import FastAPI, File, UploadFile

app = FastAPI()




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)