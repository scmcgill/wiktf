import re
import sys
import requests
from bs4 import BeautifulSoup
from optparse import OptionParser
#parser = OptionParser()
#parser.add_option("-fr", "--french", 
def get_search_term():
    search_term = ""
    for el in range(len(sys.argv) - 1):
        # add underscores
        search_term += (sys.argv[el + 1] + "_")
        # delete trailing underscore and return URL
    return search_term[:-1]
URL = "https://en.wiktionary.org/wiki/" + get_search_term()
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
# add underscores to string arguments to complete URL

def get_def(language_name):
    # check for definition of search term
    ## not working?
    lang_span = soup.find("span", id=language_name)
    if lang_span:
        print("\n# " + language_name + ":")
        for element in lang_span.next_elements:
            if element.name == "ol": 
                print("-- " + element.findNext("li").findNext("a").text + "\n")
                if element.findChildren("dl"):
                    for el in element.find_all(class_ = re.compile(r".*-quotation")):
                        print("\t" + str(el.text))
                    #print(element.find("dl").text)
            # break at styling element that indicates end of section
            if element.name == "hr":
                break
# figure out how to use language code as argument to be able to search all available languages
languages = ["French", "German", "Arabic", "Persian", "Spanish", "Esperanto"]
if page:
    search_term = "" 
    for el in range(0,len(sys.argv) - 1):
        # add spaces
        search_term += (sys.argv[el + 1] + " ")
    print("--- " + search_term + " ---")
    for lang in languages:
        get_def(lang)
else:
    print("Something went wrong :(\nMaybe a page does not exist for this term.")
