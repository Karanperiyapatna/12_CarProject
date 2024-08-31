from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_cors import CORS

from flask import Flask, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
import datetime
from pymongo import MongoClient

import uuid
import random
import string


app = Flask(__name__, static_folder="static", template_folder="templates")

# File upload setup
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['vehicle_rental']
labour_collection = db['labour_data']
booking_collection = db['booking_data']
booked_details_collection = db['booked_details_collection']

customer_collection = db['user_data']
agent_collection = db['agent_data']
cb_collection = db['cb_data']
placename_collection = db['placename_data']

enquiry_collection = db['enquiry_data']

customer_collection = db['customer_feedback']



app = Flask(__name__)
# CORS(app)
CORS(app, supports_credentials=True) 

# Mock database
users = {}
labours = []

# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
	os.makedirs(UPLOAD_FOLDER)
	
app.secret_key = '123456789' 


@app.route('/contact_us', methods=['POST'])
def contact_us():
	data = request.get_json()
	name = data.get('name')
	mobile = data.get('mobile')
	email = data.get('email')
	message = data.get('message')

	# Inserting data into MongoDB
	contact_data = {
		'name': name,
		'mobile': mobile,
		'email': email,
		'message': message,
		'update': False
	}
	enquiry_collection.insert_one(contact_data)

	print(f"Received message from {name} (Mobile: {mobile}, Email: {email}): {message}")
	return jsonify({'message': 'Thank you for contacting us!'}), 200



# ===================================== Feedback Data Code =========================================


@app.route('/get_feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = list(customer_collection.find({}, {'_id': 0}))  # Fetch all feedbacks, excluding the `_id`
    return jsonify({'feedbacks': feedbacks})


#  ===================================== SEARCH OPTION =============================================

@app.route('/api/getOptions', methods=['GET'])
def get_options():
	# Fetch distinct options from your database
	states = labour_collection.distinct("state")
	cities = labour_collection.distinct("city")
	worker_types = labour_collection.distinct("worker_type")
	return jsonify({"states": states, "cities": cities, "worker_types": worker_types})

@app.route('/api/workers', methods=['POST'])
def search_workers():
	state = request.json.get('state')
	city = request.json.get('city')
	worker_type = request.json.get('worker_type')
	booking_date = request.json.get('booking_date')

	workers = labour_collection.find({
		"state": state,
		"city": city,
		"professional": worker_type,
		"status_dates": {"$elemMatch": {"$eq": booking_date}},
		"is_active": True
	})

	worker_list = [{"labour_id": worker["labour_id"],
					"labour_name": worker["labour_name"],
					"professional": worker["worker_type"],
					"state": worker["state"],
					"city": worker["city"]}
				   for worker in workers]
	return jsonify({"workers": worker_list})


# ======================================== USER CODE =============================================

def user_id_generate():
	print("generating the labour unique ID")

	# labour_id = random.randint(1000, 9999) # 4 digit unique ID generation
	user_id = random.randint(10000, 99999) # 4 digit unique ID generation
	return user_id



#=============================================== USER CODE ==========================================


@app.route('/UserSignup', methods=['POST', 'GET'])
def UserSignup():
	if request.method == 'POST':
		data = request.form

		# Extract form data
		name = data.get('name')
		mobile_number = data.get('mobile_number')
		alt_mobile_number = data.get('alt_mobile_number')
		email = data.get('email')
		address = data.get('address')
		city = data.get('city')
		state = data.get('state')
		pincode = data.get('pincode')
		username = data.get('username')
		password = data.get('password')

		# Handle file upload
		if 'address_proof' not in request.files:
			return jsonify({'message': 'No file part'}), 400
		
		file = request.files['address_proof']
		if file.filename == '':
			return jsonify({'message': 'No selected file'}), 400
		
		if file:
			filename = secure_filename(file.filename)
			unique_id = str(uuid.uuid4())
			unique_filename = f"{unique_id}_{filename}"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))


		cdt = datetime.datetime.now()
		user_id = user_id_generate()
		user_reg_cdt = datetime.datetime.strftime(cdt, '%y-%m-%d %H:%M:%S')


		# Current Date and Time

		user_reg_cd = cdt.strftime('%y-%m-%d')

		hashed_password = generate_password_hash(password)

		# Create a dictionary to store in MongoDB
		user_data = {
			'user_id': user_id,
			'user_registration_date': user_reg_cd,
			'user_registration_datetime': user_reg_cdt,
			'name': name,
			'mobile_number': mobile_number,
			'alternative_mobile_number': alt_mobile_number,
			'email': email,
			'address': address,
			'city': city,
			'state': state,
			'pincode': pincode,
			'address_proof': unique_filename,
			'username': username,
			'password': hashed_password,
			'original_password': password ,
		}
		print("user singup data is:", user_data )

		# Insert data into the collection
		result = customer_collection.insert_one(user_data)
		if result.acknowledged:
			return jsonify({'message': 'Signup successful!'}), 201
		else:
			return jsonify({'message': 'Signup failed!', 'name': name, 'user_id': user_id}), 500

		# return jsonify({'message': 'Signup successful!'}), 201
	

