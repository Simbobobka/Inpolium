import aiohttp
import asyncio
import csv
import re
import json
from bs4 import BeautifulSoup
from pathlib import Path


CSV_OUTPUT = "scraped_data.csv"
PROGRESS_FILE = "progress.json"
SUPPLIER = "igefa Handelsgesellschaft"
INTERMEDIATE_FILE = "intermediate_data.json"
MAIN_URL = "https://store.igefa.de/c/kategorien/f4SXre6ovVohkGNrAvh3zR?page="

# write to csv
def save_to_csv(filename, data, mode="a"):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    file_exists = Path(filename).exists()
    with open(filename, mode, newline='', encoding="utf-8") as csvfile:
        fieldnames = data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)

def save_progress(url):
    if Path(PROGRESS_FILE).exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
    else:
        progress_data = []

    progress_data.append(url)

    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, indent=2)

# Load progress
def load_progress():
    if Path(PROGRESS_FILE).exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

# save to extra dataset
def save_to_intermediate(data):
    if Path(INTERMEDIATE_FILE).exists():
        with open(INTERMEDIATE_FILE, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.append(data)

    with open(INTERMEDIATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)

# Load from JSON to main CSV
def flush_to_csv():
    if not Path(INTERMEDIATE_FILE).exists():
        return
    
    with open(INTERMEDIATE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Write to CSV
    with open(CSV_OUTPUT, "a", newline='', encoding="utf-8") as csvfile:
        if data:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if csvfile.tell() == 0:
                writer.writeheader()
            
            writer.writerows(data)

async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()

# Parsing proces
async def scrape_page(session, url):
    try:
        html = await fetch_html(session, url)
        soup = BeautifulSoup(html, "html.parser")
        # Extract the first product element 
        product = soup.find("div", class_="LYSContainer_padding__21b81") 
        if product is None:
            print("No product found")
            return

        # 1. Product name
        name_element = product.find("h1")
        name = name_element.text.strip() if name_element else "Unknown Product Name"
        
        # 2. Breadcrumb
        breadcrumb_container = soup.find("div", class_="CategoryBreadcrumbs_sectionWrap__b5732")
        if breadcrumb_container:
            breadcrumb_links = breadcrumb_container.find_all("a")
            breadcrumb = "/".join(link.text.strip().lower().replace(" ", "-") for link in breadcrumb_links)
            breadcrumb = re.sub(r"[()]", "", breadcrumb)         
            breadcrumb = re.sub(r"-{2,}", "-", breadcrumb)  
        else:
            breadcrumb = None
            
        # 3. Execution
        execution_div = soup.find("div", class_="ProductInformation_variantInfo__5cb1d")
        execution = execution_div.find("div", class_='ant-typography ant-typography-secondary ProductCard_paragraph__03d53').text.split(": ")[1].strip() if execution_div else None

        # 4. Supplier article number
        supplier_article_number = execution_div.find("div", attrs={"data-testid": "product-information-sku"}).text.split(": ")[1].strip() if execution_div else None
        
        # 5. GTIN
        gtin_element = soup.find("div", attrs={"data-testid": "product-information-gtin"})
        EANGTIN = gtin_element.text.split(": ")[1].strip() if gtin_element else None
        
        # 6. Article number
        article_number = execution_div.text.split()[-1] if execution_div else None
        
        # 7. Product description
        description_element = product.find("div", class_="ProductDescription_description__4e5b7")
        description = description_element.text.strip() if description_element else None
        
        # 8. Supplier URL
        supplier_url = url
        
        # 9. Image URL
        image_url = (
            product.find("div", class_="image-gallery-slide")
            .find("img")['src'] if product.find("div", class_="image-gallery-slide") else None
        )
        
        # 10. Manufacturer
        manufacturer_row = product.find("tr", attrs={"data-row-key": "33"})
        manufacturer = (
            manufacturer_row.find_all("td")[1].text.strip() if manufacturer_row and len(manufacturer_row.find_all("td")) > 1 else None
        )
        
        # 11. Additional description
        benefits_div = soup.find('div', class_='ProductBenefits_productBenefits__1b77a')
        additional_description = ', '.join(li.get_text() for li in benefits_div.find_all('li')) if benefits_div else None

        # Collecting product data
        product_data = {
            "Product Name": name,
            "Original Data Column 1 (Breadcrumb)": breadcrumb,
            "Original Data Column 2 (Ausführung)": execution,
            "Supplier Article Number": supplier_article_number,
            "EAN/GTIN": EANGTIN if EANGTIN else None,  
            "Article Number": article_number,
            "Product Description": description,
            "Supplier": SUPPLIER,
            "Supplier-URL": supplier_url,
            "Product Image URL": image_url,
            "Manufacturer": manufacturer,
            "Original Data Column 3 (Add. Description)": additional_description if additional_description else None,
        }
        save_progress(url)
        save_to_intermediate(product_data)
        print(f"Successfully scraped {url}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        
async def fetch_product_urls(session, page_num):
    url = f"{MAIN_URL}{page_num}"
    html = await fetch_html(session, url)
    soup = BeautifulSoup(html, "html.parser")
    print(f"Fetching product URLs from page {page_num}")

    # Extract product URLs using JSON data in the script tag
    script_tag = soup.find("script", id="__NEXT_DATA__")
    json_data = json.loads(script_tag.string)
    products = json_data.get("props", {}).get("initialProps", {}).get("pageProps", {}).get("initialProductData", {}).get("hits", [])
    
    urls = []
    for product in products:
        attachments = product.get("mainVariant", {})
        product_url = f"https://store.igefa.de/p/{attachments['slug']}/{attachments['id']}"
        urls.append(product_url)
    return urls

# Main scraping logic
async def main():
    processed_urls = load_progress()
    page_num = 1
    max_pages = 500
    async with aiohttp.ClientSession() as session:
        while page_num <= max_pages:
            product_urls = await fetch_product_urls(session, page_num)
            urls_to_process = [url for url in product_urls if url not in processed_urls]
            
            if not urls_to_process:
                print(f"All URLs on page {page_num} have been processed.")
                page_num += 1
                continue
            
            tasks = [scrape_page(session, url) for url in urls_to_process]
            await asyncio.gather(*tasks)
            page_num += 1

    flush_to_csv()

# start program
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted! Flushing intermediate data to CSV...")
        flush_to_csv() 


