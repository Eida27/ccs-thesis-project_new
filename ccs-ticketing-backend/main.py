from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware # NEW: Import CORS Middleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Import our new database modules
from core.database import engine, Base, get_db
from models.ticket import DBTicket
from core.ai_triage import analyze_ticket_nlp

from core.forecasting import predict_future_demand # NEW IMPORT

# Create the database tables automatically when the app starts
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CCS ITSM Ticketing Engine")

# --- NEW: CORS CONFIGURATION ---
# We explicitly allow our Next.js frontend origin to communicate with this API
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"], # Allows all headers (e.g., Content-Type)
)

# --- PYDANTIC MODELS (Data Validation) ---
class TicketRequest(BaseModel):
    location: str
    description: str

class TicketResponse(BaseModel):
    id: int
    location: str
    ai_category: str
    priority_score: int
    status: str

    # NEW: Tells Pydantic to read the SQLAlchemy database object
    model_config = {"from_attributes": True}

# --- API ROUTES ---
# Notice we added `db: Session = Depends(get_db)` to the parameters
@app.post("/api/tickets", response_model=TicketResponse)
async def submit_ticket(ticket: TicketRequest, db: Session = Depends(get_db)):
    """
    Receives ticket, triages via AI, and saves to the PostgreSQL/SQLite database.
    """
    if not ticket.description.strip():
        raise HTTPException(status_code=400, detail="Description cannot be empty.")
        
    # 1. AI Triage
    triage_results = analyze_ticket_nlp(ticket.description)
    
    # 2. Create the Database Record (ORM Object)
    new_ticket = DBTicket(
        location=ticket.location,
        description=ticket.description,
        ai_category=triage_results.get("category"),
        ai_sentiment=triage_results.get("sentiment"),
        priority_score=triage_results.get("priority_score")
    )
    
    # 3. Save to Database
    db.add(new_ticket)       # Stage the insert
    db.commit()              # Execute the transaction
    db.refresh(new_ticket)   # Retrieve the newly generated ID from the database
    
    # 4. Return the saved data to the Next.js frontend
    return new_ticket


@app.get("/api/forecast")
async def get_ticket_forecast():
    """
    Returns a 7-day predictive forecast of ticket volumes 
    using the statsmodels ARIMA algorithm.
    """
    try:
        predictions = predict_future_demand(days_to_predict=7)
        return {"status": "success", "data": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Add this below your other routes in main.py
@app.get("/api/tickets", response_model=list[TicketResponse])
async def get_all_tickets(db: Session = Depends(get_db)):
    """
    Fetches all tickets from the database, mathematically sorted 
    from highest priority down to lowest.
    """
    # We offload the sorting to PostgreSQL for maximum performance
    tickets = db.query(DBTicket).order_by(DBTicket.priority_score.desc()).all()
    return tickets