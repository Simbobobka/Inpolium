import aiohttp
import asyncio
import csv
import re
from bs4 import BeautifulSoup
from pathlib import Path

url = [
    "https://store.igefa.de/p/clean-and-clever-smartline-seifencr-me-ros-sma-91-1-sma91-1-seifencreme-12x500ml/k9UiS8fZKdKxrhxcZGuqx7",
    "https://store.igefa.de/p/kolibri-comface-mundschutz-3-lagig-typ-iir-en-14683-typ-iir-40/GyXZ2QS4JRzY9isZWkHU4V",
    "https://store.igefa.de/p/hydrovital-classic-duschgel-hydrovital-classic-duschgel-250-ml-eine-erfrischende-reinigung-fuer-jeden-tag-250-ml/Np2oJkZtF58QNBQnnLd8B5"   
    ]
CSV_OUTPUT = "scraped_data.csv"
PROGRESS_FILE = "progress.csv"
SUPPLIER = "igefa Handelsgesellschaft"

# write to csv
def save_to_csv(filename, data, mode="a"):
    # Ensure the directory exists
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    file_exists = Path(filename).exists()
    with open(filename, mode, newline='', encoding="utf-8") as csvfile:
        fieldnames = data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        # Write the data row
        writer.writerow(data)

async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()

# Parsing proces
async def scrape_page(session, url):
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
    
    # for k, v in product_data.items():
    #     print(f'{k} : {v}')
    save_to_csv(CSV_OUTPUT, product_data)

# run main scrape proces
async def main():  
    async with aiohttp.ClientSession() as session:
        tasks = []
        for link in url:
            tasks.append(scrape_page(session, link))
        await asyncio.gather(*tasks)

# start program
if __name__ == "__main__":
    asyncio.run(main())


