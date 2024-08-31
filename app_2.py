from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
import os
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
import datetime
import uuid
import random
import string
# import pymongo
from datetime import datetime, timedelta




app = Flask(__name__)


#----------------------------------- for login and logout option xxxxxxxxxxxxxxxxxxxxxxxxx
# from flask_session import Session
# import redis
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_PERMANENT'] = True
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=5000)

# # Initialize the session
# Session(app)

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

from werkzeug.security import generate_password_hash, check_password_hash
app.secret_key = '123456789' 

# Configure Redis


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
customer_collection = db['user_data']
agent_collection = db['agent_data']
cb_collection = db['cb_data']


cdt = datetime.today()


commission_charge = 100
percentage = 2


def cal_percentage(price):
    percentage = 2
    return percentage
    

def calculate_convenience_charge(price, percentage):
    return (price * percentage) / 100




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

from flask import Flask, render_template

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


# @app.route('/')
# def index():
    # states = ["Karnataka", "Tamil Nadu", "Telangana", "Andhra Pradesh", "Kerala", "Maharashtra", "Goa"]
    # professional = ["Driver", "Mechanic", "Electrician", "Painter", "Construction Helpers", "Domestic Helpers", "Gardening", "Factory Helpers"]
#     return render_template('index.html', states=states, worker_types=professional)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/welcome')
def welcome():
    return 'Welcome to K2 company'

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/terms_conditions')
def terms_conditions():
    return render_template('terms_conditions.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/headers')
def headers():
    return render_template('headers.html')



# -------------------------------------------------- chatbot option ------------------------------------

@app.route('/chatbot_option', methods=['POST'])
def chatbot_option():
    data = request.json
    option = data.get('option')

    if option == 'marketing':
        response_message = "Marketing selected. How can I assist you with marketing?"
        print(response_message)
    elif option == 'customer_support':
        response_message = "Customer Support selected. How can I assist you with customer support?"
    else:
        response_message = "Option not recognized."

    return jsonify({'message': response_message})

# ----------------------------------------------------Labour Code -------------------------------------

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


@app.route('/labour_reg', methods=['POST', 'GET'])
def labour_reg():
    return render_template('labour_reg.html')


@app.route('/labour_login', methods=['POST', 'GET'])
def labour_login():

    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']

        # Check for existing booking
        existing_labour = labour_collection.find_one({
            'username': username,
            'password': password
        })

        if existing_labour:
            session['labour_id'] = existing_labour['labour_id']
            labour_id = existing_labour['labour_id']
            return redirect(url_for('labour_dashboard'))
        
        else:
            print("User does not exist or incorrect credentials")
            return render_template('labour_login.html', error="Invalid credentials")

    return render_template('labour_login.html')




@app.route('/update_availability', methods=['POST'])
def update_availability():
    data = request.json
    labour_id = data.get('labour_id')
    status_dates = data.get('status_dates')

    result = labour_collection.update_one(
        {'labour_id': labour_id},
        {'$set': {'status_dates': status_dates}}
    )

    if result.modified_count > 0:
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

import logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/labour_dashboard')
def labour_dashboard():
    try:
        if 'labour_id' not in session:
            return redirect(url_for('user_login'))
        
        labour_id = session['labour_id']
        logging.info(f"Labour ID from session: {labour_id}")
        
        labour = labour_collection.find_one({"labour_id": labour_id})
        if not labour:
            logging.error(f"No labour found with ID: {labour_id}")
            return "Labour not found", 404

        labour_data = labour_collection.find_one({"labour_id": labour_id})
        orders = labour_data.get('orders', []) if labour_data else []
        
        bookings = booking_collection.find({"labour_id": labour_id})
        print("bookings details is : ", bookings)
        booking_list = []
        
        for booking in bookings:
            print("bookings details is : ", booking)
            booking_list.append({
                # 'order_id': booking['order_id'],
                'user_id': booking['user_id'],
                # 'start_date': booking['start_date'],
                'status': booking['status'],
                'otp_code': booking.get('otp_code', None)
            })
        
        logging.info(f"Labour ID: {labour_id}")
        logging.info(f"Booking List: {booking_list}")

        return render_template('labour_dashboard.html', labour_id=labour_id, bookings=booking_list)

    except Exception as e:
        logging.error(f"Error fetching labour data: {e}")
        return "An error occurred", 500



from bson.objectid import ObjectId

@app.route('/validate_otp', methods=['POST'])
def validate_otp():
    data = request.get_json()
    print("json data is :",data)
    order_id = data['order_id']
    otp = data['otp']
    print("json otp code is:", otp)

    booking = booking_collection.find_one({'order_id': order_id})

    if booking:
        print("booking data is:", booking)
        otp_code = booking.get('otp_code')  # Using .get() to avoid KeyError
        print("otp_code is:", otp_code)
        if   int(otp) ==  otp_code:
            booking_collection.update_one({'order_id': order_id}, {'$set': {'status': 777}})
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid OTP'})
    else:
        return jsonify({'success': False, 'message': 'Order not found'})


@app.route('/end_work', methods=['POST'])
def end_work():
    data = request.get_json()
    order_id = data['order_id']

    booking_collection.update_one({'order_id': order_id}, {'$set': {'status': 8}})
    return jsonify({'success': True})




