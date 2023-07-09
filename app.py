import streamlit as st
import openai
import pandas as pd
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from app_functions import get_matches_resume, show_resume


embedding_function = OpenAIEmbeddings()

resumedb = Chroma(persist_directory="chroma/full_resume/",
                    collection_name="resume_full",
                    embedding_function=embedding_function)

# openApiKey = st.secrets["OPENAI_API_KEY"]
# openai.api_key = openApiKey

st.title("Resume Rater")

show_resume = st.radio('show full resume', ['yes', 'no'])

with st.sidebar:
    # st.image(image, width=100)
    st.title('Toggle options')
    # st.write('Select the options to get the best match for your job description')
    matchtype = st.radio('Select match type', ['resume', 'skills', 'work experience'])
    top_k = st.slider('Select the number of candidates to return', 1, 20, 10)

user_input = st.text_area('Enter the description of perfect candidate for hire')
st.write('You entered: ', user_input)

matches = get_matches_resume(user_input, k=top_k, match_type=matchtype)

st.dataframe(matches[['full_name', 'distance']])

matches_name = [name for name in matches['full_name'].values]
# print(matches_name)
for i, name in enumerate(matches_name):
    resume_expander = st.expander(f"See full resume of {name}", expanded=False)
    # print(name)
    # print(type(name))
    full_resume = resumedb.get(where={"full_name": name})['documents'][0]
    resume_expander.write(full_resume)


