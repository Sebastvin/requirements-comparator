from fastapi import APIRouter, File, UploadFile, HTTPException
from src.services.comparison_service import compare_requirements
from src.models.schemas import ComparisonResult
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/compare", response_model=ComparisonResult)
async def compare_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        await validate_files(file1, file2)
        comparison_result = await compare_requirements(file1, file2)
        return comparison_result

    except ValueError as ve:
        logger.warning(f"Invalid input: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error comparing files: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An error occurred while comparing files"
        )


async def validate_files(file1: UploadFile, file2: UploadFile) -> None:
    """
    Validate the uploaded files
    """

    if file1.content_type != "text/plain" or file2.content_type != "text/plain":
        raise ValueError("Both files must be text files")
