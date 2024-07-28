from flask import Flask, render_template,redirect,request,url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__ , template_folder='templates')
app.secret_key = 'your_secret_key' 

# Connection to MongoDB 
#------------------------------------------------------------------------------------------------------
client = MongoClient('mongodb://localhost:27017')
db = client.root  
user_collection = db.user_signup
chemsit_collection = db.chemist_signup
#------------------------------------------------------------------------------------------------------






#User Page ->
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
    data = user_collection.find({}, {"username": 1, "contact": 1,"email":1,"password":1})
    return render_template('home.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link,data=data)
#------------------------------------------------------------------------------------------------------

#Remove user ->
#------------------------------------------------------------------------------------------------------
@app.route('/remove_user', methods=['POST'])
def remove_data():
    data_id = request.form.get('id')  # Assuming you're using a form with a hidden input for ID
    user_collection.delete_one({"_id": ObjectId(data_id)})
    return redirect(url_for('home'))
#------------------------------------------------------------------------------------------------------






#Chemist Page ->
#------------------------------------------------------------------------------------------------------
@app.route('/chemist')
def chemist():
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
    data = chemsit_collection.find({}, {"username": 1, "email": 1,"password":1,"store":1})
    return render_template('chemist.html',owl_carousel_css_link=owl_carousel_css_link,font_awesome_css_link=font_awesome_css_link,google_fonts_css_link=google_fonts_css_link,data=data)
#------------------------------------------------------------------------------------------------------

#Remove chemist ->
#------------------------------------------------------------------------------------------------------
# @app.route('/remove_chemist', methods=['POST'])
# def remove_chemist():
#     data_id = request.form.get('id')  # Assuming you're using a form with a hidden input for ID
#     chemsit_collection.delete_one({"_id": ObjectId(data_id)})
#     return redirect(url_for('chemist'))
#------------------------------------------------------------------------------------------------------






#------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
#------------------------------------------------------------------------------------------------------