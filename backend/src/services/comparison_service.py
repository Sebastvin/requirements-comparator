from fastapi import UploadFile
from src.models.schemas import ComparisonResult, Package
from src.utils.context_manager import ContextManager
from src.utils.comparator import Comparator
import tempfile
import os


async def compare_requirements(
    file1: UploadFile, file2: UploadFile
) -> ComparisonResult:
    # Create temporary files
    tmp1 = tempfile.NamedTemporaryFile(delete=False)
    tmp2 = tempfile.NamedTemporaryFile(delete=False)

    try:
        tmp1.write(await file1.read())
        tmp2.write(await file2.read())
        tmp1.close()
        tmp2.close()

        cm1 = ContextManager(tmp1.name)
        cm2 = ContextManager(tmp2.name)

        requirements1 = [pkg for pkg in cm1.read_file() if pkg is not None]
        requirements2 = [pkg for pkg in cm2.read_file() if pkg is not None]

        comparator = Comparator(requirements1, requirements2)
        result = comparator.compare()

        return ComparisonResult(
            same=result["same"],
            different=result["different"],
            only_in_first=result["only_in_first"],
            only_in_second=result["only_in_second"],
        )

    finally:
        # Clean up temporary files
        os.unlink(tmp1.name)
        os.unlink(tmp2.name)