@app.route('/UserLogin', methods=['POST'])
def UserLogin():
	data = request.json
	print("data from the login link :", data)
	username = data.get('username')
	password = data.get('password')

	if data is None:
		return jsonify({"error": "Invalid JSON"}), 400

	existing_user = customer_collection.find_one({
			'username': username
		})
	print("userlogin existing data is :", existing_user)
	if existing_user:
			print(type(existing_user['user_id']))
			print(type(existing_user['user_id']))
			session['username'] = existing_user['user_id']
			return jsonify({'message': 'Login successful!', 'user_id': existing_user['user_id'], 'name': existing_user['username']}), 200
	else:
		# Return failure response
		return jsonify({'message': 'Invalid username or password'}), 401



# Dashboard route (for example purposes)
@app.route('/UserDashboard')
def UserDashboard():
	if 'user_id' in session:
		return jsonify({'message': f"Welcome {session['username']}"})
	else:
		return redirect(url_for('login'))
	

@app.route('/get_location_data', methods=['GET'])
def get_location_data():
	data = placename_collection.find({})
	
	states = set()
	cities = set()
	professionals = set()



	for item in data:
		state_list = item.get('states', [])
		if isinstance(state_list, list):
			states.update(state_list)
		else:
			states.add(state_list)

		city_list = item.get('city', [])
		if isinstance(city_list, list):
			cities.update(city_list)
		else:
			cities.add(city_list)

		professional_list = item.get('professional', [])
		if isinstance(professional_list, list):
			professionals.update(professional_list)
		else:
			professionals.add(professional_list)

	# or 
	'''
		states = list(mongo.db.states.find({}, {'_id': 0, 'state': 1}))
		cities = list(mongo.db.cities.find({}, {'_id': 0, 'city': 1}))
		professionals = list(mongo.db.professionals.find({}, {'_id': 0, 'type': 1}))

		states = [state['state'] for state in states]
		cities = [city['city'] for city in cities]
		professionals = [prof['type'] for prof in professionals]
	'''

	return jsonify({
		'states': list(states),
		'cities': list(cities),
		'professionals': list(professionals)
	})

from datetime import datetime


@app.route('/search_labours', methods=['POST'])
def search_labours():
	try:
		# Get the request data from frontend
		data = request.json
		print("data from search_labour : ", data)
		state = data.get('state')
		city = data.get('city')
		search_date = data.get('date')
		professional_type = data.get('professionalType')

		print("search_date is :", search_date)
		# Convert search_date to datetime object for comparison
		search_date_obj = datetime.strptime(search_date, '%Y-%m-%d')

		# Query to fetch labours based on criteria
		query = {
			'is_active': 5,
			'state': state,
			'city': city,
			'professional': professional_type,
			'status_dates.date': search_date,  # Access directly to check if this works
			'status_dates.status': 5
		}

		print(" query for search_labour", query)
		# Execute the query
		labours = list(labour_collection.find(query, {'_id': 0}))  # Exclude the _id field
		if labours:
			print("labour found successfully")
			# print("Labours found:", labours)
		else:
			print("No labours found.")

		# Return the result to frontend
		print("sending the search_labours data :",labours )
		return jsonify({'labours': labours})

	except Exception as e:
		print(f"An error occurred: {e}")
		return jsonify({'error': 'Failed to fetch labours!'}), 500


# Logout route
@app.route('/logout', methods=['POST'])
def logout():
	session.clear()  # Clears the session
	return jsonify({'message': 'Logout successful!'}), 200



def order_id_generate():
	print("generating the order id")
	order_id = str(uuid.uuid4().hex)[:16].lower()
	return order_id


