# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt



def scrape_all():
    # Initiate headless driver for deployment   
    executable_path={'executable_path':ChromeDriverManager().install()}
    browser=Browser('chrome',**executable_path,headless=True)
    news_title,news_paragraph=mars_news(browser)

    # Ruuning all scraping functions and store results in a dictionary
    data={
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "img_title_url": url_title(browser)
    }
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url='https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text',wait_time=1)

    html=browser.html
    news_soup=soup(html,'html.parser')

    # Add try/except for error handling
    try:

        #Identified the parent element and created a variable to hold it
        slide_elem=news_soup.select_one('div.list_text')

        slide_elem.find('div',class_='content_title')

        # Use the parent element to find the first 'a' tag and sabe it as 'news_title'
        news_title=slide_elem.find('div',class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p=slide_elem.find('div',class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title,news_p

# ## JPL Space Images Featured Image

# Visit URL
def featured_image(browser):
    url='https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem=browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html=browser.html
    img_soup=soup(html,'html.parser')

    try:
        # Find the relative image url
        img_url_rel=img_soup.find('img',class_='fancybox-image').get('src')
    except AttributeError:
        return None
    # Use the base url to creat ean absolute URL
    img_url=f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url
# ## Mars Facts
def mars_facts():
    try:
        df=pd.read_html('https://galaxyfacts-mars.com')[0] 
    #The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML
    except BaseException:
        return None

    df.columns=['description','Mars','Earth']
    df.set_index('description',inplace=True)

    return df.to_html()

def url_title(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(3,7):
        hemispheres={}
        full_image_elem=browser.find_by_tag('img')[i]
        full_image_elem.click()
        html = browser.html
        img_soup = soup(html, 'html.parser')
        try:
            url_rel='https://marshemispheres.com/'+img_soup.find('div',class_='downloads').find('li').find('a').get('href')
            title=img_soup.find('h2',class_='title').text
        except AttributeError:
            return None
    
        hemispheres['img_url']=url_rel
        hemispheres['title']=title
        hemisphere_image_urls.append(hemispheres)
        browser.back()

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls



