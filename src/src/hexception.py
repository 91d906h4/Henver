class URITooLongError(Exception):
    r"""URI is too long."""

    def __init__(self) -> None:
        super().__init__("Get request longer than max_url_len.")