@app.route('/send_request', methods=['POST'])
def send_request():
	data = request.get_json()

	print("send_request data :", data)  # Print received data for debugging
	
	user_id = data.get('user_id')
	username = data.get('username')
	request_date = data.get('request_date')

	labour_details = data.get('labour', {})
	labour_id = labour_details.get('labour_id')
	labour_name = labour_details.get('labour_name')

	
	# Check if all required fields are present
	if not user_id or not username or not request_date:
		return jsonify({'message': 'Missing required fields'}), 400

	# Fetch labour_id using username
	labour = labour_collection.find_one({'labour_id': labour_id})
	if not labour:
		return jsonify({'message': 'Labour not found'}), 404
	
	labour_id = labour.get('labour_id')
	labour_name = labour.get('labour_name')
	print("labour_id in send_request :", labour_id)
	print("labour_id in send_request :", labour_name)
	if not labour_id:
		return jsonify({'message': 'Labour ID not found'}), 404
	
	order_id = order_id_generate()
	
	request_entry = {
		'order_id' : order_id,
		'user_id': user_id,
		'user_name':username,
		'labour_id' : labour_id,
		'labour_name': labour_name,
		'working_date': request_date,
		'status': 6
	}
	print("data for request_entry is :", request_entry)
	booking_collection.insert_one(request_entry)
	
	return jsonify({'message': 'Request sent successfully'}), 200


@app.route('/get_requests', methods=['GET'])
def get_requests():
	labour_id = request.args.get('labour_id')
	
	if not labour_id:
		return jsonify({'message': 'Labour ID is required'}), 400
	
	pending_requests = list(booking_collection.find({'labour_id': labour_id, 'status': 6}))  # Assuming 6 means 'pending'

	requests = []
	for req in pending_requests:
		requests.append({
			'user_id': req.get('user_id', 'Unknown'),  # Provide a default value for user_id
			'request_date': req.get('request_date', 'No date available')  # Handle missing 'request_date'
		})
	
	if not requests:
		return jsonify({'requests': []}), 200
	
	return jsonify({'requests': requests}), 200



@app.route('/get_booked_details', methods=['GET'])
def get_booked_details():
	labour_id = request.args.get('labour_id')
	if not labour_id:
		return jsonify({'error': 'Labour ID is required'}), 400

	bookings = booking_collection.find({'labour_id': labour_id})
	bookings_list = list(bookings)
	for booking in bookings_list:
		booking['_id'] = str(booking['_id'])
	return jsonify({'bookedDetails': bookings_list})


# to display the booking history
@app.route('/get_user_bookings', methods=['GET'])
def get_user_bookings():
	user_id = request.args.get('user_id')
	print("Received user_id:", user_id)  # Debugging line
	if not user_id:
		return jsonify({"error": "User ID is required"}), 400
	
	try:
		# Convert user_id to integer
		user_id = int(user_id)
	except ValueError:
		return jsonify({"error": "Invalid User ID format"}), 400

	bookings = booking_collection.find({"user_id": user_id}, {"_id": 0, 
						"order_id":1,
						"labour_id": 1,
						"status": 1, 
						"working_date": 1,
						"labour_name": 1,
						"user_name":1,
						"otp": 1
						})
	booking_list = list(bookings)
	print("get_user_booking details:", booking_list)  # Debugging line
	
	return jsonify({"bookings": booking_list})


# ===================================================== Labour Code ======================================



def labour_id_generate():
	print("generating the labour unique ID")
	# Generate the first two letters (uppercase)
	first_two_letters = ''.join(random.choices(string.ascii_uppercase, k=3))
	# Generate the next two digits
	two_digits = ''.join(random.choices(string.digits, k=3))

	# Combine them to form the unique ID
	labour_id = first_two_letters + two_digits
	print(labour_id)
	return labour_id



