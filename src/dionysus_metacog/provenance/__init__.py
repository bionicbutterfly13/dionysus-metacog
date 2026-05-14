"""Source attribution records for model extraction."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceReference:
    """Citation pointer for a model element or extracted claim."""

    source_id: str
    title: str
    locator: str
    url: str | None = None

    def __post_init__(self) -> None:
        if not self.source_id:
            raise ValueError("source_id must not be empty")
        if not self.title:
            raise ValueError("title must not be empty")
        if not self.locator:
            raise ValueError("locator must not be empty")


__all__ = ["SourceReference"]
