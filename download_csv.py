from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import datetime
import log_funcs
import get_password

def date_to_string(date):
    return date.strftime("%A, %B %d, %Y")

def wait_and_click(drvr, address, by_xpath=True):
    """Wait until button is clickable, then click.
    """
    how_By = By.XPATH if by_xpath else By.ID
    to_click = WebDriverWait(drvr, 5).until(EC.element_to_be_clickable((how_By, address)))
    to_click.click()
    time.sleep(0.5)

def download_csv():
    """Go to accela website, login using fixed username and input password, download last week's
    property maintenance csv info into /Downloads.
    """

    # driver = webdriver.Chrome(ChromeDriverManager().install()) # Download Chrome driver.

    username = "talas"
    try:
        password = get_password.get_password() # Get password from user input.
    except Exception as e:
        log_funcs.log_error(e) # Log error.
        sys.exit() # Terminate program.

    url = "https://aca-prod.accela.com/LJCMG/Login.aspx?ReturnUrl=%2fLJCMG%2fCap%2fCapHome.aspx%3fmodule" \
          "%3dEnforcement%26TabName%3dEnforcement%26TabList%3dHome%257C0%257CAPCD%257C1%257CBuilding%257C2" \
          "%257CEnforcement%257C3%257CLicenses%257C4%257CPlanning%257C5%257CPublicWorks%257C6%257CCurrentTabIndex" \
          "%257C3 "

    s = Service("C:\Program Files\Google\Chrome\Application\chromedriver.exe")
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Run as headless.

    time.sleep(3)

    # Get a chrome driver, open url and max window.
    try:
        driver = webdriver.Chrome(options=chrome_options, service=s)
        driver.get(url)
        driver.maximize_window()
    except Exception as e:
        log_funcs.log_error(e)

    time.sleep(3)

    # Enter login info and login.
    try:
        driver.find_element(By.ID, "ctl00_PlaceHolderMain_LoginBox_txtUserId").send_keys(username)
        driver.find_element(By.ID, "ctl00_PlaceHolderMain_LoginBox_txtPassword").send_keys(password)
        driver.find_element(By.ID, "ctl00_PlaceHolderMain_LoginBox_btnLogin").click()
    except Exception as e:
        log_funcs.log_error(e)

    time.sleep(3)

    # Select property maintenance option from selection.
    try:
        select = Select(driver.find_element(By.ID, 'ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType'))
        select.select_by_value("Enforcement/Property Maintenance/Case/NA")
    except Exception as e:
        log_funcs.log_error(e) # Probably wrong password entered.
        sys.exit()

    time.sleep(3)

    # Get today's and a week ago date
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=7)
    a_week_ago = today - delta
    a_week_ago_str = date_to_string(a_week_ago)

    # Choose the correct date.
    try:
        if driver.current_url != "https://aca-prod.accela.com/LJCMG/Cap/CapHome.aspx?module=Enforcement&TabName" \
                                 "=Enforcement&TabList=Home|0|APCD|1|Building|2|Enforcement|3|Licenses|4|Planning|5" \
                                 "|PublicWorks|6|CurrentTabIndex|3":
            raise Exception("Unable to login to page")
        else:
            wait_and_click(
                driver, '//a[@id=\'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate_calendar_button'
                                   '\']//img[ '
                                   '@alt=\'Click to show calendar\']')
            wait_and_click(
                driver, '//div['
                                   '@id'
                                   '=\'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate_calendar_bhv_lnkTitleID'
                                   '\']')
            wait_and_click(
                driver, '//div[@id=\'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate_calendar_bhv_lnkTitleID\']')
            wait_and_click(
                driver, '//div[@id=\'ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate_calendar_bhv_lnkNextArrow'
                        '\']')
            wait_and_click(driver, '//div[normalize-space()=\'' + str(a_week_ago.year) + '\']')
            wait_and_click(driver, '//div[normalize-space()=\'' + a_week_ago.strftime('%b') + '\']')
            wait_and_click(driver, '//div[@title=\'' + a_week_ago_str + '\']')
    except Exception as e:
        log_funcs.log_error(e)
        sys.exit()

    # Click 'Search'.
    wait_and_click(driver, '//span[normalize-space()=\'Search\']')
    time.sleep(1)

    # Click 'Download'.
    wait_and_click(driver, 'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList_gdvPermitListtop4btnExport', False)
    time.sleep(5)

    # Close driver.
    driver.close()

download_csv()