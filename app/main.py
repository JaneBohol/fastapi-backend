from fastapi import FastAPI, HTTPException
from app.models import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.database import SessionLocal, User

app = FastAPI()

@app.post("/register", response_model=RegisterResponse)
def register_user(request: RegisterRequest):
    db = SessionLocal()
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(name=request.name, email=request.email, password=request.password)
    db.add(user)
    db.commit()
    return RegisterResponse(success=True, message="Account created successfully")

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(
        User.email == request.email, User.password == request.password
    ).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return LoginResponse(success=True, message="Login successful")
