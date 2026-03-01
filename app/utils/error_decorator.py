from functools import wraps
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException,status



# ! Error Handling Try Catch: With Help of Decoder
def db_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except IntegrityError as e:
            db = kwargs.get("db")
            if db:
                await db.rollback()

            # send meaningful error
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Enter Current Data"
            )
        
        except SQLAlchemyError as e:
            db = kwargs.get("db")
            print(e)
            if db:
                await db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
    return wrapper