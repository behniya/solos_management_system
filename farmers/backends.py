from .models import User
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to authenticate with email
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None