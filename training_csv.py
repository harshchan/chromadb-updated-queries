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



import csv
 
# Replace 'your_file_path.csv' with the actual path to your CSV file
file_path = 'DP_QUESS_modified.csv'
 
'''
with open(file_path, 'r',encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    headers = reader.fieldnames
    print(headers)

'''


# Open the CSV file and read its contents
with open(file_path, 'r',encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data_type = row['TRAINING_DATA_TYPE']
        question = row['QUESTIONS']
        content = row['CONTENT']
       
        if data_type.lower() == 'ddl':
            vn.train(ddl=content)
        elif data_type.lower() == 'documentation':
            vn.train(documentation=content)
        elif data_type.lower() == 'sql':
            vn.train(question=question, sql=content)
        else:
            print(f"Unknown data type: {data_type}")

