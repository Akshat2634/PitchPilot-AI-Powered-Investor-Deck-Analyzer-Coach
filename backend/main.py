import uvicorn
from app.api.api import app

if __name__ == "__main__":
    uvicorn.run(
        "app.api.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True 
    ) 