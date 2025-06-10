import requests
from bs4 import BeautifulSoup
import os
import time

def fetchandsavetofile(url, path):
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Add headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Save raw HTML
        with open(path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Successfully saved HTML to {path}")
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract and save main content
        main_content = soup.find('main')
        if main_content:
            content_path = path.replace('.html', '_content.txt')
            with open(content_path, "w", encoding="utf-8") as f:
                f.write(main_content.get_text(separator='\n', strip=True))
            print(f"Successfully saved main content to {content_path}")
        
        # Extract and save all links
        links = soup.find_all('a')
        links_path = path.replace('.html', '_links.txt')
        with open(links_path, "w", encoding="utf-8") as f:
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                if href and text:
                    f.write(f"{text}: {href}\n")
        print(f"Successfully saved links to {links_path}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except IOError as e:
        print(f"Error saving the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

def main():
    # Example URLs to scrape
    urls = [
        "https://en.wikipedia.org/wiki/Main_Page",
        "https://en.wikipedia.org/wiki/Python_(programming_language)"
    ]
    
    for url in urls:
        print(f"\nScraping: {url}")
        filename = url.split('/')[-1] or 'index'
        path = f"data/{filename}.html"
        fetchandsavetofile(url, path)
        # Be nice to the server - add a delay between requests
        time.sleep(2)

if __name__ == "__main__":
    main()