import csv
import sys
import xlsxwriter

from selenium import webdriver
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Firefox()
browser.get("https://www.amazon.com/")
wait = WebDriverWait(browser, 5)


def search(search_item):
    # Find the search box
    input_field = wait.until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    try:
        # Attempt to input the search pamater inside our search box
        browser.execute_script(f"arguments[0].value = '{search_item}';", input_field)
    except JavascriptException as error:
        raise Exception(f"Invalid JS input: {error}")
    # Press search button
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".nav-search-submit"))
    ).click()


def find_element(browser, xpath):
    """Find first DOM element that matches the xpath.
    Returns text of element, or None if the element could not be found.
    """
    try:
        return browser.find_element_by_xpath(xpath).text
    except NoSuchElementException:
        return None


def find_elements(browser, xpath):
    """Find all DOM elements that match the xpath.
    Returns elements, or None if the element could not be found.
    """
    try:
        return wait.until(
            EC.presence_of_element_located((By.XPATH, xpath))
        ).find_elements_by_xpath(xpath)
    except NoSuchElementException:
        return None


def get_products(browser):
    products = []
    # Common div among all results.
    outermost_div = "//div[contains(@data-cel-widget, 'search_result_{}')]"

    # Get number of products in page.
    num_results = len(find_elements(browser, outermost_div.format("")))

    for product in range(num_results):
        product_dict = {}
        sponsored_flag = ""
        product_xpath = outermost_div.format(product)

        try:
            # Check if entry is a sponsored result.
            if find_element(
                browser,
                product_xpath + '//div[@data-component-type="sp-sponsored-result"]',
            ):
                sponsored_flag = "X"
            # Try to get product name.
            product_name = find_element(browser, product_xpath + "//h2//a")

            # Search result entry doesn't contain product name, thus it's not a product entry, skip.
            if not product_name:
                print(
                    f"Product name could not be found for entry, skipping."
                    f"(happens to non-product divs)"
                )
                continue
            # Try to get price for carousel items.
            product_price = find_element(
                browser,
                (
                    product_xpath
                    + "//div[contains(@class, 'a-color-secondary')]//span[@class='a-color-base']"
                ),
            )
            # Get price for regular entries and sponsored results.
            if not product_price:
                product_price = find_element(
                    browser, product_xpath + "//span[@class='a-price']"
                )
            # If we can't find a price, either the result isn't displayed or it's not a product.
            if not product_price:
                print(
                    f"Price could not be found for product {product_name}, skipping "
                    f"(product unavailable)."
                )
                continue
        except Exception as error:
            print(f"Unexpected error while trying to find product: {error}")
            continue
        # Look for repeated products before appending to products.
        if not any(
            product_dict["Product"] == product_name for product_dict in products
        ):
            product_dict["Product"] = product_name
            product_dict["Price"] = product_price.replace("\n", ".")
            product_dict["Sponsored?"] = sponsored_flag
            products.append(product_dict)
            print(product_dict)

    return products


def csv_generator(products, file_name, columns):
    """Creates a .csv file using get_products() function output,
    and vars search_item/file_name as parameters.
    """
    try:
        with open(
            f"{file_name}_results.csv", "w", encoding="utf-8", newline=""
        ) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            for data in products:
                writer.writerow(data)
    except IOError:
        raise IOError("Could not build file due to IOError.")


def excel_generator(products, file_name, columns):
    """Creates a .xlsx file using get_products() function output,
    and vars search_item/file_name as parameters.
    """
    try:
        workbook = xlsxwriter.Workbook(f"{file_name}_results.xlsx")
        worksheet = workbook.add_worksheet(f"{file_name.capitalize()} Sheet")
        cols = 0
        first_row = 0

        # Name header as 'columns' var
        for header in columns:
            cols = columns.index(header)
            worksheet.write(first_row, cols, header)
        rows = 1
        for product in products:
            for key, value in product.items():
                cols = columns.index(key)
                worksheet.write(rows, cols, value)
            rows += 1
    except IOError:
        raise IOError("Could not build file due to IOError.")
    workbook.close()


def main(argv):
    search_item = argv[1]
    file_name = argv[1]
    columns = ["Product", "Price", "Sponsored?"]
    # Perform search on amazon website, argv = search parameter & file name.
    search(search_item)

    try:
        product_output = get_products(browser)
        csv_generator(product_output, file_name, columns)
        excel_generator(product_output, file_name, columns)
    finally:
        browser.quit()


if __name__ == "__main__":
    main(sys.argv)