@app.route('/labour_signup', methods=['POST', 'GET'])
def labour_signup():

    agent_id = request.args.get('agent_id', '')
    print("agent id extract for labour signup : ", agent_id)

    if request.method == 'POST':
        agent_id = request.form['agent_id']
        print("Agent ID inside form submission:", agent_id)

        labour_name = request.form['labour_name']
        username = request.form['username']
        password = request.form['password']
        professional = request.form['professional']
        mobile_number = request.form['mobile_number']
        alternative_mobile_number = request.form['alternative_mobile_number']
        email = request.form['email']
        address = request.form['address']
        landmark = request.form['landmark']
        state = request.form['state']
        city = request.form['city']
        pincode = request.form['pincode']
        price = request.form['price']
        

        # Handle file upload
        if 'address_proof' not in request.files:
            return 'No file part'
        
        file = request.files['address_proof']
        if file.filename == '':
            return 'No selected file'
        
        if file:
            filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            unique_filename = f"{unique_id}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

        labour_id = labour_id_generate()

        labour_reg_cd = datetime.strftime(cdt, '%y-%m-%d')
        labour_reg_cdt = datetime.strftime(cdt, '%y-%m-%d %H:%M:%S')

        print("agent_id inside form fill : ", agent_id)
        # Create a dictionary to store in MongoDB
        labour_data = {
            'agent_id' : agent_id,
            'labour_id' : labour_id,
            'labour_registration_date':labour_reg_cd, 
            'labour_registration_datetime':labour_reg_cdt,
            'labour_name': labour_name,
            'professional':professional,
            'mobile_number': mobile_number,
            'alternative_mobile_number' :alternative_mobile_number,
            'email_id': email,
            'address': address,
            'landmark': landmark,
            'city' : city,
            'state': state,
            'pincode': pincode,            
            'address_proof': unique_filename,
            'username': username,
            'password': password,
            'price_per_day' :price
            }

        # Insert data into the collection
        labour_collection.insert_one(labour_data)

        # Redirect to home page after successful signup
        return redirect(url_for('labour_login'))
    
    return render_template('labour_signup.html',  agent_id=agent_id)





#----------------------------------------------------- User code -----------------------------------


@app.route('/user_login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']

        # Debug: Print extracted values
        print(f"Username: {username}, Password: {password}")

        # Check for existing user
        existing_user = customer_collection.find_one({
            'username': username,
            'password': password
        })

        # Debug: Print the result of the MongoDB query
        print(f"Existing User: {existing_user}")

        if existing_user:
            session['user_id'] = existing_user['user_id']
            return redirect(url_for('user_dashboard'))  # Redirect to dashboard after login

        else:
            return render_template('user_login.html', error="Invalid credentials")

    return render_template('user_login.html')



@app.route('/user_dashboard')
def user_dashboard():
    states = ["Karnataka", "Tamil Nadu", "Telangana", "Andhra Pradesh", "Kerala", "Maharashtra", "Goa"]
    city = ["Bangalore-Banashankari", "Bangalore-JP Nagar", "Bangalore-Jayanagar",
                        "Bangalore-Rajajinagar", "Bangalore-Yeshvantpur"]
    professional = ["Driver", "Mechanic", "Electrician", "Painter", "Construction Helpers", "Domestic Helpers", "Gardening", "Factory Helpers", "PHP"]
    
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    user_id = session['user_id']
    print("user_id is :", user_id)
    
    bookings = booking_collection.find({"user_id": user_id})
    booking_list = []
    for booking in bookings:
        print("bookings data is :", booking)

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ booking details is not fetching from user_id
        # price_per_day = booking['price_per_day']
        price_per_day = "0"
        # number_working_days = booking['total_number_working_days']   
        number_working_days =  "1"
        price = int(price_per_day) + commission_charge
        total_price = price * number_working_days
        print("price to display :", price)
        percentage = cal_percentage(price)
        convenience_charge = calculate_convenience_charge(price, percentage)
        
        booking_list.append({
            'order_id': str(booking.get('order_id', 'N/A')),
            'user_id': booking.get('user_id', 'N/A'),
            'start_date': booking.get('start_date', 'N/A'),
            'end_date': booking.get('end_date', 'N/A'),
            'total_number_working_days': booking.get('total_number_working_days', 'N/A'),
            'status': booking.get('status', 'N/A'),
            'otp_code': booking.get('otp_code', 'N/A'),
            "labour_charge": price,
            'total_charge': total_price
        })
        print("booking_list data is :", booking_list)

    return render_template('user_dashboard.html', user_id=user_id, booking_list=booking_list, states=states, cities=city,worker_types=professional)


@app.route('/get_notifications', methods=['GET'])
def get_notifications():
    labour_id = session.get('labour_id')
    if not labour_id:
        return jsonify({'error': 'Labour ID not found in session'}), 400
    
    notifications = booking_collection.find({'labour_id': labour_id})

    # Convert ObjectId to string
    notifications_list = []
    for notification in notifications:
        notification['_id'] = str(notification['_id'])
        notifications_list.append(notification)

    return jsonify({'notifications': notifications_list})


def generate_otp():
    return random.randint(1000, 9999)

def send_otp_to_user(notification_id):
    booking = booking_collection.find_one({'_id': notification_id})
    user_id = booking['user_id']
    otp = booking['otp']



