from django.core.cache import cache
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response


  def __call__(self, request):
    user_id = request.user.id if request.user.is_authenticated else 'anonymous'
    key = f"rate_limit_{user_id}"
    request_count = cache.get(key)

    if request_count and int(request_count) > 100:
      return HttpResponseForbidden("Rate limit exceeded")

    if request_count:
      cache.incr(key)
    else:
      cache.set(key, 1, timeout=60)

    response = self.get_response(request)
    return response