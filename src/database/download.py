import kagglehub

# Download latest version
path = kagglehub.dataset_download("austinreese/craigslist-carstrucks-data", output_dir = "../../data/raw")

print("Path to dataset files:", path)