@app.route('/handle_notification', methods=['POST'])
def handle_notification():
    data = request.json
    action = data['action']
    notification_id = ObjectId(data['notification_id'])
    
    if action == 'accept':
        otp = generate_otp()
        order_id = order_id_generate()
        ordered_cdt = datetime.strftime(cdt, '%y-%m-%d %H:%M:%S')

        start_date = "2024-08-10" # hardcoded .....................
        end_date = "2024-08-12" # hardcoded ...........................

        number_working_days = calculate_number_days(start_date, end_date)

        booking_collection.update_one({'_id': notification_id}, {'$set': {'status': 'accepted',
                                         'otp': otp, 'order_id': order_id, 
                                         "booked_datetime" : ordered_cdt,
                                         'total_number_working_days' : number_working_days,
                                         }})
        send_otp_to_user(notification_id)  
        return jsonify({'success': True})
    
    elif action == 'reject':
        booking_collection.update_one({'_id': notification_id}, {'$set': {'status': 'rejected'}})
        return jsonify({'success': True})
    
    return jsonify({'success': False})


@app.route('/send_booking_request', methods=['POST'])
def send_booking_request():
    data = request.json
    labour_id = data['labour_id']
    user_id = data['user_id']
    # Add request to MongoDB booking_collection
    booking_request = {
        'labour_id': labour_id,
        'user_id': user_id,
        'status': 'pending', 
        'otp': None  
    }
    booking_collection.insert_one(booking_request)
    return jsonify({'success': True})


@app.route('/spot_booking', methods=['GET', 'POST'])
def spot_booking():

    if 'user_id' in session:
        user_id = session['user_id']
        state = request.form.get('state')
        city = request.form.get('city')
        worker_type = request.form.get('worker_type')
        
        print("user_id in spot booking : ", user_id)

        if not user_id:
            return redirect(url_for('user_login'))
        
        states = ["Karnataka", "Tamil Nadu", "Telangana", "Andhra Pradesh", "Kerala", "Maharashtra", "Goa"]
        city = ["Bangalore-Banashankari", "Bangalore-JP Nagar", "Bangalore-Jayanagar",
                        "Bangalore-Rajajinagar", "Bangalore-Yeshvantpur"]
        professional = ["Driver", "Mechanic", "Electrician", "Painter", "Construction Helpers", "Domestic Helpers", "Gardening", "Factory Helpers", "PHP"]
    

        workers = labour_collection.find({"state": state, "city": city, "worker_type": worker_type})
        
        worker_list = list(workers)
        print("workers list are :", worker_list)
        return render_template('spot_booking.html', user_id=user_id, worker_list=worker_list, booking_type='spot', states=states, cities=city,worker_types=professional)

    else:
        return redirect(url_for('user_login'))
    


@app.route('/long_booking', methods=['GET', 'POST'])
def long_booking():
    return render_template('long_booking.html')

 
# under spot booking search function is calling 

