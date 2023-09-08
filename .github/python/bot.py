import argparse
import os
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def main(url: str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument("--connect-timeout=10")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(url)
    driver.maximize_window()

    time.sleep(3)
    divs = driver.find_elements_by_xpath('/html/body/main/div[2]/div')

    items = []
    for div in divs:
        account = div.find_element_by_xpath('.//button[1]/span').text
        passwd = div.find_element_by_xpath('.//button[2]/span').text
        if account:
            items.append(account + ',' + passwd)

    with open(os.getcwd() + "/README.md", encoding="utf-8", mode='w') as f:
        f.write("# 免费 OpenAI 账号<br>\n")
        f.write("## 官方登录地址：https://chat.openai.com/\n如果太多人共用账号登录失败，请换账号重新登录\n\n")

        f.write("| --- | --- | --- |\n")
        f.write("|:--- |:--- |:--- |\n")

        num = 0
        contents = "|"
        for item in items:

            if num == 3:
                num = 0
                f.write("{}\n".format(contents))
                contents = "|"
            else:
                num += 1
                splitStr = f"{item}".split(",")
                contents += "账号：{} <br> 🔑：{}|".format(splitStr[0], splitStr[1])

    driver.quit()


if __name__ == '__main__':
    arg = argparse.ArgumentParser()
    arg.add_argument('--url', type=str)
    args = arg.parse_args()

    main(args.url)
