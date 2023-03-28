import openai
openai.api_key = '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'
model_engine = 'gpt-3.5-turbo'
def generate_response(prompt):
    prompt.lower()
    if len(prompt) == 0:
        return "What can i help you with?"
    model_engine = "text-davinci-003"
    prompt = (f"{prompt}")

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt + "reply in a way that a kid will understand and like",
        max_tokens=1024,
        n=2,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message.strip()

#while True:
    #prompt = input("Enter your question: ")
    #response = generate_response(prompt)
    #print(list(response))

    #print(response)
