from flask import Flask, jsonify, request, render_template, make_response, redirect, url_for
import json
import subprocess
import jwt
import datetime

app=Flask(__name__)
SECRET_KEY="test" #change this


USER_CREDENTIALS={
    "test_user":"test_password"
} #change these

@app.route("/")
def home():
    commands={"add_command":"This will add a new command with the specified alias in the json file"}
    commands["remove_command"]="This will remove command with the specified alias in the json file"
    commands["modify_command"]="This will add a new command with the specified alias in the json file"
    commands["execute_command_by_alias"]="This will execute a shell command on, known under an alias in the json file the system"
    commands["execute_costume_command"]="This will execute a user given shell command on the system"
    return jsonify(commands)

@app.route("/login", methods=["POST"])
def login():
    '''
    Simple login function

    Parameters (in the request body):
        - username: str
        - password: str 
    '''
    data = request.get_json()

    if "username" not in data or "password" not in data:
        return jsonify({"message": "Malformed request, 'username' and 'password' are required."}), 400

    username = data.get("username")
    password = data.get("password")

    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        token = jwt.encode({
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        response = make_response(redirect(url_for("get_list")))
        response.set_cookie("auth", token, httponly=True)
        return response
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route("/list_commands")
def get_list():
    '''
    This will return the list of commands already saved in the json file

    Parameters: None
    '''
    auth_cookie = request.cookies.get("auth")
    if not auth_cookie:
        return redirect(url_for("login"))
    
    try:
        with open("commands.json","r") as fd:
            commands_list=json.load(fd)

    except FileNotFoundError:
        with open("commands.json","w") as fd:
            commands_list={}
            json.dump(commands_list,fd,indent=2)
    finally:
        return jsonify(commands_list)

@app.route("/add_command",methods=["POST"])
def add_command():
    '''
    This will add a new command with the specified alias in the json file

    Parameters (in the request body):
        - alias: str
        - command: str 
    '''
    auth_cookie = request.cookies.get("auth")
    if not auth_cookie:
        return redirect(url_for("login"))
    
    if request.method=="POST":
        data=request.get_json()
    else:
        return jsonify({"message":"Method not allowed"})
    
    if data.get('alias'):
        alias=data['alias']
    else:
        return jsonify({"message":"Malformed body, missing alias"})

    if data.get('command'):
        command=data['command']
    else:
        return jsonify({"message":"Malformed body, missing command"})

        #add command to json file
    with open("commands.json","r") as fd:
        commands_list=json.load(fd)
    
    if not commands_list.get(alias):
        if "sudo" in command:
            return jsonify({"message":"System will not execute commands as root"})
        
        commands_list[alias]=command
        with open("commands.json",'w') as fd:
            json.dump(commands_list,fd,indent=2)
    else:
        return jsonify({"message":f"Alias is already used for {commands_list[alias]}"})

    return jsonify({"message":"Success"})

@app.route("/remove_command",methods=["PUT"])
def remove_command():
    '''
    This will remove command with the specified alias in the json file

    Parameters (in the request body):
        - alias: str
    '''
    auth_cookie = request.cookies.get("auth")
    if not auth_cookie:
        return redirect(url_for("login"))
    
    if request.method=="PUT":
        data=request.get_json()
    else:
        return jsonify({"message":"Method not allowed"})
    
    if data.get('alias'):
        alias=data['alias']
    else:
        return jsonify({"message":"Malformed body, missing alias"})
    
    with open("commands.json","r") as fd:
        commands_list=json.load(fd)

    if commands_list.get(alias):
        commands_list.pop(alias)
        with open("commands.json",'w') as fd:
            json.dump(commands_list,fd,indent=2)
    else:
        return jsonify({"message":f"Alias \"{alias}\" was not found "})

    return jsonify({"message":"Success"})


@app.route("/modify_command",methods=["PUT"])
def modify_command():
    '''
    This will add a new command with the specified alias in the json file

    Parameters (in the request body):
        - old_alias: str
        - new_alias: str
        - command: str
    '''
    auth_cookie = request.cookies.get("auth")
    if not auth_cookie:
        return redirect(url_for("login"))
    
    if request.method=="PUT":
        data=request.get_json()
    else:
        return jsonify({"message":"Method not allowed"})

    if data.get('old_alias'):
        old_alias=data['old_alias']
    else:
        return jsonify({"message":"Malformed body, missing old_alias"})

    if data.get('new_alias'):
        new_alias=data['new_alias']
    else:
        return jsonify({"message":"Malformed body, missing new_alias"})

    if data.get('command'):
        command=data['command']
    else:
        return jsonify({"message":"Malformed body, missing command"})
    
    with open("commands.json","r") as fd:
        commands_list=json.load(fd)

    if not commands_list.get(old_alias):
        return jsonify({"message":f"Old alias \"{old_alias}\" was not found"})

    if commands_list.get(new_alias):
        return jsonify({"message":f"New alias \"{new_alias}\" is already in use"})

    commands_list.pop(old_alias)

    if "sudo" in command:
        return jsonify({"message":"System will not execute commands as root"})
    
    commands_list[new_alias]=command
    
    with open("commands.json",'w') as fd:
            json.dump(commands_list,fd,indent=2)

    return jsonify({"message":"Success"})

@app.route("/execute_costume_command",methods=["POST"])
def execute_costume_command():
    '''
    This will execute a user given shell command on the system

    Parameters (in the request body):
        - command: str
    '''
    auth_cookie = request.cookies.get("auth")
    if not auth_cookie:
        return redirect(url_for("login"))
    
    if request.method=="POST":
        data=request.get_json()
    else:
        return jsonify({"message":"Method not allowed"})

    if data.get("command"):
        command=data['command']
    else:
        return jsonify({"message":"Malformed body, missing command"})

    if "sudo" in command:
        return jsonify({"message":"System will not execute commands as root"})

    subprocess.Popen(command.split(' '))

    return jsonify({"message":"Success"})

@app.route("/execute_command_by_alias",methods=["POST"])
def execute_command_by_alias():
    '''
    This will execute a shell command on, known under an alias in the json file the system

    Parameters (in the request body):
        - alias: str
    '''
    auth_cookie = request.cookies.get("auth")
    if not auth_cookie:
        return redirect(url_for("login"))
    
    if request.method=="POST":
        data=request.get_json()
    else:
        return jsonify({"message":"Method not allowed"})

    if data.get("alias"):
        alias=data['alias']
    else:
        return jsonify({"message":"Malformed body, missing command"})

    with open("commands.json","r") as fd:
        commands_list=json.load(fd)

    if commands_list.get(alias):
        command=commands_list[alias]
    else:
        return jsonify({"message":f"Alias \"{alias}\" was not found"})
    
    subprocess.Popen(command.split(' '))

    return jsonify({"message":"Success"})

if __name__=="__main__":
    app.run(debug=True)