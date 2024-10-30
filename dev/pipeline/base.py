from abc import ABC, abstractmethod
from typing import Any, Dict, List, Generator
import pandas as pd

class DataSource(ABC):
    """Abstract base class for data sources"""
    @abstractmethod
    def extract(self) -> Generator[pd.DataFrame, None, None]:
        """Extract data from source in batches"""
        pass

class DataTransformer(ABC):
    """Abstract base class for data transformers"""
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform data according to Deep Lynx schema"""
        pass

class DataLoader(ABC):
    """Abstract base class for loading data into Deep Lynx"""
    @abstractmethod
    def load(self, data: pd.DataFrame) -> bool:
        """Load transformed data into Deep Lynx"""
        pass 