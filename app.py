from flask import render_template,url_for,Flask,request,Flask, jsonify, make_response, request,redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt as pyjwt
from flask_login import LoginManager,current_user,login_user,UserMixin,login_required
import datetime
from flask_migrate import Migrate
from keras.models import load_model
from PIL import Image
import base64
import numpy as np
import joblib
import pandas as pd
import numpy as np
app = Flask(__name__)

global auth
auth=False
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/abdal/OneDrive/Desktop/intel-Classfier-main/diseaseinfoo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    if id is not None and id != 'None':
        return User.query.get(int(id))
    else:
        return None

@app.route('/')
def home():

    return render_template('Home.html')


@app.route('/home_after_register')
def home_after_register():

    return render_template('home-after-register.html',user=current_user)

@app.route('/voice_test')
def voice_test():

    return render_template('test2.html',user=current_user)


@app.route('/home_after_register_image')
def home_after_register_image():

    return render_template('nav-after-register.html',user=current_user)




class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    phonenumber = db.Column(db.String(10), unique=True)
    gender = db.Column(db.String(8), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)
    Test = db.relationship('Test', backref='owned_User', lazy=True)

class Test(db.Model):
    __tablename__ = 'test'
    test_id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.Text(30), nullable=False)
    result = db.Column(db.Text(30), nullable=False)
    id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('tests', lazy=True, cascade='all, delete-orphan'))

class voice_test(db.Model):
    __tablename__ = 'voice_test'
    test_id = db.Column(db.Integer, primary_key=True)
    MDVP_FO = db.Column(db.String(1000), nullable=False)
    MDVP_FHI = db.Column(db.String(1000), nullable=False)
    MDVP_FLO = db.Column(db.String(1000), nullable=False)
    MDVP_JITTER = db.Column(db.String(1000), nullable=False)
    MDVP_JITTER_precent = db.Column(db.String(1000), nullable=False)
    MDVP_RAP = db.Column(db.String(1000), nullable=False)
    MDVP_PPQ = db.Column(db.String(1000), nullable=False)
    jitter_DDP = db.Column(db.String(1000), nullable=False)
    MDVP_shimmer = db.Column(db.String(1000), nullable=False)
    MDVP_shimmer_db = db.Column(db.String(1000), nullable=False)
    shimmer_APQ3 = db.Column(db.String(1000), nullable=False)
    shimmer_APQ5 = db.Column(db.String(1000), nullable=False)
    shimmer_APQ11 = db.Column(db.String(1000), nullable=False)
    shimmer_DDA = db.Column(db.String(1000), nullable=False)
    shimmer_NHR = db.Column(db.String(1000), nullable=False)
    HNR = db.Column(db.String(1000), nullable=False)
    RBDE = db.Column(db.String(1000), nullable=False)
    DFA = db.Column(db.String(1000), nullable=False)
    Spread1 = db.Column(db.String(1000), nullable=False)
    Spread2 = db.Column(db.String(1000), nullable=False)
    D2 = db.Column(db.String(1000), nullable=False)
    PPE = db.Column(db.String(1000), nullable=False)
    result = db.Column(db.String(40), default=None)
    id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<voice_test %r>' % self.test_id

class Token(db.Model):
        __tablename__ = 'token'

        Token_id = db.Column(db.Integer, primary_key=True)
        token = db.Column(db.Text(1000), nullable=False)
        isdeleted = db.Column(db.Boolean(), nullable=False)
        id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_token_user_id'))






