import os
import uvicorn
from fastapi import FastAPI
from app.models import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.database import SessionLocal, User

app = FastAPI()

@app.post("/register", response_model=RegisterResponse)
def register_user(request: RegisterRequest):
    db = SessionLocal()
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        return RegisterResponse(success=False, message="Email already registered")
    user = User(name=request.name, email=request.email, password=request.password)
    db.add(user)
    db.commit()
    return RegisterResponse(success=True, message="Account created successfully")

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.email == request.email, User.password == request.password).first()
    if not user:
        return LoginResponse(success=False, message="Invalid credentials")
    return LoginResponse(success=True, message="Login successful")

# ✅ Add this to run the app on the right port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
