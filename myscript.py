
# Synchronising Wikidata and Wikipedias using pywikibot - Task 2
# Import modules
import pywikibot
from pywikibot import pagegenerators
from pywikibot.data import api
import numpy as np
import requests

def add_line(page: pywikibot.page.Page, line: str) -> int:
    """
        In: 
            page (pywikibot.page.Page): a Media Wiki page.
            line (str): the line to append at the end.
        Returns:
            status (int): status 
    """
    # get the page in text format
    text_page = page.get()
    # append the line at the end
    text_page += line 
    # save back to the page.text attribute
    page.text = text_page

    # try saving it to the original page
    try:
        page.save("Save edit")
        return 1
    except:
        print("ERROR: the edit cannot be saved")
        return 0

def load_wditem(wd_item: pywikibot.ItemPage) -> None:
    """
        In: 
            wd_item (pywikibot.ItemPage): a Wikibase entity of type 'item'.
        Returns:
            None 
    """

    # get the title
    wd_item_title = wd_item.title()
    print(f"The title of the loaded item is: {wd_item_title}")

    # the dictionary holding the information for the loaded item
    wd_item_dict = wd_item.get()

    # the label of sandbox in greek
    try:
        print("Name: " +  wd_item_dict['labels']['el'])
    except:
        print("No Greek label!")
    # check if there is a greek version available
    try:
        print("The greek version of the article: " + wd_item_dict['sitelinks']['el'])
    except:
        print("No greek version!")

    try:
        print("Iterate through available languages of the loaded item:")
        # through inspection of the data stored in the dict with keys, we have
        # dict_keys(['labels', 'descriptions', 'aliases', 'claims', 'sitelinks'])
        dict_wd = dict(wd_item_dict['labels'])
        for wd_property, wd_value_t in dict_wd.items():
            print(f"Language {wd_property}: " + " - : "  + wd_value_t)
            print()
    except:
        print("ERROR: could not parse the item")
        print()
    # The core part of a statement without references and ranks is called claim
    try:
        print("Iterate through claims:")
        dict_claims = wd_item_dict['claims']
        for claim in dict_claims.keys():
            print(f"For property {claim}")
            for property_t in dict_claims[claim]:
                p_value = property_t.getTarget()
                print("Value is: " + p_value.title())
                print()
    except:
        print("ERROR: could not parse the item")
        print()

def editwikidata(wiki_repo: pywikibot.site._datasite.DataSite, wd_item: pywikibot.ItemPage, propertyid: str, value: str) -> None:
    """
        In: 
            wiki_repo (pywikibot.site._datasite.DataSite): the wikidata repo
            wd_item (pywikibot.ItemPage): a Wikibase entity of type 'item'.
            propertyid (str): the id of the property of the property value pair, to be added.
            value (str): the value of the property of the property value pair, to be added.
        Returns:
            None
    """

    # load the item
    qid = wd_item.title()
    item_dict = wd_item.get()

    # new object ItemPage with the value to be added
    claim_target = pywikibot.ItemPage(wiki_repo, value)
    newclaim = pywikibot.Claim(wiki_repo, propertyid)
    # connect the claim to the claim target
    newclaim.setTarget(claim_target)

    print(f"The claim to be added: {newclaim}")
    text = input("Save? [y/n]: ")
    if text == 'y':
        wd_item.addClaim(newclaim, summary='Adding test claim')


def main():
    # Info
    print("Synchronising Wikidata and Wikipedias using pywikibot - Task 2")
    print("Nina Siaminou")
    print("Outreachy 2021")
    print("=======================================================")
    print("The printing of the page created for Task 1 is printed...:")

    # 2.
    # Hard wired parameters
    # Connect to enwiki
    enwiki = pywikibot.Site('en', 'wikipedia')
    # and then to wikidata
    enwiki_repo = enwiki.data_repository()
    # Connect to my page
    mypage = pywikibot.Page(enwiki_repo, 'User:Nina_Siam/Outreachy_1')

    # 3. print the content of the chosen page in a text format.
    print(mypage.text)

    # 4. Try append a line at the end of the file
    # add seperator 
    print("\n")
    seperator = "\n== Task 2 =="
    status = add_line(mypage, seperator)
    line = "\nHello from pywikibot!"
    status = add_line(mypage, line)

    # 5. Load an item from wikidata
    test_qid = 'Q4115189' # Qid for sandbox
    wd_item = pywikibot.ItemPage(enwiki_repo, test_qid)

    # Load the Sandbox item
    load_wditem(wd_item)

    test_lyre = 'Q201129' # Qid for lyre
    wd_item_lyre = pywikibot.ItemPage(enwiki_repo, test_lyre)

    # Load the Lyre item
    load_wditem(wd_item_lyre)

    # Bonus
    # test_property = 'P31' # instance of
    # test_value = 'Q5'  # Sandbox
    # editwikidata(enwiki_repo, wd_item, test_property, test_value)

    test_property2 = 'P276' # location
    test_value2 = 'Q466' # WWW
    editwikidata(enwiki_repo, wd_item, test_property2, test_value2)

if __name__ == '__main__':
    main()
