import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import json
import os
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AppleSupportScraper:
    def __init__(self):
        self.base_url = "https://support.apple.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.driver = None
        self.scraped_data = []
        
    def setup_driver(self):
        """Setup Chrome driver with headless options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def close_driver(self):
        """Close the Chrome driver"""
        if self.driver:
            self.driver.quit()
            
    def get_product_categories(self) -> List[Dict[str, str]]:
        """Get all product categories from Apple support"""
        categories = []
        
        try:
            response = self.session.get(self.base_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find product category links
            category_links = soup.find_all('a', href=True)
            
            for link in category_links:
                href = link.get('href')
                if href and any(product in href.lower() for product in ['iphone', 'ipad', 'mac', 'watch', 'airpods', 'tv']):
                    categories.append({
                        'name': link.get_text(strip=True),
                        'url': urljoin(self.base_url, href),
                        'product': self._extract_product_from_url(href)
                    })
                    
        except Exception as e:
            logger.error(f"Error getting product categories: {e}")
            
        return categories
    
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
    
    def scrape_support_page(self, url: str) -> Dict[str, Any]:
        """Scrape a single support page"""
        try:
            if self.driver:
                self.driver.get(url)
                time.sleep(2)
                
                # Wait for content to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                page_source = self.driver.page_source
            else:
                response = self.session.get(url)
                page_source = response.text
                
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""
            
            # Extract main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            
            if main_content:
                # Remove script and style elements
                for script in main_content(["script", "style"]):
                    script.decompose()
                    
                content_text = main_content.get_text(separator=' ', strip=True)
            else:
                content_text = soup.get_text(separator=' ', strip=True)
            
            # Extract FAQ items if present
            faq_items = self._extract_faq_items(soup)
            
            # Extract troubleshooting steps
            troubleshooting = self._extract_troubleshooting(soup)
            
            return {
                'url': url,
                'title': title_text,
                'content': content_text,
                'faq_items': faq_items,
                'troubleshooting': troubleshooting,
                'product': self._extract_product_from_url(url),
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
    
    def _extract_faq_items(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract FAQ items from the page"""
        faq_items = []
        
        # Look for common FAQ patterns
        faq_selectors = [
            'div[class*="faq"]',
            'div[class*="accordion"]',
            'details',
            'div[class*="question"]'
        ]
        
        for selector in faq_selectors:
            elements = soup.select(selector)
            for element in elements:
                question_elem = element.find(['h3', 'h4', 'h5', 'summary'])
                answer_elem = element.find(['div', 'p', 'span'])
                
                if question_elem and answer_elem:
                    faq_items.append({
                        'question': question_elem.get_text(strip=True),
                        'answer': answer_elem.get_text(strip=True)
                    })
                    
        return faq_items
    
    def _extract_troubleshooting(self, soup: BeautifulSoup) -> List[str]:
        """Extract troubleshooting steps from the page"""
        troubleshooting = []
        
        # Look for numbered lists or steps
        step_selectors = [
            'ol li',
            'div[class*="step"]',
            'div[class*="troubleshoot"]'
        ]
        
        for selector in step_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 10:  # Filter out very short text
                    troubleshooting.append(text)
                    
        return troubleshooting
    
    def scrape_all_support_pages(self, max_pages: int = 100):
        """Scrape all support pages"""
        try:
            self.setup_driver()
            
            # Get product categories
            categories = self.get_product_categories()
            logger.info(f"Found {len(categories)} product categories")
            
            scraped_count = 0
            
            for category in categories:
                if scraped_count >= max_pages:
                    break
                    
                logger.info(f"Scraping category: {category['name']}")
                
                # Scrape the category page
                category_data = self.scrape_support_page(category['url'])
                if category_data['content']:
                    self.scraped_data.append(category_data)
                    scraped_count += 1
                
                # Find and scrape sub-pages
                try:
                    response = self.session.get(category['url'])
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find links to other support pages
                    links = soup.find_all('a', href=True)
                    for link in links:
                        if scraped_count >= max_pages:
                            break
                            
                        href = link.get('href')
                        if href and 'support.apple.com' in href and href not in [d['url'] for d in self.scraped_data]:
                            logger.info(f"Scraping sub-page: {href}")
                            page_data = self.scrape_support_page(href)
                            if page_data['content']:
                                self.scraped_data.append(page_data)
                                scraped_count += 1
                                
                except Exception as e:
                    logger.error(f"Error scraping sub-pages for {category['name']}: {e}")
                    
        finally:
            self.close_driver()
            
        logger.info(f"Scraped {len(self.scraped_data)} pages total")
        return self.scraped_data
    
    def save_data(self, filename: str = "apple_support_data.json"):
        """Save scraped data to JSON file"""
        os.makedirs("data", exist_ok=True)
        filepath = os.path.join("data", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Saved {len(self.scraped_data)} pages to {filepath}")
        return filepath

def main():
    """Main function to run the scraper"""
    scraper = AppleSupportScraper()
    
    print("Starting Apple Support scraper...")
    print("This will scrape Apple support pages and save them to data/apple_support_data.json")
    
    # Scrape all support pages
    scraped_data = scraper.scrape_all_support_pages(max_pages=50)
    
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