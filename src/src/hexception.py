class URITooLongError(Exception):
    def __init__(self) -> None:
        super().__init__("Get request longer than max_url_len.")