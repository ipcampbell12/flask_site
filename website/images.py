from flask import request
from selenium import webdriver
from selenium.webdriver.common.by import By


PATH = "/Users/iancampbell/Desktop/flask_site/website/chromedriver"

wd = webdriver.Chrome(PATH)


def get_images_from_google(wd, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    search = request.form.get('animal')
    url = f"https://www.google.com/search?q={search}s&tbm=isch"

    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, 'Q4LuWd')

        for img in thumbnails[len(image_urls)+skips:max_images]:
            try:
                img.click()
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, 'n3VNCb')

            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

    return image_urls
