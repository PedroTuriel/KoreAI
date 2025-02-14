import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API funcionando correctamente en Railway"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Railway asigna un puerto dinámico
    print(f"🚀 Servidor corriendo en el puerto {port}")  # Verificación en logs
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
