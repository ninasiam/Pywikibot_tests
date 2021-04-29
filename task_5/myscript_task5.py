
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
    """ Print the description of the itemsretrived from the request to the API.
        Requires user interaction.
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
                print(item)
                if item['description'] != "Wikimedia disambiguation page":
                    print(f"{item_n}: {item['label']}, {item['description']}")
                    item_n += 1
                else:
                    print("disambiguation page")
                    item_n += 1
                    continue
            except:
                print(f"{item_n}: {item['label']}, description is not available, iterate through claims to get more information: ")
                test_qid = item['id'].strip()                                                                               
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

def check_for_claim(site_repo, item, search_param: list) -> bool:
    """ Check if an item has the given claim

        In:
        site_repo (site repository): the site repository.
        item (wikidata item):  retrieved from the request.
        search_param (list): a search parameter list to further clarify the request.

        Returns:
        status bool

    """

    test_qid = item['id'].strip()                                                                              
    item_page = pywikibot.ItemPage(site_repo, test_qid)
    wd_item_dict = item_page.get()
    dict_claims = wd_item_dict['claims']
    for claim in dict_claims.keys():
        if claim.strip() in search_param:
            print(f"The selected QID: {test_qid}")
            return True


def search_entities_categories(article: str) -> dict:
    """ Make a request to the MediaWiki API using the hardcoded parameters

        In:
        site_repo (site repository): the site repository.
        item_title (str): a title of an article, a term etc.

        Returns:
        data_dict (dict): the result of the request to the API, organized in a dict object.
    """
    # Hardcoded parameters
    try:
        session = requests.Session()

        url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "format": "json",
            "prop": "categories",
            "titles": article        
            }

        request = session.get(url=url, params=params)
        data_dict = request.json()
        return data_dict
    except:
        print("ERROR: could not make request to MediaWiki API")
        return


def choose_item_without_prompt(site_repo, data_dict: dict, search_param: list) -> None:
    """ Print the description of the itemsretrived from the request to the API

        In:
        data_dict (dict): dictionary that contains the data retrieved.
        search_param (list): a search parameter list to further clarify the request.


    """
    if data_dict:
        number_of_items_found = len(data_dict['search'])
        items_found = data_dict['search']
        search_key = data_dict['searchinfo']['search'].strip()
        print(f"Item: {search_key}, with given parameter: {search_param}")
        print('*' * 60)
        for item in items_found:
            # print(item)
            try:
                if item['description'] != "Wikimedia disambiguation page":
                    item_description = item['description'].lower().strip()
                    if search_param[0].lower() in item_description:
                        qid = item['id']
                        print(f"Item description: {item['description']}")
                        print(f"The selected QID: {qid}")
                        break
                    else:
                        if check_for_claim(site_repo, item, search_param):
                            return
                        
                else:
                    print("disambiguation page")
                    continue
            except:
                    if check_for_claim(site_repo, item, search_param):
                        return
def main():
    
    site = pywikibot.Site("en", "wikipedia")                                                                                 # Connect to enwiki
    site_repo = site.data_repository()
    # Check for an article names
    article = "Berlin"
    search_params  = ['P1376']
    data_dict = search_entities(site_repo, article)
    choose_item_without_prompt(site_repo, data_dict, search_params)


def main2():
    site = pywikibot.Site("en", "wikipedia")                                                                                 
    site_repo = site.data_repository()
    # Check for an article names
    article = "France"

    data_dict = search_entities_categories(article)
    
    found_items = data_dict["query"]["pages"]
    print(found_items)
    for k, v in found_items.items():
        for cat in v['categories']:
            print(cat["title"])

if __name__ == '__main__':
    main()
    # main2()
