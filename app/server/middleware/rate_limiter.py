import redis
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from server.utils.getTime import timeInSeconds


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
            expiration = timeInSeconds(current_date)

            key = f"{user_id}"
            count = self.redis_client.get(key)

            # Check if the key exists
            if count is None:
                # Assigning count = 1 for the edge case:  max_request = 1
                count = 1
                # If Key doesn't exist, set it with expiration time to the end of day
                self.redis_client.set(key, count, expiration)
                if count > self.max_requests:
                    raise HTTPException(status_code=429, detail="Rate uh limit exceeded")
                response = await call_next(request)
                return response

            # Check if count exceeds the limit
            count = self.redis_client.get(key)
            if int(count) > self.max_requests:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            
            # Get count and increment it for the user
            self.redis_client.incr(key)
            
            response = await call_next(request)

            return response
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code, content={"detail": exc.detail}
            )
