import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 确保目标文件夹存在
output_folder = 'C:\\txt'
os.makedirs(output_folder, exist_ok=True)

# 如果你已经将 msedgedriver 的路径添加到了环境变量中，可以尝试不指定路径
service = Service()

# 创建 Edge 浏览器实例
options = webdriver.EdgeOptions()
options.use_chromium = True  # 使用 Chromium 内核的 Edge
# options.headless = True  # 如果不需要打开浏览器窗口，可以加上这行
driver = webdriver.Edge(service=service, options=options)

# 读取 web.txt 文件中的 URL
with open('web.txt', 'r', encoding='utf-8') as file:
    urls = file.readlines()

try:
    for url in urls:
        url = url.strip()  # 去掉行末的换行符和空格
        if not url:  # 跳过空行
            continue

        try:
            print(f"Navigating to URL: {url}")
            driver.get(url)
            
            # 等待页面加载完成
            timeout = 10
            try:
                print("Waiting for page to load...")
                WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
                print("Page loaded.")
            except TimeoutException:
                print("Timed out waiting for page to load")
            
            # 获取所有的可见元素
            print("Fetching visible elements...")
            elements = driver.find_elements(By.XPATH, '//body//*[not(self::style or self::script or self::noscript)]')
            
            # 打印每个元素的信息
            print("Printing element information...")
            filename = f"{url.replace('://', '_').replace('/', '_')}.txt"
            filepath = os.path.join(output_folder, filename)
            with open(filepath, 'w', encoding='utf-8') as file:
                for element in elements:
                    file.write(f"Tag: {element.tag_name}, Text: {element.text}\n")
            print(f"Element information saved to {filepath}")
        except Exception as e:
            print(f"Error processing URL: {url}. Error: {e}")
finally:
    print("Closing browser...")
    driver.quit()