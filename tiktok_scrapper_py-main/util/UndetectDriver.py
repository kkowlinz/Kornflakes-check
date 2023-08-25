import os, time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import os, time
from webdriver_manager.chrome import ChromeDriverManager


options = uc.ChromeOptions()
options.headless = False
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
options.add_argument('--user-data-dir=C:/Users/'+os.getlogin()+'/AppData/Local/Google/Chrome/User Data/Default/')

driver = uc.Chrome(
    options=options,
    use_subprocess=True,
    executable_path=ChromeDriverManager().install()  # Use webdriver_manager to get the appropriate ChromeDriver
)


def get_page(url):
    driver.implicitly_wait(10)
    driver.get(url)

def get_soup():
    return BeautifulSoup(driver.page_source, "lxml")

def scroll_page_to_the_end():

    old_position = 0
    new_position = None

    while new_position != old_position:
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))

def close_driver():
    driver.close()
    driver.quit()
