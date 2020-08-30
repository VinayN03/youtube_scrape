from selenium import webdriver
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time

search_text = ["portable table"]

    video_count = 200

    search_text = search_text.replace(' ', '+')
    url = "https://www.youtube.com/results?search_query="+search_text+"&sp=CAMSAhAB"

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Initialize the Chrome webdriver and open the URL
    driver = webdriver.Chrome(chrome_options=options)

    driver.get(url)
    for n in range(2):
        body = driver.find_element_by_tag_name('body')
        body.send_keys(Keys.END)
        time.sleep(0.5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    mydivs = soup.findAll("div", {"id":"dismissable", "class": "style-scope ytd-video-renderer"})

    video_lst = []
    for i in mydivs:
        a_dict = {}
        a_dict['Video Title'] = i.find("a", attrs={"id": "video-title"})['title']
        a_dict['Video ID'] = i.find("a", attrs={"id": "video-title"})['href'].replace('/watch?v=', '')
        a_dict['Video URL'] = 'https://youtube.com'+i.find("a", attrs={"id": "video-title"})['href']
        a_dict['Video Length'] = ' '.join(i.find("a", attrs={"id": "video-title"})['aria-label'].split()[-4:-2])
        a_dict['Channel Link'] = i.find("ytd-channel-name").find('a')['href']
        a_dict['Channel Name'] = i.find("ytd-channel-name").find('a').get_text()
        a_dict['View Count'] = i.find("a", attrs={"id": "video-title"})['aria-label'].split()[-2]
        a_dict['Description'] = i.find("yt-formatted-string", attrs={"id": "description-text"}).get_text()
        video_lst.append(a_dict)
        
    df = pd.DataFrame(video_lst)
    df.to_csv(search_text+'.csv')