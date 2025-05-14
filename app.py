from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC

from agent.generation import generate_response
from agent.segmentation import segment_user
from agent.optimization import optimize_prompt
from monitoring.metrics import REQUEST_COUNT, CAMPAIGN_CREATED, ERROR_COUNT, FEEDBACK_RATING_COUNT
from mylogging.error_logger import error_logger
from db.feedback import init_feedback_db, save_feedback, get_all_feedback, get_feedback_rating_counts
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# --- Auth config ---
SECRET_KEY = "supersecretkey"  # Change for production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy user DB with bcrypt hash for "wonderland"
fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": "$2b$12$ur0pG2FmbfThG4dX65ITIeCV8QoEwGdae0NUY6mv3KBiZcjemk2Yu"
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# --- Initialization ---
init_feedback_db()
app = FastAPI()

# --- Pydantic Models ---
class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.7

class StructuredGenRequest(BaseModel):
    customer_name: str
    segments: list
    campaign_type: str
    product: str
    offer: str
    max_tokens: int = 100
    temperature: float = 0.7

class SegmentRequest(BaseModel):
    age: int = 0
    interests: list = []
    location: str = ""

class CampaignRequest(BaseModel):
    customer_profile: dict
    campaign_type: str
    product: str
    offer: str
    feedback: dict = None
    max_tokens: int = 100
    temperature: float = 0.7

class OptimizationRequest(BaseModel):
    original_prompt: str
    feedback: dict
    strategy: str = "engagement_boost"

# --- Exception Handlers for Error Counting ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    ERROR_COUNT.inc()
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    ERROR_COUNT.inc()
    error_logger.error("Unhandled exception: %s", str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# --- Endpoints ---
@app.get("/")
def read_root():
    return {"message": "AI Marketing API is running!"}

@app.post("/generate")
async def generate(prompt_request: PromptRequest):
    REQUEST_COUNT.inc()
    try:
        output = generate_response(
            prompt=prompt_request.prompt,
            max_new_tokens=prompt_request.max_tokens,
            temperature=prompt_request.temperature
        )
        return {"response": output}
    except Exception as e:
        ERROR_COUNT.inc()
        error_logger.error("Error in /generate: %s", str(e))
        return {"error": "Internal server error."}

@app.post("/generate-content")
async def generate_structured(req: StructuredGenRequest):
    REQUEST_COUNT.inc()
    try:
        prompt = (
            f"Hi {req.customer_name}, as a {', '.join(req.segments)} customer, "
            f"you'll love our {req.product}! {req.offer} just for you."
        )
        output = generate_response(
            prompt=prompt,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature
        )
        return {"generated_content": output}
    except Exception as e:
        ERROR_COUNT.inc()
        error_logger.error("Error in /generate-content: %s", str(e))
        return {"error": "Internal server error."}

@app.post("/segment")
def segment(data: SegmentRequest):
    REQUEST_COUNT.inc()
    try:
        segments = segment_user(data.model_dump())
        return {"segments": segments}
    except Exception as e:
        ERROR_COUNT.inc()
        error_logger.error("Error in /segment: %s", str(e))
        return {"error": "Internal server error."}

@app.post("/create-campaign")
def create_campaign_api(req: CampaignRequest, username: str = Depends(get_current_user)):
    REQUEST_COUNT.inc()
    try:
        # Save feedback for future learning
        if req.feedback:
            save_feedback(
                user=req.customer_profile.get("name", "unknown"),
                campaign_type=req.campaign_type,
                product=req.product,
                offer=req.offer,
                feedback=req.feedback
            )
            # --- Feedback analytics: update Prometheus metrics ---
            rating = req.feedback.get("rating")
            if rating:
                # Refresh all counts for accuracy
                counts = get_feedback_rating_counts()
                for r, count in counts.items():
                    FEEDBACK_RATING_COUNT.labels(rating=str(r)).set(count)
        # Use advanced optimization with product context
        result = optimize_prompt(
            original_prompt=f"Hi {req.customer_profile.get('name', 'Customer')}, as a {', '.join(req.customer_profile.get('interests', []))} customer, you'll love our {req.product}! {req.offer} just for you. This is part of our {req.campaign_type} campaign.",
            feedback=req.feedback or {},
            strategy="engagement_boost",
            product=req.product
        )
        CAMPAIGN_CREATED.inc()
        return {"generated_content": result}
    except Exception as e:
        ERROR_COUNT.inc()
        error_logger.error("Error in /create-campaign: %s", str(e))
        return {"error": "Internal server error."}

@app.post("/optimize")
def optimize(req: OptimizationRequest):
    REQUEST_COUNT.inc()
    try:
        improved_prompt = optimize_prompt(
            original_prompt=req.original_prompt,
            feedback=req.feedback,
            strategy=req.strategy
        )
        return {"optimized_prompt": improved_prompt}
    except Exception as e:
        ERROR_COUNT.inc()
        error_logger.error("Error in /optimize: %s", str(e))
        return {"error": "Internal server error."}

# --- Prometheus metrics endpoint ---
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# --- Auth Endpoints ---
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Feedback viewing endpoint ---
@app.get("/feedbacks")
def all_feedbacks():
    return {"feedbacks": get_all_feedback()}

