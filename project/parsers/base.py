"""Base parser class for all parsers."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParsedVenue:
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    district: Optional[str] = None
    category_name: Optional[str] = None
    source_url: Optional[str] = None


@dataclass
class ParsedEvent:
    title: str
    description: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    time: Optional[str] = None
    price: Optional[str] = None
    age_rating: Optional[str] = None
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    category_name: Optional[str] = None
    source_url: Optional[str] = None
    image_url: Optional[str] = None


class BaseParser(ABC):
    """Abstract base class for all parsers."""

    name: str = "base"

    @abstractmethod
    def parse_venues(self) -> list[ParsedVenue]:
        ...

    @abstractmethod
    def parse_events(self) -> list[ParsedEvent]:
        ...
