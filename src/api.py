"""
=============================================================================
SNU STUDY BUDDY FINDER - FASTAPI BACKEND
=============================================================================
RESTful API for study buddy recommendations
=============================================================================
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="SNU Study Buddy Finder API",
    description="AI-powered study buddy recommendation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model artifacts
try:
    model_artifacts = joblib.load('buddy_model.joblib')
    similarity_matrix = model_artifacts['similarity_matrix']
    df_clean = model_artifacts['df_clean']
    model_version = model_artifacts.get('model_version', '2.0_improved')
    print(f"✅ Model loaded successfully (version: {model_version})")
except FileNotFoundError:
    print("❌ Model file not found. Please run the improved model training first.")
    model_artifacts = None
    similarity_matrix = None
    df_clean = None
    model_version = "unknown"

# Pydantic models for API
class RecommendationRequest(BaseModel):
    student_id: int = Field(..., description="Student ID (index)", ge=0)
    top_n: int = Field(5, description="Number of recommendations", ge=1, le=20)
    min_similarity: float = Field(0.0, description="Minimum similarity threshold", ge=0.0, le=1.0)
    filter_by_cluster: bool = Field(False, description="Filter by same personality cluster")
    filter_by_club: bool = Field(False, description="Filter by same primary club")
    filter_by_hobby: bool = Field(False, description="Filter by same primary hobby")
    filter_by_teamwork: bool = Field(False, description="Filter by similar teamwork level")

class StudentProfile(BaseModel):
    student_id: int
    teamwork_preference: float
    introversion_extraversion: float
    books_read_past_year: int
    club_top1: str
    club_top2: str
    hobby_top1: str
    hobby_top2: str
    weekly_hobby_hours: float
    risk_taking: float
    conscientiousness: float
    open_to_new_experiences: float
    cluster: int

class Recommendation(BaseModel):
    student_id: int
    similarity_score: float
    compatibility_percentage: float
    confidence: str
    profile: StudentProfile

class RecommendationResponse(BaseModel):
    request_student_id: int
    total_recommendations: int
    recommendations: List[Recommendation]
    timestamp: str

class SystemStats(BaseModel):
    total_students: int
    total_clusters: int
    total_clubs: int
    total_hobbies: int
    avg_similarity: float
    model_version: str

# Helper functions
def get_confidence_level(score: float) -> str:
    """Get confidence level based on similarity score"""
    if score >= 0.6:
        return "High"
    elif score >= 0.4:
        return "Medium"
    else:
        return "Low"

def get_student_profile(student_idx: int) -> StudentProfile:
    """Get student profile by index"""
    student = df_clean.iloc[student_idx]
    return StudentProfile(
        student_id=student_idx,
        teamwork_preference=float(student['teamwork_preference']),
        introversion_extraversion=float(student['introversion_extraversion']),
        books_read_past_year=int(student['books_read_past_year']),
        club_top1=str(student['club_top1']),
        club_top2=str(student['club_top2']),
        hobby_top1=str(student['hobby_top1']),
        hobby_top2=str(student['hobby_top2']),
        weekly_hobby_hours=float(student['weekly_hobby_hours']),
        risk_taking=float(student['risk_taking']),
        conscientiousness=float(student['conscientiousness']),
        open_to_new_experiences=float(student['open_to_new_experiences']),
        cluster=int(student['Cluster'])
    )

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SNU Study Buddy Finder API",
        "version": "1.0.0",
        "status": "active" if model_artifacts else "model not loaded",
        "endpoints": {
            "recommendations": "/api/recommendations",
            "student": "/api/student/{student_id}",
            "stats": "/api/stats",
            "health": "/api/health"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if model_artifacts else "unhealthy",
        "model_loaded": model_artifacts is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/stats", response_model=SystemStats)
async def get_system_stats():
    """Get system statistics"""
    if model_artifacts is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return SystemStats(
        total_students=len(df_clean),
        total_clusters=int(df_clean['Cluster'].nunique()),
        total_clubs=int(df_clean['club_top1'].nunique()),
        total_hobbies=int(df_clean['hobby_top1'].nunique()),
        avg_similarity=float(similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)].mean()),
        model_version=model_version
    )

@app.get("/api/student/{student_id}", response_model=StudentProfile)
async def get_student(student_id: int):
    """Get student profile by ID"""
    if model_artifacts is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if student_id < 0 or student_id >= len(df_clean):
        raise HTTPException(status_code=404, detail=f"Student ID {student_id} not found")
    
    return get_student_profile(student_id)

@app.post("/api/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get study buddy recommendations"""
    if model_artifacts is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    student_id = request.student_id
    
    # Validate student ID
    if student_id < 0 or student_id >= len(df_clean):
        raise HTTPException(status_code=404, detail=f"Student ID {student_id} not found")
    
    # Get similarity scores
    similarities = similarity_matrix[student_id].copy()
    
    # Create DataFrame for filtering
    candidates = pd.DataFrame({
        'student_id': range(len(df_clean)),
        'similarity': similarities
    })
    
    # Exclude the student themselves
    candidates = candidates[candidates['student_id'] != student_id]
    
    # Apply minimum similarity filter
    candidates = candidates[candidates['similarity'] >= request.min_similarity]
    
    # Apply additional filters
    student_profile = df_clean.iloc[student_id]
    
    if request.filter_by_cluster:
        student_cluster = student_profile['Cluster']
        candidates = candidates[
            candidates['student_id'].apply(lambda x: df_clean.iloc[x]['Cluster'] == student_cluster)
        ]
    
    if request.filter_by_club:
        student_club = student_profile['club_top1']
        candidates = candidates[
            candidates['student_id'].apply(lambda x: df_clean.iloc[x]['club_top1'] == student_club)
        ]
    
    if request.filter_by_hobby:
        student_hobby = student_profile['hobby_top1']
        candidates = candidates[
            candidates['student_id'].apply(lambda x: df_clean.iloc[x]['hobby_top1'] == student_hobby)
        ]
    
    if request.filter_by_teamwork:
        teamwork = student_profile['teamwork_preference']
        candidates = candidates[
            candidates['student_id'].apply(
                lambda x: abs(df_clean.iloc[x]['teamwork_preference'] - teamwork) <= 1
            )
        ]
    
    # Sort by similarity and get top N
    candidates = candidates.sort_values('similarity', ascending=False).head(request.top_n)
    
    # Build recommendations
    recommendations = []
    for _, row in candidates.iterrows():
        rec_id = int(row['student_id'])
        sim_score = float(row['similarity'])
        
        recommendations.append(Recommendation(
            student_id=rec_id,
            similarity_score=sim_score,
            compatibility_percentage=sim_score * 100,
            confidence=get_confidence_level(sim_score),
            profile=get_student_profile(rec_id)
        ))
    
    return RecommendationResponse(
        request_student_id=student_id,
        total_recommendations=len(recommendations),
        recommendations=recommendations,
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/students")
async def list_students(skip: int = 0, limit: int = 100):
    """List all students with pagination"""
    if model_artifacts is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    total = len(df_clean)
    students = []
    
    for i in range(skip, min(skip + limit, total)):
        students.append({
            "student_id": i,
            "cluster": int(df_clean.iloc[i]['Cluster']),
            "teamwork_preference": float(df_clean.iloc[i]['teamwork_preference']),
            "club_top1": str(df_clean.iloc[i]['club_top1'])
        })
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "students": students
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting SNU Study Buddy Finder API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
