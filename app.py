from flask import render_template,url_for,Flask,request
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt as pyjwt
import datetime

app = Flask(__name__)


@app.route('/')
def home():

    return render_template('Home.html')
@app.route('/about-tool')
def about_tool():
    return render_template('about-tool.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')

api = Api(app)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/abdal/OneDrive/Desktop/intel-Classfier-main/diseaseinfoo.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

# Register Arguments
register_user_args = reqparse.RequestParser()
register_user_args.add_argument('firstname', type=str, required=True)
register_user_args.add_argument('lastname', type=str, required=True)
register_user_args.add_argument('phonenumber', type=str, required=True)
register_user_args.add_argument('gender', type=str, required=True)
register_user_args.add_argument('date', type=str, required=True)
register_user_args.add_argument('username', type=str, help="username required", required=True)
register_user_args.add_argument('email', type=str, help="email required", required=True)
register_user_args.add_argument('password', type=str, required=True)

# # #Login Arguments
login_user_args = reqparse.RequestParser()
login_user_args.add_argument('username', type=str, help="username required", required=True)
login_user_args.add_argument('password', type=str, required=True)

# Token Arguments
token_args = reqparse.RequestParser()
token_args.add_argument('token', type=str, required=True)




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    phonenumber = db.Column(db.String(10), unique=True)
    gender = db.Column(db.String(8), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)


class Test(db.Model):
    test_id = db.Column(db.Integer(), primary_key=True)
    image = db.Column(db.Text(30), nullable=False)
    result = db.Column(db.Text(30), nullable=False)
    id = db.Column(db.Integer(), db.ForeignKey(User.id))


class Token(db.Model):
    Token_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text(1000), nullable=False)
    isdeleted = db.Column(db.Boolean(), nullable=False)


# Token.token.alter(type=String)

user_resource_field = {
    "id": fields.Integer,
    "firstname": fields.String,
    "lastname": fields.String,
    "phonenumber": fields.String,
    "gender": fields.String,
    "date": fields.String,
    "username": fields.String,
    "email": fields.String,
    "password": fields.String

}
token_resource_field = {
    "Token_id": fields.Integer,
    "token": fields.String,
    "isdeleted": fields.Boolean,

}

##############################################################################################################
import jwt

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

    # use the retrieved values to create a new user and add it to the database
    hashed_password = generate_password_hash(password, method='sha256')
    user = User(firstname=firstname, lastname=lastname, phonenumber=phonenumber, gender=gender, date=date,
                username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    # generate a JWT token for the newly registered user
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    decodedtoken = pyjwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    return make_response(render_template('home-after-register.html'))
#####################################REGISTERRRRRRRRR###############################################################################
class Register(Resource):
    @marshal_with(user_resource_field)
    def put(self):

        args = register_user_args.parse_args()
        username = args['username']
        password = args['password']
        hashed_password = generate_password_hash(password, method='sha256')

        #  Check for blank requests
        if username is None or password is None:
            abort(400, message="OHHH This is Blank request")

        # Check for existing users
        user = User.query.filter_by(username=username).first()
        if user:
            abort(409, message="User already exists. Please Log in.")
        # return  make_response(jsonify({'message':'User already exists. Please Log in..' }), 409)

        user = User(



            firstname=args['firstname'],
            lastname=args['lastname'],
            phonenumber=args['phonenumber'],
            gender=args['gender'],
            date=args['date'],
            username=args['username'],
            email=args['email'],
            password=hashed_password)

        db.session.add(user)
        db.session.commit()
        abort(400, message="User Successfully registered.")

        # return {'username': user.username,'password': user.password}, 201
        # return user.username,user.password
################################################################################################
@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return 'Invalid login credentials'

    # generate a JWT token for the authenticated user
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }

    usertoken = pyjwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])


    # save the token to the database
    tokeninstance = Token(
        token=usertoken,
        isdeleted=False
    )
    db.session.add(tokeninstance)
    db.session.commit()

    # return the token to the client
    decodedtoken = pyjwt.decode(usertoken, app.config['SECRET_KEY'], algorithms=['HS256'])
    return make_response(render_template('home-after-register.html'))
