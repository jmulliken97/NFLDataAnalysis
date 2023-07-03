from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')

def get_player_stats(url, stat_type, player_name):
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    
    html = driver.page_source
    print("HTML Content:\n", html[:500])  # Only printing first 500 characters for brevity

    soup = BeautifulSoup(html, 'lxml')
    print("Soup Content:\n", str(soup)[:500])  # Only printing first 500 characters for brevity

    tables = soup.find_all('table', class_='Table')
    print("Tables found: ", len(tables))

    # if no tables found, return a message
    if not tables:
        print('No tables found.')
        return "No tables found."

    # Headers for different stat types
    headers_dict = {
        "passing": ['POS', 'GP', 'CMP', 'ATT', 'CMP%', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'INT', 'SACK', 'SYL', 'QBR', 'RTG'],
        "rushing": ['POS', 'GP', 'ATT', 'YDS', 'AVG', 'LNG', 'BIG', 'TD', 'YDS/G', 'FUM', 'LST', 'FD'],
        "receiving": ['POS', 'GP', 'REC', 'TGTS', 'YDS', 'AVG', 'TD', 'LNG', 'BIG', 'YDS/G', 'FUM', 'LST', 'YAC', 'FD']
    }
    headers = headers_dict[stat_type]

    player_stats = {}

    for table in tables:
        for row in table.tbody.find_all('tr'):
            name_td = row.find('td', attrs={'data-idx': '1'})
            if name_td is None:
                continue
            name = name_td.text

            if name != player_name:  # Skip if the name is not the desired player
                continue

            stats = {}
            for idx, td in enumerate(row.find_all('td')):
                if idx > 1:  # Skip RK and Name tds
                    stat_name = headers[idx-2]  # -2 because we skipped RK and Name
                    stats[stat_name] = td.text
            player_stats[name] = stats
            break  # Once we have found our player, we can break the loop

    # Don't forget to quit the browser
    driver.quit()

    return player_stats


def scrape_all(url, stat_type):
    
    driver = webdriver.Chrome(service=service, options=options)


    driver.get(url)
    
    html = driver.page_source
    print("HTML Content:\n", html[:500])  # Only printing first 500 characters for brevity

    soup = BeautifulSoup(html, 'lxml')
    print("Soup Content:\n", str(soup)[:500])  # Only printing first 500 characters for brevity

    tables = soup.find_all('table', class_='Table')
    print("Tables found: ", len(tables))

    # Headers for different stat types
    headers_dict = {
        "passing": ['POS', 'GP', 'CMP', 'ATT', 'CMP%', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'INT', 'SACK', 'SYL', 'QBR', 'RTG'],
        "rushing": ['POS', 'GP', 'ATT', 'YDS', 'AVG', 'LNG', 'BIG', 'TD', 'YDS/G', 'FUM', 'LST', 'FD'],
        "receiving": ['POS', 'GP', 'REC', 'TGTS', 'YDS', 'AVG', 'TD', 'LNG', 'BIG', 'YDS/G', 'FUM', 'LST', 'YAC', 'FD']
    }
    headers = headers_dict[stat_type]

    all_stats = {}

    for table in tables:
        for row in table.tbody.find_all('tr'):
            name_td = row.find('td', attrs={'data-idx': '1'})
            if name_td is None:
                continue
            name = name_td.text

            stats = {}
            for idx, td in enumerate(row.find_all('td')):
                if idx > 1:  # Skip RK and Name tds
                    stat_name = headers[idx-2]  # -2 because we skipped RK and Name
                    stats[stat_name] = td.text
            all_stats[name] = stats

    # Don't forget to quit the browser
    driver.quit()

    # save all stats to a file
    with open(f'{stat_type}_stats.json', 'w') as f:
        json.dump(all_stats, f)

    print(f"All {stat_type} stats have been saved to {stat_type}_stats.json")
