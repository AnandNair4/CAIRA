from abc import ABC, abstractmethod
from ingestion.schema import EvidenceItem

class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, **kwargs) -> EvidenceItem:
        ...
