import os
# setup
ENV = "local"  # server or local
DOWNLOAD_PATH = f"{os.getcwd()}\data\\funds"

# main
BASE_URL = r'https://www.investing.com'
modal_close_xpath = '/html/body/div[7]/div[2]/i'
signin_enter_xpath = '/html/body/div[5]/header/div[1]/div/div[4]/span[1]/div/a[1]'
username_input_xpath = '/html/body/div[9]/div[2]/div[3]/form/div[1]/input'
password_input_xpath = '/html/body/div[9]/div[2]/div[3]/form/div[2]/input'
signin_button_xpath = '/html/body/div[9]/div[2]/a'

# listing
LISTING_URL = r'https://www.investing.com/funds/world-funds?&issuer_filter=0'
list_names_xpath = '/html/body/div[5]/section/table/tbody/tr/td[2]/a'

# individual
price_table_first_row_xpath = '/html/body/div[5]/section/div[9]/table[1]/tbody/tr[1]'
download_button_xpath = '/html/body/div[5]/section/div[8]/div[4]/div/a'
fund_title_xpath = '/html/body/div[5]/section/div[7]/h2'
open_daterange_xpath = '//*[@id="widgetFieldDateRange"]'
start_date_input_xpath = '//*[@id="startDate"]'
apply_button_xpath = '//*[@id="applyBtn"]'
