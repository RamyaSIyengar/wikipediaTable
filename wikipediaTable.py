import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def findTotalArticlesByLanguages(languages: []):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table")

    # Locate the table under the "1,000,000+ articles" section
    table_xpath = "//h3[@id='1_000_000+_articles']/parent::div/following-sibling::table[1]"
    rows = driver.find_elements(By.XPATH, f"{table_xpath}//tbody/tr")  # Rows in the table body

    # Parse the table to create a dictionary of language and articles
    language_article_map = {}
    for row in rows:
        # Get language from column 2
        language = row.find_element(By.XPATH, "td[2]").text.strip()

        # Get articles from column 5
        # Remove commas from the article number
        articles = (row.find_element(By.XPATH, "td[5]").
                    text.strip().replace(',', ''))

        # Ensure that articles is a valid number
        if articles.isdigit():
            language_article_map[language] = int(articles)

    total_articles = 0
    for lang in languages:
        total_articles += language_article_map.get(lang, 0)
    driver.quit()
    return total_articles


languages = ["English", "German"]
total = findTotalArticlesByLanguages(languages)
print(f"Total articles for {languages}: {total}")


