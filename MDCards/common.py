from dataclasses import dataclass, asdict


@dataclass()
class Card:
    """ Fields of CSV Header """
    Weight: int = None
    Toolbar: str = None
    Title: str = None
    Body: str = None
    Extra: str = None

    def fieldnames(self):
        return tuple(asdict(self).keys())
