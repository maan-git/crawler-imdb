class CrawlerError(Exception):
    """This class defines the base error of the application"""

    def __init__(self, message):
        self.message = message


class CrawlerHttpError(CrawlerError):
    """This class defines the http base error of the application"""

    def __init__(self, message):
        super().__init__(message)