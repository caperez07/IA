# BaseMemory
from typing import Any, Dict, List
from langchain_core.memory import BaseMemory


class SimpleMemory(BaseMemory):
    memories: Dict[str, Any] = dict()

    @property
    def memory_variables(self) -> List[str]:
        return list(self.memories.keys())

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        return self.memories

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        pass

    def clear(self) -> None:
        pass