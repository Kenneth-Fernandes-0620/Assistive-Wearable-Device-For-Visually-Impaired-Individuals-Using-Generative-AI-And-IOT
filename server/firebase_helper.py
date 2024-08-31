import os
from firebase_admin import credentials, firestore, initialize_app, messaging


def load_firebase_credentials():
    # Load the Firebase Admin SDK credentials from the environment variable
    firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")

    # Initialize the Firebase Admin SDK using the parsed credentials
    cred = credentials.Certificate(firebase_credentials_path)
    initialize_app(cred)

def send_message_to_topic(topic, title, body, uid = 'Byi1c2jSuMXSsH958F1ch3TbnLD3'):

    # Define the message payload
    message = messaging.Message(
        data={
            'uid':uid
        },
        topic=topic
    )

    try:
        # Send the message
        response = messaging.send(message)
        print(f'Successfully sent message to topic "{topic}": {response}')
    except Exception as e:
        print(f'Error sending message: {e}')



load_firebase_credentials()

# Initialize Firestore
db = firestore.client()

# Function to send a document to Firestore
def send_document_to_firestore(collection_name, data):
    doc_ref = db.collection(collection_name)
    _, document_id = doc_ref.add(data)
    print(f"Document {document_id} written to collection {collection_name}.")

if __name__ == "__main__":
    # Example usage
    collection_name = "test_collection"
    data = {
        "test_field_1": "test_value_1",
        "test_field_2": "test_value_2",
        "test_field_3": "test_value_3",
    }
    send_document_to_firestore(collection_name, data)