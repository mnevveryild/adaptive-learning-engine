from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
import os

load_dotenv()  # .env dosyasındaki değerleri ortam değişkeni yapar

# 1) OpenAI testi
llm = ChatOpenAI(model="gpt-4o-mini")
answer = llm.invoke("Say 'setup ok' in one short English sentence.")
print("OpenAI:", answer.content)

# 2) Tavily testi
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
result = client.search(query="present perfect tense", max_results=1)
print("Tavily:", result["results"][0]["title"])