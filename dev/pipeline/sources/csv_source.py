from typing import Generator
import pandas as pd
from pathlib import Path
from ..base import DataSource

class CSVDataSource(DataSource):
    """CSV file data source implementation"""
    def __init__(self, file_path: Path, batch_size: int = 1000, **kwargs):
        self.file_path = file_path
        self.batch_size = batch_size
        self.kwargs = kwargs
    
    def extract(self) -> Generator[pd.DataFrame, None, None]:
        """Extract data from CSV in batches"""
        for chunk in pd.read_csv(
            self.file_path, 
            chunksize=self.batch_size,
            **self.kwargs
        ):
            yield chunk 