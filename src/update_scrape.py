from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.set_headless()
assert opts.headless  # Operating in headless mode


chrome_driver = '/home/chris/Downloads/chromedriver'
browser = Firefox(options=opts)
browser.get('https://www.ncsl.org/research/energy/energy-legislation-tracking-database.aspx')



search_form = browser.find_element_by_name("dnn$ctr85406$StateNetDB$btnSearch")
search_form.submit()

#<input type="submit" name="dnn$ctr85406$StateNetDB$btnSearch" value="Search" onclick="javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions(&quot;dnn$ctr85406$StateNetDB$btnSearch&quot;, &quot;&quot;, true, &quot;&quot;, &quot;&quot;, false, false))" id="dnn_ctr85406_StateNetDB_btnSearch" style="width:75px;">