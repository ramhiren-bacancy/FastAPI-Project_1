from datetime import datetime
from app.schemas.response import ApiResponse

def api_response(*, status_code: int, message: str, data=None):
    return ApiResponse(
        statusCode=status_code,
        message=message,
        data=data,
        success=True,
        timestamp=datetime.utcnow()
    )