from dataclasses import dataclass


@dataclass
class Event:
    pass


@dataclass
class DomainCommand(Event):
    pass


@dataclass
class IsApprovedAd(DomainCommand):
    ad_oid: str
    is_approved: bool
