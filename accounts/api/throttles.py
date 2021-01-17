from rest_framework.throttling import AnonRateThrottle


class RegisterThrottle(AnonRateThrottle):
    rate = '3/minute'
