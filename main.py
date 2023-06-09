import asyncio
import json
from playwright.async_api import async_playwright


async def scrape_company_details(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url)
            company_name = await page.inner_text('h1[data-testid="company-name"]')
            company_description = await page.inner_text('div[data-testid="company-description"]')
            ratings = await page.inner_text('span[data-testid="ratings-value"]')
            reviews = await page.inner_text('span[data-testid="reviews-value"]')
            company_data = {
                "Company Name": company_name,
                "Description": company_description,
                "Ratings": ratings,
                "Reviews": reviews
            }
            return company_data
        except Exception as e:
            print(f"An error occurred while scraping {url}: {str(e)}")
        finally:
            await browser.close()


async def scrape_companies(urls):
    tasks = []
    for url in urls:
        tasks.append(scrape_company_details(url))
    scraped_data = await asyncio.gather(*tasks)
    return scraped_data


async def main():
    g2crowd_urls = [
        "https://www.g2.com/companies/example1",
        "https://www.g2.com/companies/example2",
        "https://www.g2.com/companies/example3"
    ]
    scraped_data = await scrape_companies(g2crowd_urls)

    with open('scraped_data.json', 'w') as f:
        json.dump(scraped_data, f, indent=4)

asyncio.run(main())