####################################################################################################
class Login(Resource):
    #   @marshal_with(token_resource_field)
    def post(self):

        args = login_user_args.parse_args()
        username = args['username']
        password = args['password']
        # print("uuuuuuuuuuuuuuuuuuu",username,password)
        user = User.query.filter_by(username=username).first()
        # print("USERRRRRRRRRRRR:",user.password,password)

        if not user:
            return make_response(jsonify({'message ': 'Could not verify, Login is required'}), 401)
        if check_password_hash(user.password, password):
            usertoken = pyjwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                   app.config['SECRET_KEY'])
            decodedtoken = pyjwt.decode(usertoken, app.config['SECRET_KEY'], algorithms=["HS256"])

            # token_id=args['username']
            # tokeninstance=Token.query.filter(token_id).first()

            tokeninstance = Token(
                token=usertoken,
                isdeleted=False
            )
            db.session.add(tokeninstance)
            db.session.commit()
            # print("////////////////////////////////////",tokeninstance.token)
            # print("////////////////////////////////////",tokeninstance.isdeleted)
            # print("////////////////////////////////////",tokeninstance.Token_id)
            # print("////////////////////////////////////////////", type(tokeninstance))
            # print("////////////////////////////////////////////", type(decodedtoken))
            # print("////////////////////////////////////////////", decodedtoken["id"])

            return make_response(jsonify({'token': decodedtoken}))
        #     return make_response(jsonify({'message':'Succesful login'}))

        # else :
        #      return make_response(jsonify({'message ':'Could not verify, Login is required' }), 401)


class Logout(Resource):
    def post(self):
        args = token_args.parse_args()
        giventoken = args['token']
        print("Here My Given Token  =  ", giventoken)
        # decodedtoken = jwt.decode(giventoken,app.config['SECRET_KEY'], algorithms=["HS256"])
        # tokenid=decodedtoken["id"]
        # tokeninstance = Token.query.get(tokenid)
        tokeninstance = Token.query.filter_by(token=giventoken).first()

        if not tokeninstance:
            return make_response(jsonify({'message ': 'Could not verify Token'}), 401)

        tokeninstance.isdeleted = True
        print("Token is deleted or not ", tokeninstance.isdeleted)
        return make_response(jsonify({'message ': 'Succesful logout'}))


# # For GET request to http://localhost:5000/
class GetUser(Resource):
    def get(self):
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {'id': user.id, 'firstname': user.firstname, 'lastname': user.lastname, 'gender': user.gender,
                         'phonenumber': user.phonenumber, 'date': user.date,
                         'username': user.username,
                         'email': user.email,
                         'password': user.password
                         }
            user_list.append(user_data)
        return {"Users": user_list}, 200


class GetOneUser(Resource):
    def get(self, id):
        user = User.query.get(id)

        if not user:
            return jsonify({'message': 'User not found'})

        user_data = {'id': user.id, 'firstname': user.firstname, 'lastname': user.lastname, 'gender': user.gender,
                     'phonenumber': user.phonenumber, 'date': user.date,
                     'username': user.username,
                     'email': user.email,
                     'password': user.password
                     }
        return jsonify({'User': user_data})


# # For put request to http://localhost:5000/update/?
class UpdateUser(Resource):
    def put(self, id):
        # user=User.query.get(id)
        user = User.query.filter_by(id=id).first()
        print('///////////////////////////////////////////////////////////////////////////////////', user.id)
        if user:
            args = register_user_args.parse_args()
            user.firstname = args.get('firstname'),
            print("//////////////////////////Update user/////////////////////", user.firstname)
            user.lastname = args.get('lastname'),
            print("//////////////////////////Update user/////////////////////", user.lastname)
            user.phonenumber = args.get('phonenumber'),
            print("//////////////////////////Update user/////////////////////", user.phonenumber)
            user.gender = args.get('gender'),
            print("//////////////////////////Update user/////////////////////", user.gender)
            user.date = args.get('date'),
            print("//////////////////////////Update user/////////////////////", user.date)
            user.username = args.get('username'),
            print("//////////////////////////Update user/////////////////////", user.username)
            user.email = args.get('email'),
            print("//////////////////////////Update user/////////////////////", user.email)
            user.password = args.get('password')
            print("//////////////////////////Update user/////////////////////", user.password)
            db.session.commit()
            return 'Updated', 200
        else:
            return {'error': 'not found'}, 404

        # # # # For delete request to http://localhost:5000/delete/?


# class DeleteUser(Resource):
#     def delete (self, id):
#         #  user=User.query.filter_by(id==id).first()
#         user = User.query.get(id)
#         print ("THis is idddddddddddddddddd", id)
#         if user is None:
#             return {'error': 'not found'}, 404
#         db.session.delete(user)
#         db.session.commit()
#         return f'{id} is deleted', 200


class DeleteToken(Resource):
    def delete(self, Token_id):
        #  user=User.query.filter_by(id==id).first()
        tok = Token.query.get(Token_id)
        if tok is None:
            return {'error': 'not found'}, 404
        db.session.delete(tok)
        db.session.commit()
        return f'{Token_id} is deleted', 200


api.add_resource(GetUser, '/')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

# api.add_resource(GetOneUser, '/get/<int:id>')
# api.add_resource(UpdateUser, '/update/<int:id>')
api.add_resource(DeleteToken, '/delete/<int:Token_id>')

if __name__ == '__main__':
    app.run(debug=True)
