# NFL Stats Scraper
NFL Stats Scraper is a Python-based project that allows you to scrape player stats from the NFL website and display them in a GUI. You can also save the stats in a JSON file for later use and plotting.

# Project Structure 
This project is made up of three main components:

The GUI: Built with PyQt5, this provides a user-friendly way to input parameters (such as the URL of the stats page and the type of stats to scrape), trigger the scraping process, and view the analyze.

The Scraper: Utilizing Requests and BeautifulSoup, the scraper accesses the NFL webpage, locates the appropriate table of stats, and extracts the requested information.

Data Processor: This component is responsible for loading and saving JSON files as well as data wrangling and visualization.



```
pip install PyQt5
pip install beautifulsoup4
pip install matplotlib
pip install pandas
pip install seaborn
```

# Usage
1. Run the application. You'll see two tabs: "Scraping" and "JSON Viewer".

2. In the "Scraping" tab, enter the URL of the NFL stats page you want to scrape, and the name of the player whose stats you want. You can also select the type of stats you're interested in (passing, rushing, or receiving) from a dropdown menu.

3. Click the "Scrape" button to start the scraping process. The player's stats will appear in the text area below.

4. If you want to scrape stats for all players listed on the page, click the "Scrape All" button. This will scrape the stats and save them in a JSON file.

5. In the "JSON Viewer" tab, you can load a previously saved JSON file and display its contents. You can also enter player names and stat column names to plot the stats using matplotlib.

