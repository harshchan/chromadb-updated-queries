from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore
from vanna.groqq import Groq

class MyVanna(ChromaDB_VectorStore, Groq):
    def __init__(self, config=None):
        if config is None:
            config = {}

        ChromaDB_VectorStore.__init__(self, config={"path": "./chroma_models/Demand_Planning1"})
        api_key=config.get("api_key","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")
        model=config.get("model","llama-3.1-70b-versatile")

        Groq.__init__(self,
                      config={"api_key":api_key,"model":model,"temperature":0.1,"top_k":50}
                      
                     )
        #Groq.__init__(self, config=config)
 
vn = MyVanna()


import streamlit as st



# Streamlit UI
st.title("Question to SQL Generator")

# Input field for user's question
question = st.text_input("Enter your question")

# Generate SQL button
if st.button("Generate SQL"):
    if question:
        sql_query = vn.generate_sql(question=question)    #generate_sql(question)
        st.code(sql_query, language='sql')

        # Adding the Copy to Clipboard button
        st.text_area("Copy the SQL query", value=sql_query, height=100)
        st.write("Press Ctrl+C / Cmd+C to copy the query after selecting it.")

        #st.write(f"Generated SQL Query: `{sql_query}`")
    else:
        st.error("Please enter a question.")
