"""Source attribution records for model extraction."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from types import MappingProxyType


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


class SourceConflictError(ValueError):
    """Raised when one source ID points to conflicting references."""


@dataclass(frozen=True, slots=True)
class ProvenanceLedger:
    """Immutable source registry for source-backed model records."""

    sources: Mapping[str, SourceReference]

    def __post_init__(self) -> None:
        if not self.sources:
            raise ValueError("sources must not be empty")
        object.__setattr__(self, "sources", MappingProxyType(dict(self.sources)))

    @classmethod
    def from_sources(cls, sources: Iterable[SourceReference]) -> "ProvenanceLedger":
        """Build a ledger while rejecting conflicting duplicate source IDs."""

        indexed: dict[str, SourceReference] = {}
        for source in sources:
            existing = indexed.get(source.source_id)
            if existing is not None and existing != source:
                raise SourceConflictError(
                    f"conflicting source reference for source_id: {source.source_id}"
                )
            indexed[source.source_id] = source
        return cls(indexed)

    @property
    def source_ids(self) -> tuple[str, ...]:
        """Return source IDs in insertion order."""

        return tuple(self.sources)

    def get(self, source_id: str) -> SourceReference:
        """Return a source reference by ID."""

        return self.sources[source_id]

    def resolve(self, source_ids: Iterable[str]) -> tuple[SourceReference, ...]:
        """Resolve source IDs into source references."""

        return tuple(self.get(source_id) for source_id in source_ids)

    def metadata_for(self, source_ids: Iterable[str]) -> dict[str, str]:
        """Return adapter-friendly string metadata for source IDs."""

        references = self.resolve(source_ids)
        metadata = {
            "source_ids": ",".join(reference.source_id for reference in references),
            "source_titles": "|".join(reference.title for reference in references),
            "source_locators": "|".join(
                f"{reference.source_id}={reference.locator}"
                for reference in references
            ),
        }
        source_urls = "|".join(
            f"{reference.source_id}={reference.url}"
            for reference in references
            if reference.url is not None
        )
        if source_urls:
            metadata["source_urls"] = source_urls
        return metadata


__all__ = ["ProvenanceLedger", "SourceConflictError", "SourceReference"]
