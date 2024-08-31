from pymongo import MongoClient

# MongoDB connection


client = MongoClient('mongodb://localhost:27017/')
db = client['vehicle_rental']
labour_collection = db['labour_data']  # Replace with your collection name

# Sample document that should match the query
sample_labour = {
    'is_active': 5,
    'labour_id' :"ZSK284",
    'state': 'Karnataka',
    'city': 'Banashankari',
    'professionalType': 'Driver',
    'status_dates': [
        {
            'date': '2024-08-20',
            'status': 5
        },
        {
            'date': '2024-08-22',
            'status': 5
        }
    ],
    'name': 'John Doe',
    'age': 30
}

# Insert the document into the collection
labour_collection.insert_one(sample_labour)
print("Sample labour data inserted successfully.")
