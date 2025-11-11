from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chatbot_routes import router as chatbot_router

app = FastAPI(title="Chatbot Informativo sobre Sismos en Guatemala")

# Configuración de CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Rutas
app.include_router(chatbot_router, prefix="/api")

@app.get("/")
def root():
  return {"message": "API del Chatbot de Sismos en Guatemala funcionando correctamente."}