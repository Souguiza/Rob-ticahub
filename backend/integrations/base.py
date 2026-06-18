from dataclasses import dataclass
from datetime import date
from typing import Protocol


@dataclass(frozen=True)
class ExternalNewsItem:
    title: str
    summary_pt_br: str
    source_name: str
    original_url: str
    program: str
    original_date: date
    official: bool = False


class NewsProvider(Protocol):
    provider_name: str

    def fetch_updates(self) -> list[ExternalNewsItem]:
        """Retorna metadados e resumos proprios, nunca copias integrais de artigos."""