# Helper function to convert ObjectId to string
def convert_objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, list):
        return [convert_objectid_to_str(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_objectid_to_str(value) for key, value in obj.items()}
    else:
        return obj


@app.route('/search_workers', methods=['POST'])
def search_workers():
    state = request.form.get('state')
    city = request.form.get('city')
    worker_type = request.form.get('worker_type')
    booking_date = request.form.get('booking_date')

    query = {"state": state, "city": city, "professional": worker_type, "is_active": 4}
    workers = labour_collection.find(query)
    worker_list = [convert_objectid_to_str(worker) for worker in workers]

    return jsonify({'workers': worker_list})

@app.route('/send_booking_request_spot', methods=['POST'])
def send_booking_request_spot():
    data = request.json
    user_id = data['user_id']
    worker_list = data['worker_list']
    
    for worker in worker_list:
        labour_id = worker['labour_id']
        booking_request = {
            'labour_id': labour_id,
            'user_id': user_id,
            'status': 'pending',
            'otp': None
        }
        booking_collection.insert_one(booking_request)
    
    return jsonify({'success': True})




# ============================= spot booking ======================================================
    

@app.route('/advance_booking', methods=['GET', 'POST'])
def advance_booking():

    if 'user_id' in session:

        state = request.form.get('state')
        city = request.form.get('city')
        worker_type = request.form.get('worker_type')
        booking_date = request.form.get('booking_date')
        user_id = session.get('user_id')

        if not user_id:
            return redirect(url_for('user_login'))

        workers = labour_collection.find({"state": state, "city": city, "worker_type": worker_type})
        worker_list = list(workers)

        states = ["Karnataka", "Tamil Nadu", "Telangana", "Andhra Pradesh", "Kerala", "Maharashtra", "Goa"]
        city = ["Bangalore-Banashankari", "Bangalore-JP Nagar", "Bangalore-Jayanagar",
                            "Bangalore-Rajajinagar", "Bangalore-Yeshvantpur"]
        professional = ["Driver", "Mechanic", "Electrician", "Painter", "Construction Helpers", "Domestic Helpers", "Gardening", "Factory Helpers", "PHP"]
        
        return render_template('advance_booking.html', user_id=user_id, worker_list=worker_list, booking_type='advance', booking_date=booking_date, states=states, cities=city,worker_types=professional)


# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def user_id_generate():
    print("generating the labour unique ID")

    # labour_id = random.randint(1000, 9999) # 4 digit unique ID generation
    user_id = random.randint(10000, 99999) # 4 digit unique ID generation
    return user_id


# User Sign up Page
@app.route('/user_signup', methods=['POST', 'GET'])
def user_signup():
    if request.method == 'POST':
        # Extract form data

        user_name = request.form['name']
        mobile_number = request.form['mobile_number']
        alternative_mobile_number = request.form['alt_mobile_number'] 
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        landmark = request.form['landmark']
        pincode = request.form['pincode']

        username = request.form['username']
        password = request.form['password']

        # Handle file upload
        if 'address_proof' not in request.files:
            return 'No file part'
        
        file = request.files['address_proof']
        if file.filename == '':
            return 'No selected file'
        
        if file:
            filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            unique_filename = f"{unique_id}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

        user_id = user_id_generate()
        user_reg_cdt = datetime.strftime(cdt, '%y-%m-%d %H:%M:%S')
        
        # Create a dictionary to store in MongoDB
        customer_data = {
                'user_id' : user_id,
                'user_registration_datetime': user_reg_cdt,
                'user_name': user_name,
                'mobile_number': mobile_number,
                'alternative_mobile_number' : alternative_mobile_number,
                'email': email,
                'address': address,
                'city': city,
                'state': state,
                'pincode' : pincode,
                'landmark' : landmark,
                'address_proof': unique_filename,
                'username': username,
                'password': password,
                'signup_datetime' : "NA",
                'status' : 6,
                'remark' : "successfully signup, verification is pending"
            }

        # Insert data into the collection
        customer_collection.insert_one(customer_data)

        # Redirect to home page after successful signup
        # return redirect(url_for('index'))
        return redirect(url_for('user_login'))
    
    return render_template('user_signup.html')



@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    labour_id = data.get('labour_id')
    date = data.get('date')
    status = data.get('status')
    
    labour = labour_collection.find_one({'_id': ObjectId(labour_id)})
    
    if not labour:
        return jsonify({'success': False, 'error': 'Labour not found'})
    
    status_dates = labour.get('status_dates', [])
    
    # Check if the date already exists in the status_dates array
    for status_date in status_dates:
        if status_date['date'] == date:
            status_date['status'] = status
            break
    else:
        # If date does not exist, add a new entry
        status_dates.append({'date': date, 'status': status})
    
    labour_collection.update_one({'_id': ObjectId(labour_id)}, {'$set': {'status_dates': status_dates}})
    
    return jsonify({'success': True})



# User Login Page
@app.route('/login', methods=['POST', 'GET'])
def login():
    states = ["Karnataka", "Tamil Nadu", "Telangana", "Andhra Pradesh", "Kerala", "Maharashtra", "Goa"]
    professional = ["Driver", "Mechanic", "Electrician", "Painter", "Construction Helpers", "Domestic Helpers", "Gardening", "Factory Helpers", "PHP"]
    
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']

                # Check for existing booking
        existing_user = customer_collection.find_one({
            'username': username,
            'password': password
        })

        if existing_user:
            return render_template('user_dashboard.html', states=states, worker_types=professional)
        else:
            print("already exited")
    return render_template('user_login.html')
        

@app.route('/workers', methods=['POST'])
def workers():
    state = request.form['state']
    city = request.form['city']
    worker_type = request.form['worker_type']

    today_date = datetime.today().strftime('%Y-%m-%d')

    # Fetch workers from MongoDB based on the search criteria
    workers = list(labour_collection.find({
        'state': state,
        'city': city,
        'professional': worker_type,
        'is_active': 4
    }))

    # Convert ObjectId to string
    workers_list = []
    for worker in workers:
        worker['_id'] = str(worker['_id'])
        workers_list.append(worker)

    print("workers_list inside @worker is:", workers_list)
    
    return jsonify({'workers': workers_list})


@app.route('/book_worker', methods=['POST'])
def book_worker():
    data = request.json
    labour_id = data['labour_id']
    user_id = data['user_id']
    booking_request = {
        'labour_id': labour_id,
        'user_id': user_id,
        'status': 'pending',
        'requested_at': datetime.now()
    }
    labour_collection.booking_requests.insert_one(booking_request)
    # Notify the labourer (Assuming a notification system is in place)
    labour_collection.update_one(
        {'_id': ObjectId(labour_id)},
        {'$set': {'new_request': True}}
    )
    return jsonify(success=True)


def otp_generate():
    print("generating the OTP for confirmation")

    # labour_id = random.randint(1000, 9999) # 4 digit unique ID generation
    otp_code = random.randint(1000, 9999) # 4 digit unique ID generation
    return otp_code


def order_id_generate():
    print("generating the order id")
    order_id = str(uuid.uuid4().hex)[:16].lower()
    return order_id


def calculate_number_days(start_date, end_date):
    print("checking the number of days to be worked")
    print(type(start_date))
    print("start_date is :", start_date)
    print("end_date is :", end_date)
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)
    a =  abs((end_date-start_date).days)
    days = int(a) + 1
    return days


