from datetime import date

from integrations.base import ExternalNewsItem, NewsProvider


class MockOfficialNewsProvider(NewsProvider):
    provider_name = "mock-official-news"

    def fetch_updates(self) -> list[ExternalNewsItem]:
        return [
            ExternalNewsItem(
                title="Atualizacao simulada de temporada",
                summary_pt_br="Resumo proprio para demonstrar a futura camada de integracao oficial.",
                source_name="Fonte oficial simulada",
                original_url="https://www.firstinspires.org/",
                program="FRC",
                original_date=date.today(),
                official=True,
            )
        ]
