from django.db import models
from django.db import models
from enum import Enum


class RequestType(Enum):
    """
    Enumerated HTTP request types.
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"

    @classmethod
    def choices(cls):
        return [(req.name, req.value) for req in cls]


class Request(models.Model):
    """
    Model to capture HTTP requests made to the API.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    request_type = models.CharField(
        max_length=10, choices=RequestType.choices(), null=False, blank=False)
    comment = models.CharField(max_length=255, null=True)

    class Meta:

        ordering = ['-created_at']
