from openai import OpenAI

from app.core.settings import Settings

settings = Settings()
client = OpenAI(api_key=settings.openai_api_key.get_secret_value())

response = client.responses.create(
    model=settings.openai_model,
    instructions="You are an English teacher. Check the student's sentence for mistakes.",
    input="Yesterday I go to the market and buyed three apple.",

)

print(response.output_text)
print("-------")
print("input tokens: ", response.usage.input_tokens)
print("Output tokens: ", response.usage.output_tokens)
