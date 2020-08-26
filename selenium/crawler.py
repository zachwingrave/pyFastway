from selenium import webdriver

PATH = r"C:\Program Files (x86)\Webdrivers\chromedriver.exe"

label = input("Enter tracking number: ")

app = webdriver.Chrome(PATH)
app.get("https://www.aramex.com.au/tools/track/")

field = app.find_element_by_id("label_number")
""" Enter label into text area """

submit = app.find_element_by_id("trace_button")
""" Click on track button """


app.quit()
