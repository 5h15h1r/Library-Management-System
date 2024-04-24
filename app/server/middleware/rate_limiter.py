import redis
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta


"""
A Basic approach would look like this

user_id = request.headers.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Missing user_id in headers")

        today_date = datetime.utcnow().strftime("%Y-%m-%d")

        # Get count for user from Redis
        count = self.redis_client.get(f"{today_date}:{user_id}")
        if count is None:
            count = 0
        else:
            count = int(count)

        if count >= 10:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        self.redis_client.incr(f"{today_date}:{user_id}")

        # Set TTL for the key to automatically reset count the next day
        self.redis_client.expireat(f"{today_date}:{user_id}", int((datetime.utcnow() + timedelta(days=1)).timestamp()))

        response = call_next(request)

        return response
"""


class RateLimiterMiddleware:
    def __init__(self, redis_url: str, window_size: int, max_requests: int):
        self.redis_url = redis_url
        self.window_size = window_size  # in seconds
        self.max_requests = max_requests
        self.redis_client = redis.from_url(redis_url)

    async def __call__(self, request, call_next):
        """
        Sliding Window approach
        """

        try:
            user_id = request.headers.get("user_id")
            if not user_id:
                raise HTTPException(status_code=401, detail="Missing user_id in headers")

            now = datetime.utcnow()
            window_start = now - timedelta(seconds=self.window_size)
            window_start_timestamp = int(window_start.timestamp())
            
            # Get count for user within the window from Redis
            count = self.redis_client.zcount(
                f"{user_id}:requests", window_start_timestamp, now.timestamp()
            )

            # Check if count exceeds the limit
            if count >= self.max_requests:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            # Add current request timestamp to Redis sorted set
            self.redis_client.zadd(
                f"{user_id}:requests", {now.timestamp(): now.timestamp()}
            )

            # Remove old requests from Redis sorted set
            self.redis_client.zremrangebyscore(
                f"{user_id}:requests", 0, window_start_timestamp
            )

            response = await call_next(request)

            return response
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})