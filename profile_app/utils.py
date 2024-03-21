from .models import Profile, Courier


def get_profile_or_courier(slug):
    try:
        return Profile.objects.get(user__username=slug), False
    except Profile.DoesNotExist:
        try:
            return Courier.objects.get(user__username=slug), True
        except Courier.DoesNotExist:
            return None, None
