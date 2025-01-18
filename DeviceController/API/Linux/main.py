from flask import Flask, request, jsonify
import json

app=Flask(__name__)

@app.route("/")
def home():
    return "Home"

@app.route("/list")
def get_list():
    try:
        with open("commands.json","r") as fd:
            commands_list=json.load(fd)

    except FileNotFoundError:
        with open("commands.json","w") as fd:
            commands_list={}
            json.dump(commands_list,fd,indent=2)
    finally:
        return jsonify(commands_list)
    

if __name__=="__main__":
    app.run(debug=True)