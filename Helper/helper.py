import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate 
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings


load_dotenv()


import  openai
#----------------------------------------------------------------
# Getting all the screct
#----------------------------------------------------------------

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
TWILIO_ACCOUNT_SID=os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN=os.getenv('TWILIO_AUTH_TOKEN')

# openai key configuration
openai.api_key=OPENAI_API_KEY

#----------------------------------------------------------------
# generate message
#----------------------------------------------------------------
def generate_message(question) ->dict:

    """
    question as string ,

    returns dictionary formatted with response

    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
                
            ],
            temperature=1,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5
        )
        return {
                 "status":1,
                 "response":response.choices[0].message.content.strip()
                }
    
    except:
        return {
                 "status":0,
                 "response":"Something went wrong"
                }
    
#----------------------------------------------------------------
# Prompt template
#----------------------------------------------------------------
def prompt_template():
    template_format=""" 
    You are a helpful assistant.
    {context}
    {question}

    Answer
    #####
    """
    prompt = PromptTemplate(
        input_variables=["context","question"],
        template=template_format,
    )
    return prompt

#----------------------------------------------------------------
# Retrival
#----------------------------------------------------------------
def retrivalQA():
    dir_path="../vectorstores/db_faiss/"
    llm=OpenAI(api_key=OPENAI_API_KEY)
    custom_prompt=prompt_template()
    vector_db=FAISS.load_local(dir_path,OpenAIEmbeddings(api_key=OPENAI_API_KEY),allow_dangerous_deserialization=True)
    chain=RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={'k':3}),
        chain_type_kwargs={"prompt":custom_prompt},
        return_source_documents=True
    )

    return chain

#----------------------------------------------------------------
#Response
#----------------------------------------------------------------
def get_response(question):
    chain=retrivalQA()
    response=chain({'query': question})

    return {
        "status":1,
        "response":response['result']   
    }

    

# if __name__=='__main__':
#     res=get_response("who is Dr.Gali Nageswara?")
#     print(res['response'])