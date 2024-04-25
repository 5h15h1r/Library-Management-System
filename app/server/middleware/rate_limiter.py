import redis
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import time


class RateLimiterMiddleware:
    def __init__(self, redis_url: str, max_requests: int):
        self.max_requests = max_requests
        self.redis_url = redis_url
        self.redis_client = redis.from_url(redis_url)

    async def __call__(self, request: Request, call_next):
        try:
            # Extract user_id from the headers
            user_id = request.headers.get("user_id")
            if not user_id:
                raise HTTPException(
                    status_code=401, detail="Missing user_id in the headers"
                )

            current_date = datetime.utcnow()
            # Calculate the end of the day
            end_of_day = datetime(
                current_date.year, current_date.month, current_date.day, 23, 59, 59
            )
            # Calculate local offset time
            local_timezone_offset_seconds = time.timezone
            remaining_time = end_of_day - current_date
            expiration_time = remaining_time.seconds - +(-local_timezone_offset_seconds)

            key = f"{user_id}"
            count = self.redis_client.get(key)

            # Check if the key exists
            if count is None:
                # Key doesn't exist, set it with expiration
                self.redis_client.set(key, 1, expiration_time)

                # Assigning count = 1 for the edge case:  max_request = 1
                count = 1
                if count > self.max_requests:
                    raise HTTPException(status_code=429, detail="Rate limit exceeded")
                response = await call_next(request)
                return response

            # Get count and increment it for the user
            count = self.redis_client.incr(key)

            # Check if count exceeds the limit
            if count > self.max_requests:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            # Continue processing the request
            response = await call_next(request)

            return response
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code, content={"detail": exc.detail}
            )
