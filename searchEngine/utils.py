from selenium import webdriver
import time
from selenium.webdriver.common import keys
import re
from selenium.common.exceptions import NoSuchElementException

def check_exists_by_class_name(cname,driver):
    try:
        driver.find_element_by_id(cname)
    except NoSuchElementException:
        return False
    return True


def myfunc(searchword):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    prefs = {'profile.managed_default_content_settings.images':2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path='/home/mahmed/Desktop/reviewWebsite/searchEngine/chromedriver',chrome_options = options)
        

    driver.get("https://www.amazon.com/")
    time.sleep(2)

    search = driver.find_element_by_id("twotabsearchtextbox")
    search.send_keys(searchword)
    time.sleep(2)

    search.send_keys(keys.Keys.ENTER)
    time.sleep(2)

    links = []
    names = []

    elems = driver.find_elements_by_class_name("s-access-title")


    for name in elems:
        if name.text != "":
            links.append(name.text)

    
    #elems = driver.find_elements_by_class_name("s-access-detail-page")


    #for name in elems:
    #    if name.text != "":
    #        links.append(name.text)


    currenturl = driver.current_url
    driver.quit()
    return (links , currenturl)

def getreviews(pagelink,pname):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    prefs = {'profile.managed_default_content_settings.images':2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path='/home/mahmed/Desktop/reviewWebsite/searchEngine/chromedriver',chrome_options = options)
    driver.get(str(pagelink))
    time.sleep(2)

    print(pname)

    #driver.find_element_by_class_name('a-size-base').click()
    driver.find_element_by_link_text(str(pname)).click()
    time.sleep(2)


    revtitle = []
    rev = []
    rat = []

    if check_exists_by_class_name('dp-summary-see-all-reviews',driver):
        driver.find_element_by_id('dp-summary-see-all-reviews').click()

        time.sleep(2)

        rating = driver.find_elements_by_class_name("arp-rating-out-of-text")

        for review in rating:
            rat.append(review.text)


        noofreviews = driver.find_element_by_class_name('totalReviewCount')

        count = int(noofreviews.text)

        c = 1

        while c == 1:
        #print(count)
            reviews = driver.find_elements_by_class_name("review-text")
            reviewstitle = driver.find_elements_by_class_name("review-title")

            for review in reviews:
                rev.append(review.text)
                #rev.append("\n")
                #rev.append('======================================================================================================')

            for review in reviewstitle:
                revtitle.append(review.text)

            count =count-10

            if count<10:
                c=2
            else:
                driver.find_element_by_class_name("a-last").click()
            time.sleep(2)

    else:
        rev.append('No Reviews Present For This Product')


    driver.quit()

    return (rev , rat)
