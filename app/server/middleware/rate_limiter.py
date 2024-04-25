import redis
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime


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

            # Get current date
            todays_date = datetime.utcnow().strftime("%Y-%m-%d")

            # Check if the key exists
            key = f"{todays_date}:{user_id}"
            count = self.redis_client.get(key)
            if count is None:
                # Key doesn't exist, set it with expiration
                self.redis_client.set(key, 0, ex=86400)

            # Get count for user from Redis
            count = self.redis_client.incr(key)


            # Check if count exceeds the limit (e.g. 1000 calls per day)
            if count >= self.max_requests:
                raise HTTPException(
                    status_code=429, detail="Rate limit exceeded")

            # Increment count in Redis
            # self.redis_client.incr(key)

            # Continue processing the request
            response =  await call_next(request)

            return response
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
