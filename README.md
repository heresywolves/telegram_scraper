# **Telegram Scraper**

## Collects usernames from groups into excel files.

__________________________________________________
### Instructions
Have git and python installed
```
pip install python
pip install git
```
Clone this repository
```
git clone https://github.com/sifersphynx/telegram_scraper.git
```
Install script dependencies
```
pip install telethon
pip install pandas
```
Go to https://my.telegram.org/apps and create an API.
Open scrape.py and paste in your created API information
```
api_id = 2362365435
api_hash = '406b124a883756fefsg24g24g'
phone = '+76668887777'
```
Run the script
```
python scrapy.py
```
It would ask for access verification. A code will be sent to your telegram account. Enter in the numbers and follow terminal instructions.
_________________________________________________
Note: Default export is in xlsx format. Uncomment "data_to_csv" function in the end of the script for a csv format.
