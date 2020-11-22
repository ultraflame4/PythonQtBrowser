from dataclasses import dataclass,field


@dataclass()
class BrowserSettings:

    use_urlblacklist : bool = False
    url_blacklist: list = field(default=[])

