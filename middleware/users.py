from django.utils import timezone


class LastRequestMiddleware:
    """
        Middleware saving user's last request
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            user.last_request = timezone.now()
            user.save(update_fields=["last_request"])
        response = self.get_response(request)
        return response
