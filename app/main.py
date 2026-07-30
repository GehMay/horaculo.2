import sys
import os

# Adiciona o diretório 'backend' ao sys.path para que os imports absolutos funcionem
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine
from app.routers import auth, profiles, jobs, events, admin, showcase

# Create the database tables for the MVP
# In a real environment, you would use Alembic migrations instead
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(jobs.router)
app.include_router(events.router)
app.include_router(admin.router)
app.include_router(showcase.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Horáculo!"}

if __name__ == "__main__":
    import uvicorn
    # Executa o servidor uvicorn programaticamente
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
