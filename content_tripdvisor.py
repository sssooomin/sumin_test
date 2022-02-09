from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver



keyword = "카페베네"      #검색한 키워드


def save_only_review(review,keyword):
    with open(str(str(keyword)+"_only_review.txt"),"a+",encoding='utf-8') as f:
        for i in range(len(review)):
            for j in range(len(review[i])):
                f.write(str(review[i][j]))
                f.write("\n")

def save_only_address(address,keyword):

    with open(str(keyword+"_only_address.txt"),"a+",encoding='utf-8') as f:
        f.write(str(address))
        f.write("\n")

def save_NameAdress(names,address,keyword):
    with open(str(str(keyword)+"_all_thing.txt"),"a+",encoding='utf-8') as f:
        f.write(str("지점명: ",names))
        f.write(str("주소: ",address,"\n"))
def save_ReviewDate(review,date,keyword):
    with open(str(keyword + "_only_review.txt"), "a+",encoding='utf-8') as f:
        for i in range(len(review)):
            for j in range(len(review[i])):
                f.write(str("리뷰: ", review[i][j]))
                f.write(str("날짜: ", date[i][j], "\n"))
def save_all_thing(names,address,review,date,keyword):
    with open(str(str(keyword)+"_all_thing.txt"),"a+",encoding='utf-8') as f:
        f.write(str("지점명: ",names))
        f.write(str("주소: ",address,"\n"))
        for i in range(len(review)):
            for j in range(len(review[i])):
                f.write(str("리뷰: ",review[i][j]))
                f.write(str("날짜: ",date[i][j],"\n"))

def review_date_make(review_tmp,date_tmp):
    review = []
    date= []
    for i in range(len(review_tmp)):
        review_tmp2 = remove_tags(str(review_tmp[i]))
        date_tmp2 = remove_tags(str(date_tmp[i]))

        review.append(review_tmp2)
        date.append(date_tmp2)
    return review,date

def click_more(driver):
    try:
        driver.find_element_by_xpath("//span[@class='taLnk ulBlueLinks' and contains(text(),'더 보기')]").click()
        driver.find_element_by_class_name("").click()

    except:
         pass

def next_page():
    try:
        # this is navigate to next page
        driver.find_element_by_xpath('//a[@class="nav next taLnk ui_button primary"]').click()

        driver.implicitly_wait(2)


        return True
    except :
        return False

def remove_tags(text):
    return TAG_RE.sub('', text)


TAG_RE = re.compile(r'<[^>]+>')






trip_url='https://www.tripadvisor.co.kr'


driver = webdriver.Chrome(
        'C:/Users/Cha/PycharmProject/deeplearning/dms/AutoCrawler-master/chromedriver/chromedriver_win.exe')
with open(keyword+"_tripadviser_link.txt") as f:
    ad=f.read().splitlines()

    for url_naver in ad:
        driver.get(url_naver)
        click_more(driver)
        time.sleep(1.5)
        response = driver.page_source

        soup = BeautifulSoup(response, 'html.parser',
                             from_encoding='utf-8')  # Beautifulsoup로 html의 구조를 정힌진 형태로 만들어냄

        driver.execute_script("window.scrollTo(0, document.body.scrollheight);")

        names = soup.find("h1", {"class": "ui_header"})
        address = soup.find("span", {"class": "detail"})

        names = remove_tags(str(names))
        address = remove_tags(str(address))

        save_only_address(address,keyword)
        with open(str(str(keyword)+"_all_thing.txt"),"a+",encoding='utf-8') as handle:
            handle.write("\n\n")
            handle.write(names)
            handle.write("  ")
            handle.write(address)
            handle.write("\n")
        print(names,address)

        review = []
        date = []

        is_more = True
        while (is_more):

            driver.execute_script("window.scrollTo(0, document.body.scrollheight);")

            click_more(driver)
            time.sleep(1.5)
            driver.implicitly_wait(5)

            response = driver.page_source
            soup = BeautifulSoup(response, 'html.parser',
                                 from_encoding='utf-8')  # Beautifulsoup로 html의 구조를 정힌진 형태로 만들어냄

            review_tmp = soup.findAll("p", {"class": "partial_entry"})
            date_tmp = soup.findAll("span", {"class": "ratingDate"})

            review_tmp,date_tmp=review_date_make(review_tmp,date_tmp)

            review.append(review_tmp)
            date.append(date_tmp)

            is_more = next_page()



        save_only_review(review,keyword)

        #save_all_thing(names,address,review,date,keyword)
        with open(str(str(keyword)+"_all_thing.txt"),"a+",encoding='utf-8') as handle:
            for i in range(len(review)):
                for j in range(len(review[i])):
                    print("#")
                    handle.write(review[i][j])
                    handle.write("  ")
                    handle.write(date[i][j])
                    handle.write("\n")