@app.route('/book', methods=['POST'])
def book():
    # labour_id = request.form['worker_id']
    labour_id = request.form['worker_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    user_id = session['user_id']  # Assuming the user ID is stored in the session


    otp_code = otp_generate()

    number_working_days = calculate_number_days(start_date, end_date)

    # Check for existing booking
    existing_booking = booking_collection.find_one({
            'labour_id': labour_id,
            'start_date': {'$lte': end_date},
            'end_date': {'$gte': start_date}
        })
    
    print("labour id is :", labour_id)
    if existing_booking:
            message = "This worker is already booked for the selected dates."
    else:
        agentData = labour_collection.find_one({"labour_id" : labour_id})
        print("agentData is :", agentData)

        if agentData:
            agent_id = agentData['agent_id']
            price_per_day = agentData['price_per_day']

        else:
            print("No data found for labour_id:", labour_id)

        order_id = order_id_generate()

        booked_cdt = datetime.strftime(cdt, '%y-%m-%d %H:%M:%S')

        # Insert booking data into MongoDB
        booking = {
        'order_id' : order_id,
        'booked_datetime' : booked_cdt,
        'user_id': user_id,
        'labour_id': labour_id,
        'agent_id' : agent_id,
        'start_date': start_date,
        'end_date': end_date,
        'total_number_working_days' : number_working_days,
        'status': "pending",
        'otp_code' : otp_code,
        'remark': 'Booked',
        'price_per_day': price_per_day
        }
  
        booking_collection.insert_one(booking)
        message = "Worker booked successfully!"
    
    return redirect(url_for('user_dashboard'))


def get_payment_details(order_id):
    print("order id in get_payment_details :", order_id)

    pay_bookings = booking_collection.find({"order_id": order_id})
    print("payment details booking info:", pay_bookings)
    payment_details = []
    for pay_booking in pay_bookings:
        print("bookings data is :", pay_booking)
        price_per_day = pay_booking['price_per_day']
        number_working_days = pay_booking['total_number_working_days']
        price = int(price_per_day) + commission_charge
        total_price = price * number_working_days
        print("price to display :", price)
        percentage = cal_percentage(price)
        convenience_charge = calculate_convenience_charge(price, percentage)

        payment_details.append({
            'order_id': str(pay_booking['order_id']),  
            'user_id': pay_booking['user_id'],
            'start_date': pay_booking['start_date'],
            'end_date': pay_booking['end_date'],
            'total_number_working_days' : pay_booking['total_number_working_days'],
            "labour_charge" : price,
            'total_charge' : total_price
        })
        print("booking_list data is :", payment_details)
    # Implement the logic to fetch payment details based on the order_id
    return payment_details
    

@app.route('/user_payment')
def user_payment():
    order_id = request.args.get('order_id')
    print("order ID is :",order_id)
    # Fetch the complete details for the order_id and pass it to the template
    payment_details = get_payment_details(order_id)  # Define this function to get payment details
    print("payment details is :", payment_details)

        # Pass only the first element if the list is not empty
    if payment_details:
        payment_detail = payment_details[0]
    else:
        payment_detail = None

    return render_template('user_payment.html', payment_detail=payment_detail)

    '''
    global payment, name
    name = request.form.get('user_name')
    client = razorpay.Client(auth= ('', ""))

    data = {"amount": price, "currency": "INR", "receipt": "#11"}
    payment = client.order.create(data= data)
    '''




# ------------------------------------------------------  Agent Part Code ---------------------------------- 


def agent_id_generate():
    print("generating the agent unique ID")

    # Generate the first two letters (uppercase)
    first_two_letters = ''.join(random.choices(string.ascii_uppercase, k=2))

    # Generate the next two digits
    two_digits = ''.join(random.choices(string.digits, k=2))

    # Combine them to form the unique ID
    agent_id = first_two_letters + two_digits

    print(agent_id)
    return agent_id

from werkzeug.security import check_password_hash, generate_password_hash

@app.route('/agent_login', methods=['POST', 'GET'])
def agent_login():

    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']

                # Fetch agent details from the database
        existing_user = next((user for user in agent_collection if user['username'] == username), None)
        print("Existing user details: ", existing_user)

        # Check if username exists and password is correct
        if existing_user and check_password_hash(existing_user['password'], password):
            session["user"] = existing_user['username']
            session.permanent = True  # Session will be permanent until logout
            app.permanent_session_lifetime = datetime.timedelta(days=7)  # Session lasts for 7 days
            return redirect("/agent_dashboard")
        else:
            return render_template("login.html", message="Invalid username or password.")
        
    if "user" in session:
        return redirect("/agent_dashboard")

    return render_template("login.html")

    '''

    # Check for existing booking
    existing_user = agent_collection.find_one({'name': username   })
    print("existing_user deatils is : ", existing_user)

    # Check if username exists and password is correct
    if username and check_password_hash(username.password, password):
        session["user"] =  existing_user['username']
        return redirect("/agent_dashboard")
    else:
        return render_template("login.html", message="Invalid username or password.")

'''
    '''
    if existing_user:
        print("existing user is satisfied")
        if check_password_hash(existing_user['password'], password):
            session['name'] = username
            print("returning to the agent dashboard")
            return redirect(url_for('agent_dashboard'))
        else:
            return 'Invalid Credentials', 401
    else:
        return 'Invalid credentials', 401
    '''
    
# return render_template('agent_login.html')


@app.route('/agent_logout')
def agent_logout():
    # session.pop('name', None)
    session.clear()
    return redirect(url_for('agent_login'))
        

@app.route('/agent_dashboard')
def agent_dashboard():
    if 'username' not in session:
        return redirect(url_for('agent_login'))

    username = session['username']
    agent_name = agent_collection.find({'username': username})
    print("agent_name details is :", agent_name)
    # agent_name = agent_name['name']
    agent_name = "NA"
    # agent_username = agent_name['username']
    agent_username = "NA"
    # agent_id = session.get('agent_id')  # Assuming the agent ID is stored in the session

    if not username:
        return redirect(url_for('login'))  # Redirect to login if agent ID is not found

    # bookings = booking_collection.find({'agent_id': agent_id})
    bookings = booking_collection.find({'agent_id': username}).sort('registered_date', -1).limit(3)
    bookings = list(bookings)
    
    # print("agent id is : ", agent_id)

    # labours = labour_collection.find({'agent_id': agent_id})
    # or
    agent = agent_collection.find_one({'agent_id': username})
    labours = labour_collection.find({'city': agent['city']})
    labour_list = [labour for labour in labours]

    # print("labour_list is :", labour_list )
    # return render_template('agent_dashboard.html', agent_name = agent_name, agent_username = agent_username, agent_id=agent_id, bookings=bookings, labours=labour_list)
    return render_template('agent_dashboard.html', 
                           agent_name=agent['name'], 
                           agent_id=agent['agent_id'],
                           agent_username=agent['username'],
                           bookings=bookings,
                           labours=labours)

@app.route('/submit_labours', methods=['POST'])
def submit_labours():
    data = request.get_json()
    print("data from the selected labour id but :", data)

    # Process and print the values one by one
    for labour_id in data['labour_ids']:
        print(labour_id)  # This prints to the server log
        found_labours = labour_collection.find_one({'labour_id': labour_id })
        print(found_labours)
        if found_labours:
            labour_collection.update_one({'labour_id': labour_id}, {'$set': {'active_status': 4}})
            return jsonify({'message': 'Labours received and updated successfully'}), 200
        
    else:
        return jsonify({'error': 'No labour IDs provided'}), 400



def agent_id_generate():
    print("generating the agent unique ID")

    # Generate the first two letters (uppercase)
    first_two_letters = ''.join(random.choices(string.ascii_uppercase, k=2))

    # Generate the next two digits
    two_digits = ''.join(random.choices(string.digits, k=2))

    # Combine them to form the unique ID
    agent_id = first_two_letters + two_digits

    print(agent_id)
    return agent_id


@app.route('/agent_signup', methods=['POST', 'GET'])
def agent_signup():
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        mobile_number = request.form['mobile_number']
        alt_mobile_number = request.form['alt_mobile_number']
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']
        landmark = request.form['landmark']

        # Handle file upload
        if 'address_proof' not in request.files:
            return 'No file part'
        
        file = request.files['address_proof']
        if file.filename == '':
            return 'No selected file'
        
        if file:
            filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            unique_filename = f"{unique_id}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

        agent_id = agent_id_generate()

        agent_reg_cdt = datetime.strftime(cdt, '%y-%m-%d %H:%M:%S')
        agent_reg_cd = datetime.strftime(cdt, '%y-%m-%d')

        hashed_password = generate_password_hash(password)

        # Create a dictionary to store in MongoDB
        agent_data = {
                'agent_id': agent_id,
                'agent_registration_date' :agent_reg_cd,
                'agent_registration_datetime': agent_reg_cdt,
                'name': name,
                'mobile_number': mobile_number,
                'alternative_mobile_number' : alt_mobile_number,
                'email': email,
                'address': address,
                'city': city,
                'state': state,
                'pincode' : pincode,
                'landmark' : landmark,
                'address_proof': unique_filename,
                'username': username,
                'password': password,
            }

        # Insert data into the collection
        agent_collection.insert_one(agent_data)

        # Redirect to home page after successful signup
        # return redirect(url_for('index'))
        return redirect(url_for('agent_login'))
    
    return render_template('agent_signup.html')





# ------------------------------------------------------  Agent Part Code ---------------------------------- 



@app.route('/cb_signup', methods=['POST', 'GET'])
def cb_signup():

    if request.method == 'POST':
        cb_name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        # professional = request.form['professional']
        mobile_number = request.form['mobile_number']
        # alternative_mobile_number = request.form['alternative_mobile_number']
        email = request.form['email']
        address = request.form['address']
        landmark = request.form['landmark']
        state = request.form['state']
        city = request.form['city']
        pincode = request.form['pincode']
        # price = request.form['price']
        

        # Handle file upload
        if 'address_proof' not in request.files:
            return 'No file part'
        
        file = request.files['address_proof']
        if file.filename == '':
            return 'No selected file'
        
        if file:
            filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            unique_filename = f"{unique_id}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

        cb_id = labour_id_generate()

        labour_reg_cd = datetime.strftime(cdt, '%y-%m-%d')
        labour_reg_cdt = datetime.strftime(cdt, '%y-%m-%d %H:%M:%S')

        print("cb_id inside form fill : ", cb_id)
        # Create a dictionary to store in MongoDB
        labour_data = {
            'cb_id' : cb_id,
            'labour_registration_date':labour_reg_cd, 
            'labour_registration_datetime':labour_reg_cdt,
            'cb_name': cb_name,
            # 'professional':professional,
            'mobile_number': mobile_number,
            # 'alternative_mobile_number' :alternative_mobile_number,
            'email_id': email,
            'address': address,
            'landmark': landmark,
            'city' : city,
            'state': state,
            'pincode': pincode,            
            'address_proof': unique_filename,
            'username': username,
            'password': password,
            # 'price_per_day' :price
            }

        # Insert data into the collection
        cb_collection.insert_one(labour_data)

        # Redirect to home page after successful signup
        return redirect(url_for('cb_login'))
    
    return render_template('cb_signup.html')


@app.route('/cb_login', methods=['POST', 'GET'])
def cb_login():
    
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']

                # Check for existing booking
        existing_user = cb_collection.find_one({
            'username': username,
            'password': password
        })

        if existing_user:
            cb_id = existing_user['cb_id']
            if cb_id:
                session['cb_id'] = cb_id
            return redirect(url_for('cb_dashboard'))
        else:
            return 'Invalid credentials', 401

    return render_template('cb_login.html')




@app.route('/cb_dashboard')
def cb_dashboard():
    if 'cb_id' not in session:
        return redirect(url_for('cb_login'))

    cb_id = session['cb_id']
    # agent_id = session.get('agent_id')  # Assuming the agent ID is stored in the session

    if not cb_id:
        return redirect(url_for('login'))  # Redirect to login if agent ID is not found

    cb_deatils = cb_collection.find({'cb_id': cb_id})
    # registered = list(registered)
    
    # print("agent id is : ", agent_id)

    labours = labour_collection.find({'agent_id': cb_id})
    labour_list = [labour for labour in labours]

    # print("labour_list is :", labour_list )
    return render_template('cb_dashboard.html', cb_id=cb_id, labours=labour_list)






#---------------------------------------------------- Main Calling Function ---------------------------------


if __name__ == '__main__':
    # if not os.path.exists(app.config['UPLOAD_FOLDER']):
    #     os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=False, threaded=True)  # Change to False for production






# =======================================================================================================


'''

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from pymongo import MongoClient

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['vehicle_rental']
# vehicle_collection = db['vehicles']
booking_collection = db['bookings']
customer_collection = db['customers']
workers_collection = db['workers']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    states = ["Karnataka", "Tamil Nadu", "Telangana", "Andhra Pradesh", "Kerala", "Maharashtra", "Goa"]
    worker_types = ["Driver", "Mechanic", "Electrician", "Painter", "Construction Helpers", "Domestic Helpers", "Gardening", "Factory Helpers"]
    return render_template('index.html', states=states, worker_types=worker_types)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/vehicles', methods=['POST'])
def vehicles():
    state = request.form['state']
    city = request.form['city']
    worker_type = request.form['worker_type']
    vehicles = list(vehicle_collection.find({'state': state, 'district': city, 'worker_type': worker_type}))
    return render_template('vehicles.html', vehicles=vehicles)



@app.route('/book', methods=['POST'])
def book():
    register_Number = request.form['register_Number']
    name = request.form['name']
    mobile_number = request.form['mobile_number']
    address = request.form['address']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    if 'addressProof' not in request.files:
        return "No file part"
    
    file = request.files['addressProof']
    
    if file.filename == '':
        return "No selected file"
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save customer details
        customer_collection.insert_one({
            'name': name,
            'register_Number': register_Number,
            'mobile_number': mobile_number,
            'address': address,
            'address_proof': filename,
            'start_date': start_date,
            'end_date': end_date
        })

        # Check for existing booking
        existing_booking = booking_collection.find_one({
            'register_Number': register_Number,
            'start_date': {'$lte': end_date},
            'end_date': {'$gte': start_date}
        })

        if existing_booking:
            message = "This vehicle is already booked for the selected dates."
        else:
            booking_collection.insert_one({
                'regNumber': register_Number,
                'start_date': start_date,
                'end_date': end_date,
                'status': 'Booked'
            })
            message = "Vehicle booked successfully!"

        return render_template('message.html', message=message)
    else:
        return "File type not allowed"



if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)  # Change to False for production





--------------------------- original code, before agent booking updation -------------------------------------------------



from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from pymongo import MongoClient

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['vehicle_rental']
vehicle_collection = db['vehicles']
booking_collection = db['bookings']
customer_collection = db['customers']
workers_collection = db['workers']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    states = ["Karnataka", "Tamil Nadu", "Telangana", "Andhra Pradesh", "Kerala", "Maharashtra", "Goa"]
    worker_types = ["Driver", "Mechanic", "Electrician", "Painter", "Construction Helpers", "Domestic Helpers", "Gardening", "Factory Helpers"]
    return render_template('index.html', states=states, worker_types=worker_types)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/vehicles', methods=['POST'])
def vehicles():
    state = request.form['state']
    city = request.form['city']
    worker_type = request.form['worker_type']
    vehicles = list(vehicle_collection.find({'state': state, 'district': city, "worker_type": worker_type}))
    return render_template('vehicles.html', vehicles=vehicles)


@app.route('/book', methods=['POST'])
def book():
    regNumber = request.form['regNumber']
    name = request.form['name']
    mobile_number = request.form['mobile_number']
    address = request.form['address']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    if 'addressProof' not in request.files:
        return "No file part"
    
    file = request.files['addressProof']
    
    if file.filename == '':
        return "No selected file"
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save customer details
        customer_collection.insert_one({
            'name': name,
            'regNumber': regNumber,
            'mobile_number' : mobile_number,
            'address': address,
            'addressProof': filename,
            'start_date': start_date,
            'end_date': end_date
        })

        # Check for existing booking
        existing_booking = booking_collection.find_one({
            'regNumber': regNumber,
            'start_date': {'$lte': end_date},
            'end_date': {'$gte': start_date}
        })

        if existing_booking:
            message = "This vehicle is already booked for the selected dates."
        else:
            booking_collection.insert_one({
                'regNumber': regNumber,
                'start_date': start_date,
                'end_date': end_date,
                'status': 7
            })
            message = "Vehicle booked successfully!"

        return render_template('message.html', message=message)
    else:
        return "File type not allowed"



if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)




'''

'''


# ============================ code with mail updation, No module named 'email_utils' =====================

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pymongo import MongoClient
from email_utils import send_confirmation_email

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['vehicle_rental']
vehicle_collection = db['vehicle']
booking_collection = db['bookings']
customer_collection = db['customers']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    states = ["Karnataka", "Tamil Nadu", "Telangana", "Andhra Pradesh"]
    return render_template('index.html', states=states)

@app.route('/vehicles', methods=['POST'])
def vehicles():
    state = request.form['state']
    city = request.form['city']
    vehicles = list(vehicle_collection.find({'state': state, 'district': city}))
    return render_template('vehicles.html', vehicles=vehicles)

@app.route('/book', methods=['POST'])
def book():
    regNumber = request.form['regNumber']
    name = request.form['name']
    id_number = request.form['id_number']
    email = request.form['email']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    if 'addressProof' not in request.files:
        return "No file part"
    
    file = request.files['addressProof']
    
    if file.filename == '':
        return "No selected file"
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save customer details
        customer_collection.insert_one({
            'name': name,
            'id_number': id_number,
            'email': email,
            'regNumber': regNumber,
            'addressProof': filename,
            'start_date': start_date,
            'end_date': end_date
        })

        # Check for existing booking
        existing_booking = booking_collection.find_one({
            'regNumber': regNumber,
            'start_date': {'$lte': end_date},
            'end_date': {'$gte': start_date}
        })

        if existing_booking:
            message = "This vehicle is already booked for the selected dates."
        else:
            vehicle = vehicle_collection.find_one({'regNumber': regNumber})
            vehicle_type = vehicle['vehicle type']
            booking_collection.insert_one({
                'regNumber': regNumber,
                'start_date': start_date,
                'end_date': end_date
            })
            send_confirmation_email(email, vehicle_type, regNumber)
            message = "Woww Cooool, Vehicle booked successfully! Please check the mail"

        return render_template('message.html', message=message)
    else:
        return "File type not allowed"

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

    

'''





# =============================================== original code working fine R2 last updated code ==============


'''

# ======================================= BEFORE THE E-LABOUR CONCEPT ===============================



from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pymongo import MongoClient

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['vehicle_rental']
vehicle_collection = db['vehicles']
booking_collection = db['bookings']
customer_collection = db['customers']
worker_collection = db['workers']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    states = ["Karnataka", "Tamil Nadu", "Telangana", "Andhra Pradesh", "Kerala", "Maharashtra", "Goa"]
    return render_template('index.html', states=states)

@app.route('/vehicles', methods=['POST'])
def vehicles():
    state = request.form['state']
    city = request.form['city']
    vehicles = list(vehicle_collection.find({'state': state, 'district': city}))
    return render_template('vehicles.html', vehicles=vehicles)

@app.route('/book', methods=['POST'])
def book():
    regNumber = request.form['regNumber']
    name = request.form['name']
    mobile_number = request.form['mobile_number']
    address = request.form['address']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    if 'addressProof' not in request.files:
        return "No file part"
    
    file = request.files['addressProof']
    
    if file.filename == '':
        return "No selected file"
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save customer details
        customer_collection.insert_one({
            'name': name,
            'regNumber': regNumber,
            'mobile_number' : mobile_number,
            'address': address,
            'addressProof': filename,
            'start_date': start_date,
            'end_date': end_date
        })

        # Check for existing booking
        existing_booking = booking_collection.find_one({
            'regNumber': regNumber,
            'start_date': {'$lte': end_date},
            'end_date': {'$gte': start_date}
        })

        if existing_booking:
            message = "This vehicle is already booked for the selected dates."
        else:
            booking_collection.insert_one({
                'regNumber': regNumber,
                'start_date': start_date,
                'end_date': end_date
            })
            message = "Vehicle booked successfully!"

        return render_template('message.html', message=message)
    else:
        return "File type not allowed"

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

'''








'''

# =============================== original code ===================================================== 


from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['vehicle_rental']
vehicle_collection = db['vehicles']
booking_collection = db['bookings']

@app.route('/')
def index():
    states = ["Karnataka", "Tamil Nadu", "Telangana", "Andhra Pradesh", "Kerala", "Goa", "Maharashtra"]
    return render_template('index.html', states=states)

@app.route('/vehicles', methods=['POST'])
def vehicles():
    state = request.form['state']
    city = request.form['city']
    print(f"Selected state: {state}, Selected city: {city}")  # Debugging line
    vehicles = list(vehicle_collection.find({'state': state, 'district': city}))
    print(f"Fetched vehicles: {vehicles}")  # Debugging line
    return render_template('vehicles.html', vehicles=vehicles)

@app.route('/book', methods=['POST'])
def book():
    regNumber = request.form['regNumber']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    existing_booking = booking_collection.find_one({
        'regNumber': regNumber,
        'start_date': {'$lte': end_date},
        'end_date': {'$gte': start_date}
    })

    if existing_booking:
        message = "This vehicle is already booked for the selected dates."
    else:
        booking_collection.insert_one({
            'regNumber': regNumber,
            'start_date': start_date,
            'end_date': end_date
        })
        message = "Vehicle booked successfully!"
    
    return render_template('message.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)

    
'''