# Chat with Marcus Aurelius
This bot has a simple system prompt and does a basic similarity search on Meditations, the famous book by Stoic Roman Emperor Marcus Aurelius.

# Run Commands
1. in Terminal: source env/bin/activate
2. in Terminal: pip install -r requirements.txt
3. in Terminal: export OPENAI_API_KEY=="YOUR_API_KEY"
4. in Terminal: python3 visit_the_palace.py
5. chat with Marcus Aurelius, greatest emperor of Rome

# Logical Flow
1. Get user inbound message
2. Append to message history
3. Perform similarity search on inbound message to get examples
4. Append examples to system prompt
5. Generate outbound message
6. Append outbound message to message history
7. Send to user
