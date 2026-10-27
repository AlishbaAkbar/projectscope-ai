from redis import Redis
from rq import Queue
from app.config import settings

redis_conn = Redis.from_url(settings.REDIS_URL)
analysis_queue = Queue('analysis', connection=redis_conn)
reports_queue = Queue('reports', connection=redis_conn)
emails_queue = Queue('emails', connection=redis_conn)