@app.route('/LabourSignup', methods=['POST'])
def labour_signup():
	if request.method == 'POST':
		data = request.form

		# Extract form data
		name = data.get('name')
		professional = data.get('professional')
		mobile_number = data.get('mobile_number')
		alt_mobile_number = data.get('alt_mobile_number')
		email = data.get('email')
		address = data.get('address')
		city = data.get('city')
		state = data.get('state')
		pincode = data.get('pincode')
		username = data.get('username')
		password = data.get('password')

		# Handle file upload
		if 'address_proof' not in request.files:
			return jsonify({'message': 'No file part'}), 400
		
		file = request.files['address_proof']
		if file.filename == '':
			return jsonify({'message': 'No selected file'}), 400
		
		if file:
			filename = secure_filename(file.filename)
			unique_id = str(uuid.uuid4())
			unique_filename = f"{unique_id}_{filename}"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))


		cdt = datetime.datetime.now()
		user_id = user_id_generate()
		user_reg_cdt = datetime.datetime.strftime(cdt, '%y-%m-%d %H:%M:%S')


		# Current Date and Time

		user_reg_cd = cdt.strftime('%y-%m-%d')

		hashed_password = generate_password_hash(password)
		labour_id = labour_id_generate()

		# Create a dictionary to store in MongoDB
		user_data = {
			'user_id': labour_id,
			'user_registration_date': user_reg_cd,
			'user_registration_datetime': user_reg_cdt,
			'name': name,
			'professional': professional,
			'mobile_number': mobile_number,
			'alternative_mobile_number': alt_mobile_number,
			'email': email,
			'address': address,
			'city': city,
			'state': state,
			'pincode': pincode,
			'address_proof': unique_filename,
			'username': username,
			'password': hashed_password,
			'original password': password,
		}

		# Insert data into the collection
		labour_collection.insert_one(user_data)

		return jsonify({'message': 'Signup successful!'}), 201
	


@app.route('/labour_dashboard', methods=['GET'])
def labour_dashboard():
	if 'labour_id' not in session:
		return jsonify({'message': 'Unauthorized access'}), 401

	labour_id = session['labour_id']
	requests = booking_collection.find({'labour_id': labour_id})
	requests_list = []
	for request_entry in requests:
		requests_list.append({
			'user_id': request_entry['user_id'],
			'request_date': request_entry['request_date'],
			'status': request_entry['status']
		})

	if not requests_list:
		return jsonify({
			'labour_id': labour_id,
			'has_requests': False,
			'message': 'No requests available'
		}), 200

	return jsonify({
		'labour_id': labour_id,
		'has_requests': True,
		'requests': requests_list
	}), 200



@app.route('/LabourLogin', methods=['POST'])
def LabourLogin():
	data = request.json
	print("data from the login link :", data)
	username = data.get('username')
	password = data.get('password')

	if data is None:
		return jsonify({"error": "Invalid JSON"}), 400

	existing_user = labour_collection.find_one({
			'username': username,
			'password': password
		})
	if existing_user:
			print(existing_user)
			print(existing_user['labour_id'])
			session['labour_id'] = existing_user['labour_id']
			labour_id =  existing_user['labour_id']
			name = existing_user['labour_name']
			print(labour_id, name)
			return jsonify({'message': 'Login successful!', 'labour_id': existing_user['labour_id'], 'name': existing_user['labour_name']}), 200
	else:
		# Return failure response
		return jsonify({'message': 'Invalid username or password'}), 401
   
def otp_generate():
	print("generating the OTP for confirmation")

	# labour_id = random.randint(1000, 9999) # 4 digit unique ID generation
	otp_code = random.randint(1000, 9999) # 4 digit unique ID generation
	return otp_code


@app.route('/respond_request', methods=['POST'])
def respond_request():
	data = request.get_json()
	
	labour_id = data.get('labour_id')
	user_id = data.get('user_id')
	response = data.get('response')  # 'accept' or 'reject'
	
	if not labour_id or not user_id or not response:
		return jsonify({'message': 'Missing required fields'}), 400
	
	# Fetch the request from the booking_collection
	booking = booking_collection.find_one({'user_id': user_id, 'labour_id': labour_id})
	print("booking data in respond_request calling function", booking)
	
	if not booking:
		return jsonify({'message': 'Booking not found'}), 404
	
	# Update the booking status based on the response
	new_status = 7 if response == 'accept' else 8

	# Update the booking collection
	update_data = {'status': new_status}

	# Add the OTP to the update data if the response is 'accept'
	if response == 'accept':
		otp_code = otp_generate()
		update_data['otp'] = otp_code

		# Store booking details in booked_details collection
		booked_details_collection.insert_one({
			'user_id': user_id,
			'labour_id': labour_id,
			# 'request_date': booking['request_date'],
			'status': new_status,
			'otp': otp_code
		})
	

	print("response while requesting update_data : ", update_data )

	booking_collection.update_one(
	{'order_id': booking['order_id']},
	{'$set': update_data}
	)

	# booking_collection.update_one(
	#     {'order_id': booking['order_id']},
	#     {'$set': {'status': new_status}}
	# )
	
	return jsonify({'message': f'Request {response}ed successfully'}), 200

