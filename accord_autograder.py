from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from axe_selenium_python import Axe

#
#
# In the future: adjust selenium waits
#


def assess_accord():

    results = "Learn ARIA - Accordion Accessibility Assessment \n \n"

    driver = webdriver.Chrome('/Users/cassandraferworn/Downloads/chromedriver')
    driver.get("https://cmvferworn.github.io/accordion.html")
    #"Establish Waiting Strategy" placeholder
    driver.implicitly_wait(0.5)

    #-------testing header-------
    
    results += "Accordion headers are keyboard focusable : "
    score = 0
    
    #select the first header
    headers = driver.find_elements(By.CSS_SELECTOR, "dt");
    header1 = headers[0]
    header1_div = header1.find_element(By.CSS_SELECTOR, "div")

    #check that it is keyboard focusable (tabindex = 0)
    header1_div_tabindex = header1_div.get_attribute("tabindex")
    
    if header1_div_tabindex == "0":
        results += "1.0 pts\n"
        score += 1
    else:
        results += "0.0 pts\n"

    results += "Accordion headers are announced as buttons instead of list items : "
    
    #check for role attribute & that it's set to "button"
    header1_div_role = header1_div.get_attribute("role")
    if header1_div_role == "button":                     
        results += "2.0 pts \n"
        score += 2
    else:
        results += "0.0 pts \n"

    #----------testing Expanding/Collapsing-----------
    
    results += "Accordion headers open panels with a click or key press : "

    #accordian opens with keypress && announces expanded vs collapsed

    text_fields = driver.find_elements(By.CSS_SELECTOR, "dd")
    text_field1 = text_fields[0]
    display = text_field1.get_attribute("style")
    aria_hidden = text_field1.get_attribute("aria-hidden")
    text_field1_is_displayed = text_field1.is_displayed()


    #This isn't...super great
    #Should definitely be tested more

    local_score = 0
    expanded_score = 0

    #confirm header collapsed. check if the text field under the first header is not visible
    if not text_field1_is_displayed and display == "display: none;" and aria_hidden:
        #check for announces collapsed
        header1_div_aria_expanded = header1_div.get_attribute("aria-expanded")
        if header1_div_aria_expanded is not True:
            expanded_score += 1

        #simlulate keypress
        header1_div.send_keys(Keys.ENTER)
        driver.implicitly_wait(10) #this should probably be turned into an explicit wait
        aria_hidden = text_field1.get_attribute("aria_hidden")
        if not aria_hidden:
            score += 1
            local_score += 1

    #check if text field is visible
    if text_field1_is_displayed and not aria_hidden:
        #check for announces expanded
        header1_div_aria_expanded = header1_div.get_attribute("aria-expanded")
        print(header1_div_aria_expanded + " second")
        if header1_div_aria_expanded:
            expanded_score += 1
        
        #simlulate keypress
        header1_div.send_keys(Keys.ENTER)
        driver.implicitly_wait(10) #this should probably be turned into an explicit wait
        aria_hidden = text_field1.get_attribute("aria_hidden")
        if aria_hidden:
            score += 1
            local_score += 1

    score += expanded_score
            
    #Print keypress score to text file
    results += str(local_score) + ".0 pts \n"

    #Print accordian anounce expanded to text file
    results += "Accordions announce expanded when a panel is opened and collapsed when closed : " + str(expanded_score) + ".0 pts \n"

    #---------testing panels focusable & arrow key navigation
    results += "Accordion panels are focusable with a Tab key press when opened : "
    panels = driver.find_elements(By.CSS_SELECTOR, "dd")
    panel = panels[0]
    panel_tabindex = panel.get_attribute("tabindex")
    if panel_tabindex  == "0":
        results += "2.0 pts\n"
        score += 2
    else:
        results += "0.0 pts\n"
    

    #---------results file and quit--------    
    results += "Total Score: " + str(score) + "/10"
    
    #create assessment results text file
    results_file = open('accord_assess.txt', 'w')
    results_file.write(results)
        
    driver.quit()
    #quitting still leaves a new instance of chrome in mac dock. An issue when running this multiple times for sure.
    


assess_accord()
