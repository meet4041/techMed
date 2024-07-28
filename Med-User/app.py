from pymongo import MongoClient
from flask import Flask, redirect, url_for, flash,session,render_template, request
from flask_login import LoginManager, UserMixin
from bson import ObjectId
import random
import base64
from flask_login import logout_user


app = Flask(__name__ , template_folder='templates')
app.secret_key = 'your_secret_key' 
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Connection to MongoDB 
#------------------------------------------------------------------------------------------------------
client = MongoClient('mongodb://localhost:27017')
db = client.root  
users_collection = db.user_signup 
contact_info = db.contact_to_chemist
add_medicine = db.add_medicine
images = db.photos
med_add = db.add_to_cart
med_add_1 = db.order_of_user
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
        cart_count = med_add.count_documents({})
        cart_items = med_add.find()
        return render_template('home.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link,cart_count=cart_count, cart_items=cart_items,logged_in=True)
    else:
        return render_template('login.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
#------------------------------------------------------------------------------------------------------
    





#Signup Page->
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
    cont = request.form.get('cont')
    email = request.form.get('email')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')

    #Simple validation
    if not (username and email and password and cpassword and cont):
        flash('Please fill in all fields.', 'error')
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
    user_data = {'username': username, 'contact':cont, 'email': email, 'password': password }
    users_collection.insert_one(user_data)

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
    if 'user_id' in session:
        return render_template('login.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
    else:
        return render_template('login.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
    

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user_data = users_collection.find_one({"username": request.form['username'], "password": request.form['password']})
    print(username)

    # Simple form validation
    if not (username and password):
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('login_page'))

    # Save the username to the session
    if user_data:
            # Store user_id in session
            session['user_id'] = str(user_data["_id"])
            # session['username'] = str(user_data["username"])
            session['user_name'] = username
            return redirect(url_for('home'))
    else:
        flash('Username or password do not match', 'error')
        return render_template('login.html') 
#-----------------------------------------------------------------------------------------------------
    





#About Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/about')
def about():
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
        cart_count = med_add.count_documents({})
        cart_items = med_add.find()
        return render_template('about.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link,cart_count=cart_count, cart_items=cart_items,logged_in=True)
    else:
        return render_template('about.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
#----------------------------------------------------------------------------------------------------- 
    





#Contact Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/contact')
def contact_page():
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
        cart_count = med_add.count_documents({})
        cart_items = med_add.find()
        return render_template('contact.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link,cart_count=cart_count, cart_items=cart_items,logged_in=True)
    else:
        return render_template('contact.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
    
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    num = request.form.get('num')
    email = request.form.get('email')
    message = request.form.get('message')

    if not (name and email and message and num):
        flash('Please fill in all fields*', 'error')
        return redirect(url_for('contact'))

    # Storing data to databse
    user_data = {'name': name, 'number' : num ,'email': email, 'message': message }
    contact_info.insert_one(user_data)

    flash('Message Sent!', 'success')
    return redirect(url_for('contact_page'))
#------------------------------------------------------------------------------------------------------





#Buy Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/buy')
def buy():
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
        data = add_medicine.find({}, {"name": 1, "price": 1})
        cart_count = med_add.count_documents({})
        cart_items = med_add.find()

        return render_template('buy.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link, data=data,cart_count=cart_count, cart_items=cart_items,logged_in=True)
    else:
        return render_template('login.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
#------------------------------------------------------------------------------------------------------
    




#Buy medicine(add to cart) Page->
#-----------------------------------------------------------------------------------------------------
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():

    product_id = request.form.get('product_id')
    product_name = request.form.get('product_name')
    product_price = int(request.form.get('product_price'))
    quantity = int(request.form.get('qua'))

    # Convert product_id to ObjectId
    product_id = ObjectId(product_id)

    # Perform database operation to add to cart
    # (Assuming you have a 'cart' collection in your database)
    cart_item = {
        'product_id': product_id,
        'product_name': product_name,
        'product_price': product_price,
        'quantity': quantity
    }
    med_add.insert_one(cart_item)
    flash('Added to cart', 'success')

    return redirect('/buy')
#-----------------------------------------------------------------------------------------------------





#Remove medicine Page (add to cart->
#------------------------------------------------------------------------------------------------------
@app.route('/remove_medicine', methods=['POST'])
def remove_data():
    data_id = request.form.get('id')  # Assuming you're using a form with a hidden input for ID
    med_add.delete_one({"_id": ObjectId(data_id)})
    return redirect('/cart')
#------------------------------------------------------------------------------------------------------






#Upload Page ->
#-----------------------------------------------------------------------------------------------------
@app.route('/upload')
def upload_page():
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
        return render_template('upload.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link,logged_in=True)
    else:
        return render_template('login.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
    
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the uploaded files
        photo_files = request.files.getlist('photos')

        # Iterate through each uploaded file
        for idx, photo_file in enumerate(photo_files):
            # Check if the file name is empty
            if photo_file.filename == '':
                flash(f'No selected file for file #{idx + 1}', 'error')
                continue

            # Save each file temporarily or process it as needed
            temp_path = f'photo_{idx + 1}.png'
            photo_file.save(temp_path)
            random_number = random.randint(1, 100000)
            
            # Convert image to binary data
            binary_data = base64.b64encode(open(temp_path, 'rb').read())
            order_detail = {
                "photo": binary_data.decode('utf-8'),
                'token_number' : random_number #rand
            }

            # Store the binary data in MongoDB
            images.insert_one(order_detail)
            
            flash(f'Photo {idx + 1} uploaded successfully.', 'success')

        return redirect(url_for('upload_page'))
#-----------------------------------------------------------------------------------------------------
    





# Cart page ->
#-----------------------------------------------------------------------------------------------------
@app.route('/cart')
def cart():
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
        data = med_add.find({}, {"product_name": 1, "product_price": 1, "quantity":1})
        cart_count = med_add.count_documents({})
        cart_items = med_add.find()   
             
        return render_template('cart.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link, data=data,cart_count=cart_count, cart_items=cart_items,logged_in=True)
    else:
        return render_template('login.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
#-----------------------------------------------------------------------------------------------------
    





#Place Order Page ->
#-----------------------------------------------------------------------------------------------------
@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
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
        if request.method == 'POST':
            cart_items = list(med_add.find())
            customer_id = session['user_id']
            product_id = request.form.get('product_id')
            random_number = random.randint(1, 100000)

            # Convert product_id to ObjectId
            product_id = ObjectId(product_id)

            # Iterate through each item and store in orders
            for item in cart_items:
                grand_total = sum(item['product_price'] * item['quantity'] for item in cart_items)
                total = (item['product_price']*item['quantity'])
                
                order_detail = {
                    'user_id' :customer_id,  #ID
                    # 'customer_name' :customer_name, #a #a
                    'product_id': item['product_id'], #ID 
                    'product_name': item['product_name'], #Dolo $Dolo
                    'product_price': item['product_price'], #25 #25
                    'product_quantity': item['quantity'], #2 #1
                    'product_total': total, #50 #25
                    'grand_sum' : grand_total, #75
                    'token_number' : random_number #rand
                }

                a = {
                'product_id': product_id,
                }
                med_add_1.insert_one(order_detail)

                # Clear the cart after placing the order
                session.pop('cart',None)

            return render_template('placeorder.html',product_id=product_id,random_number=random_number,grand_total=grand_total,owl_carousel_css_link=owl_carousel_css_link, font_awesome_css_link=font_awesome_css_link, google_fonts_css_link=google_fonts_css_link, logged_in=True)
        else:
            return render_template('login.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link)
#-----------------------------------------------------------------------------------------------------






#Logout Page ->
#-----------------------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    if 'user_id' in session:
        logout_user()
        session.pop('user_id', None)
        return redirect(url_for('login'))
    else:
        return render_template('login')
#-----------------------------------------------------------------------------------------------------
    



#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
#-----------------------------------------------------------------------------------------------------