'''
@app.route('/update-request', methods=['POST'])
def update_request():
	data = request.get_json()
	request_id = data.get('request_id')
	status = data.get('status')
	
	if not request_id or status not in ['Accepted', 'Rejected']:
		return jsonify({'message': 'Invalid input'}), 400

	result = booking_collection.update_one(
		{'_id': request_id},
		{'$set': {'status': status}}
	)
	
	if result.matched_count == 0:
		return jsonify({'message': 'Request not found'}), 404
	
	return jsonify({'message': 'Request updated successfully'}), 200

'''

@app.route('/labour_logout', methods=['POST'])
def labour_logout():
	# Clear the session to log the user out
	session.clear()
	return jsonify({'message': 'Logout successful'}), 200



@app.route('/validate_otp', methods=['POST'])
def validate_otp():
    data = request.get_json()
    order_id = data.get('order_id')
    otp = data.get('otp')
    otp = int(otp)

    print("Validating the otp, order id is:", order_id)
    print("Validating the otp, from frontend otp value is:", otp)

    booking = booking_collection.find_one({"order_id": order_id})
    if not booking:
        return jsonify({"success": False, "message": "Booking not found"}), 404

    booking_otp = int(booking.get('otp'))
    print("validate otp, booking otp value is:", booking_otp)

    if booking_otp == otp:
        # Update the booking status to 'Started'
        update_result = booking_collection.update_one(
            {"order_id": order_id},
            {"$set": {"status": "Started"}}
        )
        print("Update result:", update_result.modified_count)

        if update_result.modified_count == 1:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Failed to update status"}), 500
    else:
        return jsonify({"success": False, "message": "Invalid OTP"}), 400
	
@app.route('/end_work', methods=['POST'])
def end_work():
    data = request.json
    order_id = data.get('order_id')

    # Implement your logic to mark the work as ended and process payment
    # For example, update the booking status in your database
    # and process the payment.

    # Assuming everything goes well:
    return jsonify({"success": True}), 200
	
# ============================================= AGENT CODE =====================================


def agent_id_generate():
	print("generating the labour unique ID")
	# Generate the first two letters (uppercase)
	first_two_letters = ''.join(random.choices(string.ascii_uppercase, k=3))
	# Generate the next two digits
	two_digits = ''.join(random.choices(string.digits, k=3))

	# Combine them to form the unique ID
	labour_id = first_two_letters + two_digits
	print(labour_id)
	return labour_id


@app.route('/AgentSignup', methods=['POST'])
def agent_signup():
	if request.method == 'POST':
		data = request.form

		# Extract form data
		name = data.get('name')
		mobile_number = data.get('mobile_number')
		alt_mobile_number = data.get('alt_mobile_number')
		email = data.get('email')
		address = data.get('address')
		city = data.get('city')
		state = data.get('state')
		pincode = data.get('pincode')
		username = data.get('username')
		password = data.get('password')

		# Handle file upload
		if 'address_proof' not in request.files:
			return jsonify({'message': 'No file part'}), 400
		
		file = request.files['address_proof']
		if file.filename == '':
			return jsonify({'message': 'No selected file'}), 400
		
		if file:
			filename = secure_filename(file.filename)
			unique_id = str(uuid.uuid4())
			unique_filename = f"{unique_id}_{filename}"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))


		cdt = datetime.datetime.now()
		agent_id = agent_id_generate()
		user_reg_cdt = datetime.datetime.strftime(cdt, '%y-%m-%d %H:%M:%S')


		# Current Date and Time

		user_reg_cd = cdt.strftime('%y-%m-%d')

		hashed_password = generate_password_hash(password)

		# Create a dictionary to store in MongoDB
		user_data = {
			'agent_id': agent_id,
			'agent_registration_date': user_reg_cd,
			'agent_registration_datetime': user_reg_cdt,
			'name': name,
			'mobile_number': mobile_number,
			'alternative_mobile_number': alt_mobile_number,
			'email': email,
			'address': address,
			'city': city,
			'state': state,
			'pincode': pincode,
			'address_proof': unique_filename,
			'username': username,
			'password': hashed_password,
			'original password': password ,
		}

		# Insert data into the collection
		agent_collection.insert_one(user_data)

		return jsonify({'message': 'Signup successful!'}), 201
	

