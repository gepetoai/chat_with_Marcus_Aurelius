from ai import initialize_vdb, find_examples, generate_response


#########SIMPLE IMPLEMENTATION#########
#First, we initialize the vector database
db = initialize_vdb()


#Short system prompt
prompt = "You are Marcus Aurelius, Emperor of Rome. You are speaking to a common boy who is curious about Mediations. Below are excerpts from Meditations for you to respond from. If the answer is not in the following text, respond with I do not know (but as Marcus would say it) Make sure you keep your messages short, max 3 sentences:\n\n"

#Initialize first Assistant Message
outbound = "Good day young one. How may I be of aid?"

#Initialize first inbound message
inbound = ""

#Initialize Messages table
messages = []

while inbound != "Exit":
    print("###################################################")
    inbound = input("Marcus: " + outbound+ "\nYou: ")
    
    if input == "Exit":
        break
    
    #append user input to messages
    messages.append({"role": "user", "content": inbound})

    #do similarity search and get examples
    examples = find_examples(db, inbound)

    #format custom system prompt
    custom_prompt = prompt + examples
    custom_prompt = {"role": "system", "content": custom_prompt}

    #format messages for response generation
    llm_messages = [custom_prompt] + messages

    #generate response
    response = generate_response(llm_messages, "gpt-4-1106-preview")
    outbound = response.choices[0].message.content

    if outbound:
        messages.append({"role": "assistant", "content": outbound})

    else:
        print("My apologies, the battlefield calls. Until we meet again. Glory to Rome!")
        break

