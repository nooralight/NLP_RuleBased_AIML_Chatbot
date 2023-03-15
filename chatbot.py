import aiml
import nlp_class

# Create a Kernel object. No string encoding (all I/O is unicode)
kern = aiml.Kernel()
kern.setTextEncoding(None)
#kern.setTextEncoding(None)

# Use the Kernel's bootstrap() method to initialize the Kernel. The
# optional learnFiles argument is a file (or list of files) to load.
# The optional commands argument is a command (or list of commands)
# to run after the files are loaded.
# The optional brainFile argument specifies a brain file to load.
kern.learn("/data.aiml")

# Define a rule-based algorithm to handle a specific user input
def handle_user_input(user_input):
    # Check if the user is asking for the weather
    response = nlp_class.chatbot(user_input)
    return response

# Define an NLP algorithm to handle a specific user input
# def handle_nlp(user_input):
#     # Use a pre-trained model to identify the user's intent
#     # In this example, we'll use a simple rule to determine the intent
#     if 'movie' in user_input.lower():
#         # If the user is asking about a movie, return the name of the movie
#         return 'The movie you are asking about is Jaws.'
#     # If the user's intent cannot be determined, return None
#     return None

# Welcome the user
print("Welcome to this chat bot. Please feel free to ask questions from me!")

# Main loop
while True:
    # Get user input
    try:
        user_input = input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print("Bye!")
        break
    ans = handle_user_input(user_input)
    print(ans)
    if "I am sorry!" in ans:
        answer = kern.respond(user_input)
        print(answer)