@app.route('/AgentLogin', methods=['POST'])
def AgentLogin():
	data = request.json
	username = data.get('username')
	password = data.get('password')

	user = agent_collection.find_one({'username': username})
	if user and check_password_hash(user['password'], password):
		session['agent_id'] = user['agent_id']
		session['username'] = username
		session['logged_in'] = True
		return jsonify({'message': 'Login successful!'}), 200
	else:
		return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/AgentDashboard')
def AgentDashboard():
	if 'logged_in' in session:
		user = agent_collection.find_one({'username': session.get('username')})
		user_data = {
			'name': user.get('name'),
			'email': user.get('email'),
			'city': user.get('city'),
			'state': user.get('state'),
			'pincode': user.get('pincode'),
		}
		return jsonify(user_data), 200
	else:
		return jsonify({'message': 'Unauthorized'}), 401
	

@app.route('/Agentlogout')
def Agentlogout():
	session.pop('logged_in', None)
	session.pop('user_id', None)
	session.pop('username', None)
	return jsonify({'message': 'Logged out successfully'}), 200
	

# ======================================= COMMISSION BASED WMPLOYEE ================================


def agent_id_generate():
	print("generating the labour unique ID")
	# Generate the first two letters (uppercase)
	first_two_letters = ''.join(random.choices(string.ascii_uppercase, k=3))
	# Generate the next two digits
	two_digits = ''.join(random.choices(string.digits, k=3))

	# Combine them to form the unique ID
	labour_id = first_two_letters + two_digits
	print(labour_id)
	return labour_id


@app.route('/CbSignup', methods=['POST'])
def cb_signup():
	if request.method == 'POST':
		data = request.form

		# Extract form data
		name = data.get('name')
		mobile_number = data.get('mobile_number')
		alt_mobile_number = data.get('alt_mobile_number')
		email = data.get('email')
		address = data.get('address')
		city = data.get('city')
		state = data.get('state')
		pincode = data.get('pincode')
		username = data.get('username')
		password = data.get('password')

		# Handle file upload
		if 'address_proof' not in request.files:
			return jsonify({'message': 'No file part'}), 400
		
		file = request.files['address_proof']
		if file.filename == '':
			return jsonify({'message': 'No selected file'}), 400
		
		if file:
			filename = secure_filename(file.filename)
			unique_id = str(uuid.uuid4())
			unique_filename = f"{unique_id}_{filename}"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))


		cdt = datetime.datetime.now()
		agent_id = agent_id_generate()
		user_reg_cdt = datetime.datetime.strftime(cdt, '%y-%m-%d %H:%M:%S')


		# Current Date and Time

		user_reg_cd = cdt.strftime('%y-%m-%d')

		hashed_password = generate_password_hash(password)

		# Create a dictionary to store in MongoDB
		user_data = {
			'cb_id': agent_id,
			'registration_date': user_reg_cd,
			'registration_datetime': user_reg_cdt,
			'name': name,
			'mobile_number': mobile_number,
			'alternative_mobile_number': alt_mobile_number,
			'email': email,
			'address': address,
			'city': city,
			'state': state,
			'pincode': pincode,
			'address_proof': unique_filename,
			'username': username,
			'password': hashed_password,
			'original password': password ,
		}

		# Insert data into the collection
		cb_collection.insert_one(user_data)

		return jsonify({'message': 'Signup successful!'}), 201
	

@app.route('/CbLogin', methods=['POST'])
def CbLogin():
	data = request.json
	username = data.get('username')
	password = data.get('password')

	user = cb_collection.find_one({'username': username})
	if user and check_password_hash(user['password'], password):
		session['agent_id'] = user['agent_id']
		session['username'] = username
		session['logged_in'] = True
		return jsonify({'message': 'Login successful!'}), 200
	else:
		return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/CbDashboard')
def CbDashboard():
	if 'logged_in' in session:
		user = cb_collection.find_one({'username': session.get('username')})
		user_data = {
			'name': user.get('name'),
			'email': user.get('email'),
			'city': user.get('city'),
			'state': user.get('state'),
			'pincode': user.get('pincode'),
		}
		return jsonify(user_data), 200
	else:
		return jsonify({'message': 'Unauthorized'}), 401
	

@app.route('/Cblogout')
def Cblogout():
	session.pop('logged_in', None)
	session.pop('user_id', None)
	session.pop('username', None)
	return jsonify({'message': 'Logged out successfully'}), 200


if __name__ == '__main__':
	if not os.path.exists(app.config['UPLOAD_FOLDER']):
		os.makedirs(app.config['UPLOAD_FOLDER'])
	app.run(debug=True, use_reloader=False)
