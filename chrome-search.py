from selenium import webdriver

search_string = input("Input url or string to search for:")

search_string = search_string.replace(' ', '+')

# need to download chromedriver to work
# https://googlechromelabs.github.io/chrome-for-testing/#stable
browser = webdriver.Chrome() 
  
for i in range(1): 
    matched_elements = browser.get("https://www.google.com/search?q=" +
                                     search_string + "&start=" + str(i)) 