from pymongo import MongoClient

# Connect to MongoDB (replace with your connection string if necessary)
client = MongoClient('mongodb://localhost:27017/')

# Access the rental database and city_data collection
db = client['vehicle_rental']
collection = db['placename_data']

# Arrays to be inserted
states = ["Karnataka", "Tamil Nadu", "Telangana", "Andhra Pradesh", "Kerala", "Maharashtra", "Goa"]
professional = ["Driver", "Mechanic", "Electrician", "Painter", "Construction Helpers", "Domestic Helpers", "Gardening", "Factory Helpers"]

# Document structure
data = {
    "states": states,
    "professional": professional
}

# Insert data into the collection
collection.insert_one(data)

print("Data inserted successfully!")
