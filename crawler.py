from selenium import webdriver

PATH = r"C:\Program Files (x86)\Webdrivers\chromedriver.exe"

app = webdriver.Chrome(PATH)
app.get("http://seleniumhq.org/")
