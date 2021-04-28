
# Synchronising Wikidata and Wikipedias using pywikibot - Task 5
# Nina Siaminou
# Outreachy 2021

# Import modules
import pywikibot
from pywikibot import pagegenerators
from pywikibot.data import api
import requests


def search_entities(site_repo, item_title: str) -> dict:
    """ Make a request to the MediaWiki API using the hardcoded parameters

        In:
        site_repo (site repository): the site repository.
        item_title (str): a title of an article, a term etc.

        Returns:
        data_dict (dict): the result of the request to the API, organized in a dict object.
    """
    # Hardcoded parameters
    params = { 'action' :'wbsearchentities', 
                'format' : 'json',
                'language' : 'en',
                'type' : 'item',
                'search': item_title}
    try:
        request = api.Request(site=site_repo, parameters=params)
        data_dict = request.submit()
        return data_dict
    except:
        print("ERROR: could not make request to MediaWiki API")
        return

def choose_item(site_repo, data_dict: dict) -> None:
    """ Print the description of the itemsretrived from the request to the API

        In:
        data_dict (dict): dictionary that contains the data retrieved.

    """
    if data_dict:
        number_of_items_found = len(data_dict['search'])
        items_found = data_dict['search']
        search_key = data_dict['searchinfo']['search'].strip()
        print(f"Item(s) correspond for the search key: {search_key}")
        print('*' * 60)
        item_n = 1
        for item in items_found:
            try:
                if item['description'] != "Wikimedia disambiguation page":
                    print(f"{item_n}: {item['label']}, {item['description']}")
                    item_n += 1
                else:
                    print("disambiguation page")
                    item_n += 1
                    continue
            except:
                print(f"{item_n}: {item['label']}, description is not available, iterate through claims to get more information: ")
                test_qid = item['id'].strip()                                                                               # Qid for item without description
                item_page = pywikibot.ItemPage(site_repo, test_qid)
                wd_item_dict = item_page.get()
                dict_claims = wd_item_dict['claims']
                for claim in dict_claims.keys():
                    for property_t in dict_claims[claim]:
                        p_value = property_t.getTarget()
                        print(f"Property: {claim} -> Value is:  {p_value}")
                item_n += 1 
        
        while True:
            selection = input("Select one of the above (using the number) to get the QID value: ").strip()
            try:
                selection = int(selection)
                selection = selection - 1
                qid = items_found[selection]['id']
                print(f"The selected QID: {qid}")
                break
            except:
                print("ERROR: give a valid input (int) according the list above")

def main():
    
    site = pywikibot.Site("en", "wikipedia")                                                                                 # Connect to enwiki
    site_repo = site.data_repository()
    # Check for an article names
    article = "Scala"

    data_dict = search_entities(site_repo, article)
    choose_item(site_repo, data_dict)

if __name__ == '__main__':
    main()