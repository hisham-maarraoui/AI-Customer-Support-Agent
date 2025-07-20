import requests
from bs4 import BeautifulSoup
import json
import os
import time
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleAppleScraper:
    def __init__(self):
        self.base_url = "https://support.apple.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_data = []
        
    def get_support_pages(self) -> List[str]:
        """Get a list of Apple support pages to scrape"""
        # Common Apple support pages for different products
        support_pages = [
            "https://support.apple.com/iphone",
            "https://support.apple.com/ipad", 
            "https://support.apple.com/mac",
            "https://support.apple.com/watch",
            "https://support.apple.com/airpods",
            "https://support.apple.com/tv",
            "https://support.apple.com/iphone/guide",
            "https://support.apple.com/ipad/guide",
            "https://support.apple.com/mac/guide",
            "https://support.apple.com/watch/guide",
            "https://support.apple.com/airpods/guide",
            "https://support.apple.com/tv/guide",
            "https://support.apple.com/iphone/troubleshooting",
            "https://support.apple.com/ipad/troubleshooting", 
            "https://support.apple.com/mac/troubleshooting",
            "https://support.apple.com/watch/troubleshooting",
            "https://support.apple.com/airpods/troubleshooting",
            "https://support.apple.com/tv/troubleshooting"
        ]
        
        # Add some specific support articles
        specific_articles = [
            "https://support.apple.com/en-us/HT201270",  # iPhone reset
            "https://support.apple.com/en-us/HT201263",  # iPad reset
            "https://support.apple.com/en-us/HT201295",  # Mac reset
            "https://support.apple.com/en-us/HT204306",  # Apple Watch reset
            "https://support.apple.com/en-us/HT201945",  # AirPods reset
            "https://support.apple.com/en-us/HT201265",  # iPhone backup
            "https://support.apple.com/en-us/HT201269",  # iPad backup
            "https://support.apple.com/en-us/HT201250",  # Mac backup
            "https://support.apple.com/en-us/HT201296",  # iPhone update
            "https://support.apple.com/en-us/HT204204",  # iPad update
            "https://support.apple.com/en-us/HT201541",  # Mac update
            "https://support.apple.com/en-us/HT204507",  # Apple Watch update
        ]
        
        return support_pages + specific_articles
    
    def scrape_page(self, url: str) -> Dict[str, Any]:
        """Scrape a single support page"""
        try:
            logger.info(f"Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""
            
            # Extract main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content') or soup.find('body')
            
            if main_content:
                # Remove script and style elements
                for script in main_content(["script", "style", "nav", "header", "footer"]):
                    script.decompose()
                    
                content_text = main_content.get_text(separator=' ', strip=True)
            else:
                content_text = soup.get_text(separator=' ', strip=True)
            
            # Clean up content
            content_text = ' '.join(content_text.split())
            
            # Extract product from URL
            product = self._extract_product_from_url(url)
            
            # Extract FAQ items
            faq_items = self._extract_faq_items(soup)
            
            # Extract troubleshooting steps
            troubleshooting = self._extract_troubleshooting(soup)
            
            return {
                'url': url,
                'title': title_text,
                'content': content_text,
                'faq_items': faq_items,
                'troubleshooting': troubleshooting,
                'product': product,
                'scraped_at': time.time()
            }
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return {
                'url': url,
                'title': '',
                'content': '',
                'faq_items': [],
                'troubleshooting': [],
                'product': 'Unknown',
                'scraped_at': time.time(),
                'error': str(e)
            }
    
    def _extract_product_from_url(self, url: str) -> str:
        """Extract product name from URL"""
        url_lower = url.lower()
        if 'iphone' in url_lower:
            return 'iPhone'
        elif 'ipad' in url_lower:
            return 'iPad'
        elif 'mac' in url_lower:
            return 'Mac'
        elif 'watch' in url_lower:
            return 'Apple Watch'
        elif 'airpods' in url_lower:
            return 'AirPods'
        elif 'tv' in url_lower:
            return 'Apple TV'
        else:
            return 'Other'
    
    def _extract_faq_items(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract FAQ items from the page"""
        faq_items = []
        
        # Look for common FAQ patterns
        faq_selectors = [
            'div[class*="faq"]',
            'div[class*="accordion"]',
            'details',
            'div[class*="question"]',
            'h3', 'h4', 'h5'
        ]
        
        for selector in faq_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 10 and '?' in text:
                    # Look for answer in next sibling
                    next_elem = element.find_next_sibling(['p', 'div'])
                    if next_elem:
                        answer = next_elem.get_text(strip=True)
                        if answer and len(answer) > 20:
                            faq_items.append({
                                'question': text,
                                'answer': answer
                            })
                    
        return faq_items
    
    def _extract_troubleshooting(self, soup: BeautifulSoup) -> List[str]:
        """Extract troubleshooting steps from the page"""
        troubleshooting = []
        
        # Look for numbered lists or steps
        step_selectors = [
            'ol li',
            'div[class*="step"]',
            'div[class*="troubleshoot"]',
            'li'
        ]
        
        for selector in step_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 20:  # Filter out very short text
                    troubleshooting.append(text)
                    
        return troubleshooting
    
    def scrape_all_pages(self):
        """Scrape all support pages"""
        pages = self.get_support_pages()
        logger.info(f"Found {len(pages)} pages to scrape")
        
        for i, page in enumerate(pages):
            logger.info(f"Scraping page {i+1}/{len(pages)}: {page}")
            data = self.scrape_page(page)
            if data['content']:
                self.scraped_data.append(data)
            time.sleep(1)  # Be respectful to Apple's servers
            
        logger.info(f"Scraped {len(self.scraped_data)} pages successfully")
        return self.scraped_data
    
    def save_data(self, filename: str = "apple_support_data.json"):
        """Save scraped data to JSON file"""
        os.makedirs("../data", exist_ok=True)
        filepath = os.path.join("../data", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Saved {len(self.scraped_data)} pages to {filepath}")
        return filepath

def main():
    """Main function to run the scraper"""
    scraper = SimpleAppleScraper()
    
    print("Starting Simple Apple Support scraper...")
    print("This will scrape Apple support pages and save them to data/apple_support_data.json")
    
    # Scrape all support pages
    scraped_data = scraper.scrape_all_pages()
    
    # Save the data
    filepath = scraper.save_data()
    
    print(f"Scraping completed! Saved {len(scraped_data)} pages to {filepath}")
    
    # Print summary
    products = {}
    for item in scraped_data:
        product = item.get('product', 'Unknown')
        products[product] = products.get(product, 0) + 1
    
    print("\nScraping Summary:")
    for product, count in products.items():
        print(f"  {product}: {count} pages")

if __name__ == "__main__":
    main() 