import os
from firebase_admin import credentials, firestore, initialize_app


def load_firebase_credentials():
    # Load the Firebase Admin SDK credentials from the environment variable
    firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")

    # Initialize the Firebase Admin SDK using the parsed credentials
    cred = credentials.Certificate(firebase_credentials_path)
    initialize_app(cred)


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