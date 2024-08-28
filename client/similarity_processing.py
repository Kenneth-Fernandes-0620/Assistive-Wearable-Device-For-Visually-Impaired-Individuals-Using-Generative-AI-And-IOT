from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Your dictionary
prompts = {
    "Describe the environment": "Describe the environment", 
    "Explain the current scene": "Describe the environment",
    "Tell me what is happening around me": "Describe the environment",
    "What do you see?": "Describe the environment",

    "Emergency situation": "SOS",
    "I need assistance": "SOS",
    "Call for help": "SOS",
    "Send help immediately": "SOS",
    "This is an emergency": "SOS",
    "Help me now": "SOS",
    "Can you trigger an SOS?": "SOS",

    "I need help": "help",
    "I require assistance": "help",
    "Support needed": "help",
    "Help me out": "help",

    "Set up the system": "setup",
    "Initialize the setup": "setup",
    "Begin the installation process": "setup",
    "What are the setup steps?": "setup",
    "How to start setup?": "setup",

    "Is there a crowd detected?": "detect crowd",
    "Can you see a crowd?": "detect crowd",
    "Are there many people around?": "detect crowd",
    "Detect any large gathering": "detect crowd",
    "Crowd detection needed": "detect crowd",
    "Is the area crowded?": "detect crowd",
    "Do you see any group of people?": "detect crowd",

    "Terminate program": "exit",
    "Close the application": "exit",
    "Shut down the system": "exit",
    "End the process": "exit",
    "Exit now": "exit",
    "Stop everything": "exit",
    "Can we quit the program?": "exit",
}

# Convert dictionary keys to a list
keys_list = list(prompts.keys())

# Define a function to find the most similar key
def find_most_similar_command(input_text):
    # Combine input_text with keys_list for vectorization
    combined_texts = [input_text] + keys_list

    # Vectorize the texts using TF-IDF
    vectorizer = TfidfVectorizer().fit_transform(combined_texts)
    vectors = vectorizer.toarray()

    # Compute cosine similarity between the input text and all keys
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    # Find the index of the highest similarity score
    most_similar_index = cosine_similarities.argmax()

    # Return the most similar key and its corresponding value
    most_similar_key = keys_list[most_similar_index]
    return prompts[most_similar_key]


if __name__ == "__main__":
    # List of test cases to check the function
    test_inputs = [
        "Describe what you see around",
        "I need urgent help",
        "assist me?",
        "Configure the setup for me",
        "Is there a crowd of people?",
        "Shut down everything immediately",
        "shut down",
        "Explain the scene",
        'environment',
        'crowd information',
        'current scene',

    ]

    # Testing all input cases
    for input_text in test_inputs:
        similar_key, corresponding_value = find_most_similar_command(input_text, keys_list)
        print(f"Input: '{input_text}'\nMapped to: '{corresponding_value}' (Key: '{similar_key}')\n")
