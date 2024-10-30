from pathlib import Path
import time
import psutil
import pandas as pd
from dev.pipeline.sources.csv_source import CSVDataSource
from dev.utils.logging import setup_pipeline_logging

def run_performance_benchmark():
    """Benchmark pipeline performance with different configurations"""
    logger = setup_pipeline_logging(log_file=Path("logs/benchmark.log"))
    results = []
    
    # Test different batch sizes
    batch_sizes = [100, 500, 1000, 5000]
    csv_path = Path("tests/data/sample_manufacturing_data.csv")
    
    print("\nPerformance Benchmark Results:")
    print("-" * 80)
    print(f"{'Batch Size':^15} | {'Total Time':^15} | {'Memory Usage':^15} | {'Records/Sec':^15}")
    print("-" * 80)
    
    for batch_size in batch_sizes:
        start_time = time.time()
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Process data
        source = CSVDataSource(csv_path, batch_size=batch_size)
        records_processed = 0
        
        for batch in source.extract():
            records_processed += len(batch)
            time.sleep(0.1)  # Simulate processing
        
        # Calculate metrics
        end_time = time.time()
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        total_time = end_time - start_time
        records_per_second = records_processed / total_time
        memory_used = final_memory - initial_memory
        
        print(f"{batch_size:^15} | {total_time:^15.2f} | {memory_used:^15.2f} | {records_per_second:^15.2f}")
        
        results.append({
            'batch_size': batch_size,
            'total_time': total_time,
            'memory_used': memory_used,
            'records_per_second': records_per_second
        })
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    run_performance_benchmark() 