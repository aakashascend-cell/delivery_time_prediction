from pathlib import Path

# Use a list of tuples to define (Path, Type)
file_locations = [
    (Path.cwd() / "__init__.py", "file"),
    (Path.cwd() / "src", "dir"),

    (Path.cwd() / "data/raw/", "dir"),
    (Path.cwd() / "data/processed/", "dir"),
    
    (Path.cwd() / "notebooks/EDA.ipynb", "file"),
    
    (Path.cwd() / "api/", "dir"),
    (Path.cwd() / "mlops/", "dir"),
    (Path.cwd() / "requirement.txt","file")
]

for path , path_type in file_locations:
    if path_type== 'dir':
        path.mkdir(parents=True,exist_ok=True)
    
    else:
        path.parent.mkdir(parents=True,exist_ok=True)
        
        if not path.exists() or path.stat().st_size == 0:
            path.touch()
