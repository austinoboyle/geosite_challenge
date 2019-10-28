from rest_framework.renderers import BrowsableAPIRenderer


class RequestListRenderer(BrowsableAPIRenderer):
    template = "request-list.html"
