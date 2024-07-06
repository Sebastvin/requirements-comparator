from fastapi import APIRouter, File, UploadFile
from services.comparison_service import compare_requirements
from models.schemas import ComparisonResult

router = APIRouter()


@router.post("/compare", response_model=ComparisonResult)
async def compare_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    return await compare_requirements(file1, file2)
