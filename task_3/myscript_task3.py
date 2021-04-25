
# Synchronising Wikidata and Wikipedias using pywikibot - Task 3
# Nina Siaminou
# Outreachy 2021

# Import modules
import pywikibot
from pywikibot import pagegenerators
from pywikibot.data import api
import numpy as np
import wikitextparser as wtp                                                                                                  # use of the wikitextparser
import mwparserfromhell as mps                                                                                                # use of the myparserofhell
import re
import copy

# https://www.mediawiki.org/wiki/Alternative_parsers
# https://wikitextparser.readthedocs.io/en/latest/README.html#templates
def parse_wiki_infobox_wtp(site, wiki_page: str, list_of_properties: dict) -> None:
    """ Loads a wikipedia article and prints the available parameters from the 
        infobox.

        In: 
        site (pywikibot.Site): the host site (e.g Wikipedia 'en')
        wiki_page (str): The title of the article (e.g Douglas Adams).
        list_of_parameters (dict): List of parameters that correspond to the wikipage infobox.

        Note: a parser tool is required (wikitextparser).
    """
    # Try load the page
    try:
        page = pywikibot.Page(site, wiki_page)
        item = pywikibot.ItemPage.fromPage(page)     

        page_title = page.title()     
        item_qid = item.title()                                          
        print(f"The title of the loaded item is: {page_title} with Q-label: {item_qid}")                                     # item title

        dict_item = item.get()                                                                                               # Get the item dictionary
        text = page.text

    except:
        print("ERROR: could not find the wiki item")
        return
    list_of_properties_tmp = copy.deepcopy(list_of_properties)
    parsed = wtp.parse(text)
    templates = parsed.templates
    found_infobox = False
    # Parse the parsed object and look for templates
    try:   
        for template in templates:
            if "Infobox" in template.name:   
                # there is a list of infoboxes available           
                print(f"Template name: {template.name}")
                for arg in template.arguments:
                    # extract the values that correspond to the given template parameters.
                    if arg.name.strip() in list_of_properties.keys():
                        print(f"For template arg name: {arg.name} -> {list_of_properties[arg.name.strip()]}: {arg.value}")
                        del list_of_properties_tmp[arg.name.strip()]                                                        # Remove the found item from the list
                found_infobox = True
        if list_of_properties_tmp:                                                                                          # Since it exists, some properties were not found
            print(f"No information found for: {list(list_of_properties_tmp.keys())}")
        if not found_infobox:
            print("Infobox is not available")   
    except:
        print("ERROR: could not parse the templates of the wiki item")
        return

# https://github.com/earwig/mwparserfromhell/
def parse_wiki_infobox_mps(site, wiki_page: str, list_of_properties: dict) -> None:
    """ Loads a wikipedia article and prints the available parameters from the 
        infobox.

        In: 
        site (pywikibot.Site): the host site (e.g Wikipedia 'en')
        wiki_page (str): The title of the article (e.g Douglas Adams).
        list_of_parameters (dict): List of parameters that correspond to the wikipage infobox.

        Note: a parser tool is required (my parser from hell).
    """
    # Try load the page
    try:
        page = pywikibot.Page(site, wiki_page)
        item = pywikibot.ItemPage.fromPage(page)     

        page_title = page.title()     
        item_qid = item.title()                                          
        print(f"The title of the loaded item is: {page_title} with Q-label: {item_qid}")                                     # item title

        dict_item = item.get()                                                                                               # Get the item dictionary
        text = page.text

    except:
        print("ERROR: could not find the wiki item")
        return
    list_of_properties_tmp = copy.deepcopy(list_of_properties)
    parsed = mps.parse(text)
    templates = parsed.filter_templates()
    infobox_flag = False
    # Parse the parsed object and look for templates
    try:   
        for template in templates:
            if template.name.matches("Infobox Instrument"):   
                # there is a list of infoboxes available           
                print(f"Template name: {template.name}")
                infobox = template
                available_names = [infobox_name.name.strip() for infobox_name in infobox.params]                             # available parameters for the infobox
                infobox_flag = True
                break
        if not infobox_flag:
            print("Infobox is not available") 
    except:
        print("ERROR: could not parse the templates of the wiki item") 
        return
    # extract the values that correspond to the given template parameters.
    try:
        for par in list_of_properties.keys():
            if par in available_names:
                val = str(infobox.get(par).value).strip()
                if val: # regex for escape characters 
                    print(f"For template arg: {par} -> {list_of_properties[par]} = {val}")         
                else:
                    print(f"No info found for arg: {par}")
            else:
                print(f"{par} not available in the infobox") 
    except:
        print("ERROR: could not parse the infobox of the wiki item")
        return

# https://www.wikidata.org/wiki/Wikidata:Pywikibot_-_Python_3_Tutorial/Data_Harvest
def print_claims(site, wiki_page: str, list_of_properties: dict) -> None: 
    """ Loads a a wikipedia article, and prints the statements from Wikidata
        indicated be the list_of_properties argument

        In: 
        site (pywikibot.Site): the host site (e.g Wikipedia 'en')
        wiki_page (str): The title of the article (e.g Douglas Adams).
        list_of_parameters (dict): List of parameters that correspond to the wikipage infobox.

    """
    # Try load the page
    try:
        page = pywikibot.Page(site, wiki_page)
        item = pywikibot.ItemPage.fromPage(page)        
        dict_item  = item.get()

    except:
        print("ERROR: could not find the wiki item")
        return
    # Iterate the claims dictionary, and find the properties indicated by list_of_properties
    # if they exist
    try:
        print("\nIterate through available statements:")
        dict_claims = dict_item['claims']
        for claim in dict_claims.keys():
            if claim in list_of_properties.values():
                prp_v = [prp_t.getTarget().title() for prp_t in dict_claims[claim]]
                print(f"For property: {claim} = {prp_v}")
    except:
        print("ERROR: could not parse the item")
        return

def print_structure(site, wiki_page: str) -> None:
    """ Print the structure of the given article wiki_page

        In:
        site (pywikibot.Site): the host site (e.g Wikipedia 'en').
        wiki_page (str): The title of the article (e.g Douglas Adams).

    """
    # Try load the page
    try:
        page = pywikibot.Page(site, wiki_page)
        text = page.text

    except:
        print("ERROR: could not find the wiki item")
        return
    # print the section headers
    parsed = wtp.parse(text)
    sections = parsed.sections
    sections_titles = [section_title.title for section_title in sections]
    print("The structure of the article {page.title()} is (section headers): ")
    print(sections_titles)

def main():
    
    site = pywikibot.Site("en", "wikipedia")                                                                                 # Connect to enwiki
    list_of_properties = {'hornbostel_sachs': 'P1762', 'name': 'P2561',
                          'image': 'P18', 'inventors': 'P61', 'related': 'P7084', 'range': 'P2343'}                          # dict with properties 
    
    # For one article at first
    article = "Piano"

    parse_wiki_infobox_mps(site, article, list_of_properties)                                                                # parse the article
    print_claims(site, article, list_of_properties)                                                                          # print the corresponding statements from wikidata
    print("*" * 40)
    # Now Check for more articles
    articles = ["Lyre", "Electric guitar",  "Violin", "Flute"]

    for article in articles:
        parse_wiki_infobox_mps(site, article, list_of_properties) 
        print_claims(site, article, list_of_properties)
        print("*" * 40)

    # Print the structure of each article
    print_structure(site, article)

if __name__ == '__main__':
    main()