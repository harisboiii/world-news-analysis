
# https://github.com/Iceloof/GoogleNews
from GoogleNews import GoogleNews
import pandas as pd

# get the news with lang and country parameters
def get_news(settings, query):
  googlenews = GoogleNews(
    lang=settings["lang"], 
    region=settings["region"],
    period=settings["period"],
  )
  number_of_pages = settings["number_of_pages"]
  # get each pages
  final_list = []
  googlenews.search(query)
  print("Total Pages: ", googlenews.total_count())
  for page in range(1, number_of_pages + 1):
      page_result = googlenews.page_at(page)
      # merge dat
      final_list = final_list + page_result
  return final_list