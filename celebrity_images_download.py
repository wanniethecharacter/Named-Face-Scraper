# Author: Prateek Mehta
# Script to download images from google


import time  # Importing the time library to check the time of code execution
import sys  # Importing the System Library
import os
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

########### Edit From Here ###########

# This list is used to search keywords. You can edit this list to search for google images of your choice. You can simply add and remove elements of the list.
search_keyword = ['Tom Hanks']

# This list is used to further add suffix to your search term. Each element of the list will help you download 100 images. First element is blank which denotes that no suffix is added to the search keyword of the above list. You can edit the list by adding/deleting elements from it.So if the first element of the search_keyword is 'Australia' and the second element of keywords is 'high resolution', then it will search for 'Australia High Resolution'
keywords = [' face',
            ' side face',
            ' looking up',
            ' looking down',
            # ' wearning glasses',
            # ' happy face',
            ' close up']

########### End of Editing ###########


# Downloading entire Web Document (Raw Page Content)
def download_page(url):
    # urllib library for Extracting web pages
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        return respData
    except Exception as e:
        print(str(e))


# Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line+1)
        end_content = s.find(',"ow"', start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


# Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    soup = BeautifulSoup(page, 'html.parser')
    imgs = soup.find_all('img')
    for img in imgs:
        items.append(img.get('src'))
    # while True:
    #     item, end_content = _images_get_next_item(page)
    #     if item == "no_links":
    #         break
    #     else:
    #         # Append all the links in the list named 'Links'
    #         items.append(item)
    #         # Timer could be used to slow down the request for image downloads
    #         time.sleep(0.1)
    #         page = page[end_content:]
    return items


############## Main Program ############
t0 = time.time()  # start the timer

# Download Image Links
i = 0
while i < len(search_keyword):
    items = []
    iteration = "Item no.: " + \
        str(i+1) + " -->" + " Item name = " + str(search_keyword[i])
    print(iteration)
    print("Evaluating...")
    search_keywords = search_keyword[i]
    search = search_keywords.replace(' ', '%20')

    # make a search keyword  directory
    try:
        os.chdir("faces/")
        os.makedirs(search_keywords)
    except OSError as e:
        if e.errno != 17:
            raise
        # time.sleep might help here
        pass

    j = 0
    while j < len(keywords):
        pure_keyword = keywords[j].replace(' ', '%20')
        url = 'https://www.google.com/search?q=' + search + pure_keyword + \
            '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        raw_html = (download_page(url))
        time.sleep(0.1)
        items = items + (_images_get_all_items(raw_html))
        j = j + 1
    # print ("Image Links = "+str(items))
    print("Total Image Links = "+str(len(items)))
    print("\n")

    # This allows you to write all the links into a test file. This text file will be created in the same directory as your code. You can comment out the below 3 lines to stop writing the output to the text file.
    info = open('output.txt', 'a')  # Open the text file called database.txt
    # Write the title of the page
    info.write(str(i) + ': ' +
               str(search_keyword[i-1]) + ": " + str(items) + "\n\n\n")
    info.close()  # Close the file

    t1 = time.time()  # stop the timer
    # Calculating the total time required to crawl, find and download all the links of 60,000 images
    total_time = t1-t0
    print("Total time taken: "+str(total_time)+" Seconds")
    print("Starting Download...")

    # To save imges to the same directory
    # IN this saving process we are just skipping the URL if there is any error

    k = 0
    errorCount = 0
    while (k < len(items)):

        try:
            req = Request(items[k], headers={
                          "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urlopen(req, None, 15)
            print(os.getcwd())
            file_name = search_keywords + "/"+str(k+1)+".jpg"
            output_file = open(file_name, "wb")

            data = response.read()
            output_file.write(data)
            response.close()

            print("completed ====> "+str(k+1))

            k = k+1

        except Exception as e:

            errorCount += 1
            print("Error on image "+str(k+1) + ": " + str(e))
            k = k+1

    i = i+1

print("\n")
print("Everything downloaded!")
print("\n"+str(errorCount)+" ----> total Errors")

# ----End of the main program ----#


# In[ ]:
