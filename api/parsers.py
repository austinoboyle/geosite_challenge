from rest_framework.parsers import BaseParser


class PlainTextParser(BaseParser):
    """
    Plain text parser.

    Copied from https://www.django-rest-framework.org/api-guide/parsers/#custom-parsers
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()