import jwt
from sqlalchemy.exc import IntegrityError  # import IntegrityError
@app.route('/register', methods=['POST'])
def register_user():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phonenumber = request.form['phonenumber']
    gender = request.form['gender']
    date = request.form['date']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    try:
        # use the retrieved values to create a new user and add it to the database
        hashed_password = generate_password_hash(password, method='scrypt')
        usernew = User(firstname=firstname, lastname=lastname, phonenumber=phonenumber, gender=gender, date=date,
                    username=username, email=email, password=hashed_password)
        login_user(usernew,remember=True)
        db.create_all()
        db.session.add(usernew)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        error_message = 'An account with that email address already exists. Please use a different email address.'
        return render_template('Home.html', error_message=error_message)

    # generate a JWT token for the newly registered user
    payload = {
        'id': usernew.id,
        'username': usernew.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    global auth

    auth = True

    return render_template('home-after-register.html', auth=auth,usernew=current_user)
#####################################REGISTERRRRRRRRR###############################################################################

################################################################################################
import jwt

@app.route('/login', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return make_response(render_template('Home.html', error='*Invalid login username or password'))

    # generate a JWT token for the authenticated user
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    # save the token to the database
    tokeninstance = Token(
        token=token,
        isdeleted=False,
        id=user.id
    )
    login_user(user, remember=True)
    db.session.add(tokeninstance)
    db.session.commit()
    global auth
    auth=True
    # return the token to the client
    return make_response(render_template('home-after-register.html', auth=auth,user=current_user,token=tokeninstance))
from functools import wraps
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data['id']
            user = User.query.get(user_id)
            if not user:
                raise Exception('User not found')
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(user, *args, **kwargs)
    return decorated


####################################################################################################


@app.route('/logoutt')
@login_required
def logoutt():
    # get the token from the request headers or query parameters
    giventoken = request.headers.get('Authorization') or request.args.get('token')

    # find the token instance in the database and delete it
    tokeninstance = Token.query.filter_by(token=giventoken).first()
    if tokeninstance:
        db.session.delete(tokeninstance)
        db.session.commit()

    # set the value of auth to False when the user logs out
    global auth
    auth = False

    # return a response indicating that the logout was successful
    return make_response(render_template('Home.html',auth = auth))


@app.route('/contact')
def contact():
    return render_template('contact.html',auth=auth)
@app.route('/about-tool')
def about_tool():
    return render_template('about-tool.html',auth=auth)

#########################################Deployment#################################################################

def preprossing(image):
    image=Image.open(image)
    image = image.resize((224, 224))
    image_arr = np.array(image.convert('RGB'))
    image_arr.shape = (1, 224, 224, 3)
    return image_arr

classes = ['Healthy','Parkinson']
model1=load_model("weights_best.hdf5")

def predict(image):
    image_arr= preprossing(image)
    print("Image preprocessed")
    result = model1.predict(image_arr)
    print("Prediction result:", result)
    ind = np.argmax(result)
    prediction = classes[ind]
    print("Prediction:", prediction)
    return prediction



@app.route('/image_test', methods=['GET', 'POST'])
def image_test():

    flag = 'hand-written'
    title = 'Hand-written Test'
    if request.method == 'POST':
        print('in')
        image = request.files['file']

        # result=predict(image)
        # print("res",result)
        new_test = Test(image=image.read(), id=current_user.id)
        db.create_all()
        db.session.add(new_test)
        # db.session.commit()
        result = predict(image)
        new_test.result = result
        # print(new_test.owned_User)
        db.session.commit()
        return redirect(url_for('profile'))



    else:
        print('out')
        return render_template('test.html', user=current_user, title=title, flag=flag)


def predict_voice(MDVP_FO, MDVP_FHI, MDVP_FLO, MDVP_JITTER, MDVP_JITTER_precent, MDVP_RAP, MDVP_PPQ,
                  jitter_DDP, MDVP_shimmer, MDVP_shimmer_db, shimmer_APQ3, shimmer_APQ5, shimmer_APQ11,
                  shimmer_DDA, shimmer_NHR, HNR, RBDE, DFA, Spread1, Spread2, D2, PPE):
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.joblib")
    pca = joblib.load("pca.joblib")
    # Preprocess the input data using the same steps as during training
    input_data = np.array([[MDVP_FO, MDVP_FHI, MDVP_FLO, MDVP_JITTER, MDVP_JITTER_precent, MDVP_RAP, MDVP_PPQ,
                            jitter_DDP, MDVP_shimmer, MDVP_shimmer_db, shimmer_APQ3, shimmer_APQ5, shimmer_APQ11,
                            shimmer_DDA, shimmer_NHR, HNR, RBDE, DFA, Spread1, Spread2, D2, PPE]])
    x_scaled = scaler.transform(input_data)
    x_pca = pca.transform(X=x_scaled)
    # Use the trained model to make predictions on the preprocessed input data
    prediction = model.predict(x_pca)
    ind = np.argmax(prediction)
    prediction = classes[ind]
    print("Prediction:", prediction)
    return prediction


@app.route('/voice_test', methods=['GET', 'POST'])
def voicetest():
    flag = 'voiceTest'
    title = 'Voice-Test'
    if request.method == 'POST':
        # Get the input data from the form
        MDVP_FO = float(request.form["MDVP_FO"])
        MDVP_FHI = float(request.form["MDVP_FHI"])
        MDVP_FLO = float(request.form["MDVP_FLO"])
        MDVP_JITTER = float(request.form["MDVP_JITTER"])
        MDVP_JITTER_precent = float(request.form["MDVP_JITTER_precent"])
        MDVP_RAP = float(request.form["MDVP_RAP"])
        MDVP_PPQ = float(request.form["MDVP_PPQ"])
        jitter_DDP = float(request.form["jitter_DDP"])
        MDVP_shimmer = float(request.form["MDVP_shimmer"])
        MDVP_shimmer_db = float(request.form["MDVP_shimmer_db"])
        shimmer_APQ3 = float(request.form["shimmer_APQ3"])
        shimmer_APQ5 = float(request.form["shimmer_APQ5"])
        shimmer_APQ11 = float(request.form["shimmer_APQ11"])
        shimmer_DDA = float(request.form["shimmer_DDA"])
        shimmer_NHR = float(request.form["shimmer_NHR"])
        HNR = float(request.form["HNR"])
        RBDE = float(request.form["RBDE"])
        DFA = float(request.form["DFA"])
        Spread1 = float(request.form["Spread1"])
        Spread2 = float(request.form["Spread2"])
        D2 = float(request.form["D2"])
        PPE = float(request.form["PPE"])
        new_test = voice_test(MDVP_FO=MDVP_FO, MDVP_FHI=MDVP_FHI, MDVP_FLO=MDVP_FLO, MDVP_JITTER=MDVP_JITTER,
                              MDVP_JITTER_precent=MDVP_JITTER_precent, MDVP_RAP=MDVP_RAP, MDVP_PPQ=MDVP_PPQ,
                              jitter_DDP=jitter_DDP, MDVP_shimmer=MDVP_shimmer, MDVP_shimmer_db=MDVP_shimmer_db
                              , shimmer_APQ3=shimmer_APQ3, shimmer_APQ5=shimmer_APQ5, shimmer_APQ11=shimmer_APQ11,
                              shimmer_DDA=shimmer_DDA, shimmer_NHR=shimmer_NHR, HNR=HNR, RBDE=RBDE, DFA=DFA
                              , Spread1=Spread1, Spread2=Spread2, D2=D2, PPE=PPE, id=current_user.id)
        db.create_all()
        db.session.add(new_test)
        result = predict_voice(MDVP_FO, MDVP_FHI, MDVP_FLO, MDVP_JITTER, MDVP_JITTER_precent, MDVP_RAP, MDVP_PPQ,
                               jitter_DDP, MDVP_shimmer, MDVP_shimmer_db, shimmer_APQ3, shimmer_APQ5, shimmer_APQ11,
                               shimmer_DDA, shimmer_NHR, HNR, RBDE, DFA, Spread1, Spread2, D2, PPE)
        new_test.result = result
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return render_template('test2.html', user=current_user, title=title, flag=flag)


@app.route('/profile')
@login_required
def profile():
    title='profile'
    flag = 'profile'
    image_results = []
    voice_results = []
    curr_user = User.query.filter_by(id=current_user.id).first()
    imagetests = Test.query.filter_by(id=current_user.id).all()
    voicetests = voice_test.query.filter_by(id=current_user.id).all()
    MDVP_FO = None
    MDVP_JITTER = None
    MDVP_shimmer_db = None
    for test in imagetests:
        byte = base64.b64encode(test.image).decode('utf-8')
        result = test.result
        image_results.append([byte, result])
    for voiceTest in voicetests:
        MDVP_FO = voiceTest.MDVP_FO
        MDVP_JITTER = voiceTest.MDVP_JITTER
        MDVP_shimmer_db = voiceTest.MDVP_shimmer_db
        result2 = voiceTest.result
        voice_results.append([MDVP_FO, MDVP_JITTER, MDVP_shimmer_db, result2])

    return render_template('profile.html', user=current_user, curr_user=curr_user,
                           image_results=image_results, MDVP_FO=MDVP_FO, MDVP_JITTER=MDVP_JITTER,
                           MDVP_shimmer_db=MDVP_shimmer_db, voice_results=voice_results, flag=flag,title=title)
#######################################################################3


if __name__ == '__main__':
    app.run(debug=True)
