import requests
import gzip
import json  # Import the json module
# Rest of your code...


# Function to download and decompress a file
def download_and_decompress_file(url):
    response = requests.get(url, stream=True)
    print(response.status_code)
    # Check if the request was successful
    if response.status_code == 200:
        with gzip.GzipFile(fileobj=response.raw) as f:
            content = f.read()

        return content

# Base URL for the files

# List to store the URLs of the repositories
urls_list = []


def func(base_url):
    for i in range(24):
        url = base_url.format(i)
        content = download_and_decompress_file(url)
        content_str = content.decode()  # Decode bytes to a string

    # Assuming the data is in JSON format, you can use your preferred JSON parsing method here
    # For example, if the data is a list of dictionaries, you can extract URLs like this:
    # import json
    # data = json.loads(content_str)
    # for item in data:
    #     urls_list.append(item['url'])

    # For demonstration purposes, let's assume we're extracting URLs from each line of JSON data
    # If the data is not in JSON format, adjust the extraction method accordingly
        lines = content_str.strip().split('\n')
        for line in lines:
            try:
                item = json.loads(line)
                if 'repo' in item and 'url' in item['repo']:
                    urls_list.append(item['repo']['url'])
                    #print(item['repo']['url'])
            except json.JSONDecodeError:
                print(f"Error decoding JSON from line: {line}")


            if len(urls_list) >= 110:
                break
        if len(urls_list) >= 110:
            break
    return(urls_list)



if __name__ == '__main__':
    base_url = "https://data.gharchive.org/2015-01-01-{}.json.gz"
    urls_list = func(base_url)

    # Print the list of URLs
    print("List of URLs:")
    for url in urls_list:
        print(url)
