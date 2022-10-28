import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import json

if __name__ == '__main__':
    driver = uc.Chrome() # it opens a new chrome window
    driver.get("https://www.linkedin.com/login/ru?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin") # it opens page witn authorization form

    login_field = driver.find_element('id',"username")
    login_field.send_keys("YOURE LOGIN") # write your login
    pass_field = driver.find_element('id',"password")
    pass_field.send_keys("YOURE PASSWORD") # write your password
    login_button = driver.find_element('class name',"btn__primary--large")
    login_button.click()

    driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/") # it opens page with your connections
    time.sleep(5) # wait for page loading
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll down to load all connections

    html= driver.page_source 
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', class_= 'scaffold-finite-scroll__content')

    num = 0
    data={} # dictionary for saving data
    for li in content.find_all('li'): # find all connections and get info about them
        num += 1
        data[num] ={}
        find_link = li.find('div',class_='mn-connection-card__details')
        find_link2 = find_link.find('a')
        url=find_link2.get('href')
        url2 = "https://www.linkedin.com" + url
        driver.get(url2)
        html= driver.page_source
        soup2 = BeautifulSoup(html, 'html.parser')
        nm = soup2.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words')
        name = name.text
        data[num]['name'] = name
        pos = soup2.find('div', class_='text-body-medium break-words') # position/specialisation for job
        if pos != None:
            data[num]['position'] = pos.text
        loc = soup2.find('span', class_='text-body-small inline t-black--light break-words') # location
        if loc != None:
            data[num]['location'] = loc.text.replace('\n','')

    with open('data.json', 'w', encoding='utf-8') as f: # save data to json file
        json.dump(data, f, ensure_ascii=False, indent=4)
