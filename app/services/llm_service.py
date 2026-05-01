from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from app.config import config


class LLMService:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
            openai_api_key=config.OPENAI_API_KEY
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.chain = ConversationalRetrievalChain(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(),
            memory=self.memory
        )

    def ger_response(self, query):
       try:
        response = self.chain({"question": query})
        return response["answer"]
       
       except Exception as e:
          print (f"Error getting LLM Response:{e}")
          return "I encountered an error processing your request."

  