# Navigating the DOM: Building a Custom Web Scraper for Business Data

In January 2024, a friend of mine was working on building up their business and hit a massive roadblock: they needed a significant amount of lead data from business directories, and manually copying and pasting was completely unscalable. I offered to step in and build a custom web scraper to automate the extraction process.

### The Thought Process

Building a web scraper is rarely a straightforward task. Modern websites are heavily reliant on JavaScript to render content dynamically, meaning standard HTTP request libraries often just return empty HTML shells. Furthermore, directories often employ basic bot-mitigation techniques. 

To overcome this, I took an iterative approach, running multiple tests and refining the script until it could reliably bypass these hurdles. I realized I needed a browser automation tool to physically wait for the JavaScript to execute and interact with the page elements.

I also integrated a randomized User-Agent rotator. By reading from a text file of legitimate browser user agents (separated by semicolons) and assigning a random one to each session, the script effectively masks its automated nature to avoid triggering immediate rate limits or bans.

### How It Works

The architecture combines Selenium and BeautifulSoup4 to create a robust extraction pipeline. 

First, Selenium launches a Chrome instance with a spoofed User-Agent and navigates to the target URL. The script instructs the browser to wait for the DOM to load, and then programmatically clicks the necessary pagination elements to reveal the desired data blocks. 

Once the data is visibly rendered on the screen, the script grabs the raw HTML source code and passes it over to BeautifulSoup. BeautifulSoup parses the markup, isolates the specific CSS classes containing the company names, and extracts the raw text. Finally, the names are appended to a clean text file for immediate business use.

### The Tech Stack
* **Language:** Python 3.10
* **Libraries:** Selenium, BeautifulSoup4 (bs4), csv, random

### How to Use This Project

1. Clone the repository and install the dependencies from the `requirements.txt` file.
2. Ensure you have a valid Chrome binary and a `useragents.txt` file in the project directory. The text file should use semicolons as delimiters and contain a column titled `useragent`.
3. Update the `TARGET_URL` and `CHROME_BIN` variables in the script.
4. Run the scraper: `python scraper.py`