import requests
import gzip
import os
import shutil

# Function to download and decompress a file
def download_and_decompress_file(url, filename):
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    # Decompress the downloaded gzip file
    with gzip.open(filename, 'rb') as f_in:
        with open(filename[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Remove the original compressed file
    os.remove(filename)

# Base URL for the files
base_url = "https://data.gharchive.org/2015-01-01-{}.json.gz"

# Download and decompress files from 0 to 23
for i in range(24):
    url = base_url.format(i)
    filename = f"2015-01-01-{i}.json.gz"
    download_and_decompress_file(url, filename)
    print(f"File {i} downloaded and decompressed.")
