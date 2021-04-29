# Pywikibot_tests
Getting familiar with pywikibot api, for outreachy 2021 wikidata project 

## Task 2
In the myscript_task2.py the following tasks are implemented:
  - Log in to a Wikimedia account
  - Connect to an already existing site and print it out (the one created for Task 1).
  - Append new lines of text at the end of the page and save the changes.
  - Load a Wikidata item (Sandbox) and print parts of its content.
  - Add a new Property-Value pair to the Sandbox item.

The output is appended to the log.txt file.

## Task 3
In the myscript_task3.py the following tasks are implemented:
   - Parse a wikipedia article and print a list of statements (if available), indicated by the user.
   - Print the corresponding statements from wikidata.
   - Repeat the process for a series of articles that share the same infobox template.
   - Print the structure of the article (section headers).

## Task 5
In the myscript_task5.py the following tasks are implemented:
   - A function that makes a request to the MediaWiki API, based a given search key.
   - A function that collects the results of the previous request, prints the description of each item retrieved and returns the QID value.
# Built with
  - pywikibot
  - wikitextparser
  - myparserfromhell
