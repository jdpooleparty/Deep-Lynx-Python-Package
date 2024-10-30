from pathlib import Path
import pandas as pd

def create_sample_data():
    """Create sample manufacturing data for demos"""
    # Ensure directory exists
    data_dir = Path("tests/data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample data
    data = {
        'id': [f'EQ{i:03d}' for i in range(1, 6)],
        'equipment_name': ['CNC Machine', '3D Printer', 'Robot Arm', 'Laser Cutter', 'Inspection Station'],
        'process_type': ['Machining', 'Additive', 'Assembly', 'Cutting', 'QC'],
        'duration': [120, 240, 60, 90, 30],
        'status': ['active', 'active', 'maintenance', 'active', 'active']
    }
    
    df = pd.DataFrame(data)
    
    # Save to CSV
    csv_path = data_dir / "sample_manufacturing_data.csv"
    df.to_csv(csv_path, index=False)
    print(f"Sample data created at: {csv_path}")

if __name__ == "__main__":
    create_sample_data() 