from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_login import LoginManager, UserMixin
from pymongo import MongoClient
from bson import ObjectId


app = Flask(__name__ , template_folder='templates')
app.secret_key = 'your_secret_key' 
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Connection to MongoDB 
#------------------------------------------------------------------------------------------------------
client = MongoClient('mongodb://localhost:27017/')

#Database
db = client["root"]  

#All collection
users_collection = db["chemist_signup"]
medicine = db.add_medicine
images_collection = db.photos
order_collection = db.order_of_user
#------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------
# User model for demonstration
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": user_id})
    if user_data:
        user = User()
        user.id = user_data["_id"]
        return user
    return None
#------------------------------------------------------------------------------------------------------






#Home Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/')
def home():
    owl_carousel_css_link = (
        '<link rel="stylesheet" '
        'type="text/css" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.1.3/assets/owl.carousel.min.css">'
    )
    font_awesome_css_link = (
        '<link rel="stylesheet" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
    )
    google_fonts_css_link = (
        '<link href="https://fonts.googleapis.com/css?family=Poppins:400,600,700|Roboto:400,700&display=swap" '
        'rel="stylesheet">'
    )
    if 'user_id' in session:
        return render_template('home.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link,logged_in=True)
    else:
        return render_template('login.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
#------------------------------------------------------------------------------------------------------
    





#Signup Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/signup')
def signup_page():
    owl_carousel_css_link = (
        '<link rel="stylesheet" '
        'type="text/css" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.1.3/assets/owl.carousel.min.css">'
    )
    font_awesome_css_link = (
        '<link rel="stylesheet" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
    )
    google_fonts_css_link = (
        '<link href="https://fonts.googleapis.com/css?family=Poppins:400,600,700|Roboto:400,700&display=swap" '
        'rel="stylesheet">'
    )
    return render_template('signup.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    store = request.form.get('store')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')

    #Simple validation
    if not (username and password and cpassword and email and store):
        flash('Please fill in all fields.................', 'error')
        return redirect(url_for('signup_page'))
    
    #Username already exists
    if users_collection.find_one({'$or': [{'username': username}]}):
        flash('Username already taken. Please choose another one.', 'error')
        return redirect(url_for('signup_page'))
    
    #Password checking
    if(password!=cpassword):
        flash('Password do not match.', 'error')
        return redirect(url_for('signup_page'))

    # Storing data to databse
    user_data = {'username': username, 'email':email , 'password': password , 'store':store}
    users_collection.insert_one(user_data)

    flash('Signup successful!', 'success')
    return redirect(url_for('login_page'))
#------------------------------------------------------------------------------------------------------






#Login Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/login')
def login_page():
    owl_carousel_css_link = (
        '<link rel="stylesheet" '
        'type="text/css" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.1.3/assets/owl.carousel.min.css">'
    )
    font_awesome_css_link = (
        '<link rel="stylesheet" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
    )
    google_fonts_css_link = (
        '<link href="https://fonts.googleapis.com/css?family=Poppins:400,600,700|Roboto:400,700&display=swap" '
        'rel="stylesheet">'
    )
    return render_template('login.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user_data = users_collection.find_one({"username": request.form['username'], "password": request.form['password']})

    # Simple form validation
    if not (username and password):
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('login_page'))

    if user_data:
            # Store user_id in session
            session['user_id'] = str(user_data["_id"])
            return redirect(url_for('home'))
    else:
        flash('Username or password do not match', 'error')
        return render_template('login.html') 
#------------------------------------------------------------------------------------------------------
    





#Image Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/orders')
def orders():
    owl_carousel_css_link = (
        '<link rel="stylesheet" '
        'type="text/css" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.1.3/assets/owl.carousel.min.css">'
    )
    font_awesome_css_link = (
        '<link rel="stylesheet" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
    )
    google_fonts_css_link = (
        '<link href="https://fonts.googleapis.com/css?family=Poppins:400,600,700|Roboto:400,700&display=swap" '
        'rel="stylesheet">'
    )
    if 'user_id' in session:
        # Retrieve photos from the database
        photos_data = images_collection.find()

        grouped_data = {}
        for item in photos_data:
            token = item['token_number']
        if token not in grouped_data:
            grouped_data[token] = []

        # Append image data to the corresponding token
        grouped_data[token].append({'photo': item['photo'], 'token_number': token})

        return render_template('prescription.html', grouped_data=grouped_data,owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
    else:
        return render_template('prescription.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
#-----------------------------------------------------------------------------------------------------
    





# Remove Image
#------------------------------------------------------------------------------------------------------
@app.route('/remove/<photo_id>')
def remove(photo_id):
    # Find the photo by ID in the database
    photo = images_collection.find_one({"_id": ObjectId(photo_id)})

    # Check if the photo exists
    if photo:
        # Delete the photo from the database
        images_collection.delete_one({"_id": ObjectId(photo_id)})
        flash('Photo removed successfully.', 'success')
    else:
        flash('Photo not found.', 'error')

    return redirect(url_for('orders'))
#------------------------------------------------------------------------------------------------------






#Stock Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/stock')
def stock():
    owl_carousel_css_link = (
        '<link rel="stylesheet" '
        'type="text/css" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.1.3/assets/owl.carousel.min.css">'
    )
    font_awesome_css_link = (
        '<link rel="stylesheet" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
    )
    google_fonts_css_link = (
        '<link href="https://fonts.googleapis.com/css?family=Poppins:400,600,700|Roboto:400,700&display=swap" '
        'rel="stylesheet">'
    )
    if 'user_id' in session:
        # Retrieve data from MongoDB
        data = medicine.find({}, {"name": 1, "price": 1})
        # Pass data to HTML template
        return render_template('stock.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link, data=data,logged_in=True)
    else:
        return render_template('home.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
#------------------------------------------------------------------------------------------------------
    





#Order received page Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/order_update')
def order_update():
    owl_carousel_css_link = (
        '<link rel="stylesheet" '
        'type="text/css" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.1.3/assets/owl.carousel.min.css">'
    )
    font_awesome_css_link = (
        '<link rel="stylesheet" '
        'href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
    )
    google_fonts_css_link = (
        '<link href="https://fonts.googleapis.com/css?family=Poppins:400,600,700|Roboto:400,700&display=swap" '
        'rel="stylesheet">'
    )
    if 'user_id' in session:
        data = order_collection.find()
        grouped_data = {}
        grand_totals = {}
        for item in data:
            token = item['token_number']
            if token not in grouped_data:
                grouped_data[token] = []
            grouped_data[token].append(item)
            # Accumulate product_total for the token in grand_totals
            if token in grand_totals:
                grand_totals[token] += item['product_total']
            else:
                grand_totals[token] = item['product_total']
        return render_template('orders.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link,data=data,grouped_data=grouped_data, grand_totals=grand_totals,logged_in=True)
    else:
        return render_template('orders.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
#------------------------------------------------------------------------------------------------------
    





#Add medicine  Page->
#------------------------------------------------------------------------------------------------------
@app.route('/med', methods=['POST'])
def med():
    name = request.form.get('name')
    price = int(request.form.get('price'))

    if not (name and price):
        flash('Please enter all the details.', 'error')
        return redirect(url_for('home'))

    # Store data in MongoDB
    data_to_insert = {"name": name, "price": price}
    medicine.insert_one(data_to_insert)

    flash('Medicine Added!', 'success')
    return redirect(url_for('home'))
#------------------------------------------------------------------------------------------------------






#Remove medicine Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/remove_medicine', methods=['POST'])
def remove_data():
    data_id = request.form.get('id')  # Assuming you're using a form with a hidden input for ID
    medicine.delete_one({"_id": ObjectId(data_id)})
    return redirect(url_for('stock'))
#------------------------------------------------------------------------------------------------------







#Logout Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    if 'user_id' in session:
        # Clear the session data
        session.clear()
        return redirect(url_for('login'))
    else:
        return render_template('login')
#------------------------------------------------------------------------------------------------------
    




    
#------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
#------------------------------------------------------------------------------------------------------