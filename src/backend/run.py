import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app_api", port=8000, log_level="info", host='0.0.0.0')
