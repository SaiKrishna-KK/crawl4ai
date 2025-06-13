import requests
from .legacy.docs_manager import DocsManager
from .html2text import html2text


class DependencyDocsManager(DocsManager):
    """Manage documentation for third-party dependencies."""

    def __init__(self, dependencies: dict[str, str] | None = None, logger=None):
        super().__init__(logger)
        self.dependencies = dependencies or {}

    async def fetch_dependency_docs(self) -> None:
        """Download and store docs for configured dependencies."""
        for name, url in self.dependencies.items():
            try:
                resp = requests.get(url, timeout=15)
                resp.raise_for_status()
                md = html2text(resp.text)
                doc_file = self.docs_dir / f"{name}.md"
                with open(doc_file, "w", encoding="utf-8") as f:
                    f.write(md)
                self.logger.info(f"Fetched docs for {name}")
            except Exception as e:
                self.logger.error(f"Failed to fetch docs for {name}: {e}")

    async def fetch_docs(self) -> bool:
        """Fetch base docs and then dependency docs."""
        base = await super().fetch_docs()
        await self.fetch_dependency_docs()
        return base
