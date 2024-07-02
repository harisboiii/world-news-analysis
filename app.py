import streamlit as st
import wna_googlenews as wna
import pandas as pd
from transformers import pipeline

st.set_page_config(layout="wide",page_title="News Inferno",page_icon="🌍")

st.title("Google News LLM")

# Store the initial value of widgets in session state
if "placeholder" not in st.session_state:
    st.session_state.placeholder = "Enter your search query here"

# Display the text input widget with dynamic placeholder
query = st.text_input("Search for news",
                      placeholder=st.session_state.placeholder)

models = [
          "j-hartmann/emotion-english-distilroberta-base",
          "SamLowe/roberta-base-go_emotions",
          "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
        ]

settings = {
  "langregion": "en/US",
  "period": "1d",
  "model": models[0],
  "number_of_pages": 5
}


with st.sidebar:
  st.title("Settings")
  # add language and country parameters
  # st.header("Language and Country")
  
  # settings["langregion"] = st.selectbox("Select Language", ["en/US", "fr/FR"])
  # input field for number of pages
  st.header("Number of Pages")
  settings["number_of_pages"] = st.number_input("Enter Number of Pages", min_value=1, max_value=10)

  settings["region"] = settings["langregion"].split("/")[0]
  settings["lang"] = settings["langregion"].split("/")[1]

  # add period parameter
  st.header("Period")
  settings["period"] = st.selectbox("Select Period", ["1d", "7d", "30d"])
  # Add models parameters
  st.header("Models")
  settings["model"] = st.selectbox("Select Model", models)


if st.button("Search"):
  classifier = pipeline(task="text-classification", model=settings["model"], top_k=None)
  # display a loading progress
  with st.spinner("Loading last news ..."):
    allnews = wna.get_news(settings, query)
    st.dataframe(allnews)
  with st.spinner("Processing received news ..."):
    df = pd.DataFrame(columns=["sentence", "date","best","second"])
    # loop on each sentence and call classifier
    for curnews in allnews:
      #st.write(curnews)
      cur_sentence = curnews["title"]
      cur_date = curnews["date"]
      model_outputs = classifier(cur_sentence)
      cur_result = model_outputs[0]
      #st.write(cur_result)
      # get label 1
      label = cur_result[0]['label']
      score = cur_result[0]['score']
      percentage = round(score * 100, 2)
      str1 = label + " (" + str(percentage) + ")%"
      # get label 2
      label = cur_result[1]['label']
      score = cur_result[1]['score']
      percentage = round(score * 100, 2)
      str2 = label + " (" + str(percentage) + ")%"
      # insert cur_sentence and cur_result into dataframe
      df.loc[len(df.index)] = [cur_sentence, cur_date, str1, str2]

  # write info on the output
  st.write("Number of sentences:", len(df))

  st.dataframe(df)

