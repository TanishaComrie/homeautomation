"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

# from crypt import methods
import site 

from app import app, Config,  mongo, Mqtt
from flask import escape, render_template, request, jsonify, send_file, redirect, make_response, send_from_directory 
from json import dumps, loads 
from werkzeug.utils import secure_filename
from datetime import datetime,timedelta, timezone
from os import getcwd
from os.path import join, exists
from time import time, ctime
from math import floor
 



#####################################
#   Routing for your application    #
#####################################


# 1. CREATE ROUTE FOR '/api/set/combination'
    
# 2. CREATE ROUTE FOR '/api/check/combination'

# 3. CREATE ROUTE FOR '/api/update'
   
# 4. CREATE ROUTE FOR '/api/reserve/<start>/<end>'

# 5. CREATE ROUTE FOR '/api/avg/<start>/<end>'

@app.route('/api/set/combination',methods=['POST'])
def set_passcode(code):
    if request.method == "POST":
        try:
            item=mongo.setPasscode(code)
            if item:
                return jsonify({"status":"complete","data":"complete"})
        except Exception as e:
            msg=str(e)
            print (f'set_passcode error: f{msg}')
    return jsonify({"status":"failed","data":"failed"})

@app.route('/api/check/combination',methods=['POST'])
def check_passcode():
    '''Checks if the passcode is correct'''
    if request.method == "POST":
        try:
            form = request.form
            passcode = form.get('passcode')
            if passcode:
                result = mongo.passcodes(passcode)
                if result != 0:
                    return jsonify({"status":"success","data":"complete"})
        except Exception as e:
            print(f"check_passcode() error: {e}")
        
        return jsonify({"status":"failed","data":"failed"})
    
@app.route('/api/update',methods=['POST'])
def update():
    if request.method== "POST":
        try:
            jsonDoc = request.get_json()
            timestamp= floor(datetime.now().timestamp())
            jsonDoc['timestamp'] = timestamp

            Mqtt.publish("620156117",mongo.dumps(jsonDoc))
            Mqtt.publish("620156117_pub",mongo.dumps(jsonDoc))
            print(f'MQTT:'(jsonDoc))

            data=mongo.insertData(jsonDoc)
            if data:
                return jsonify({"status":"complete","data":"complete"})
        except Exception as e:
            msg=str(e)
            print(f'update() error:{msg}')
    return jsonify({"status":"failed","data":"failed"})


@app.route('/api/reserve/<start>/<end>/<filename>',methods=['GET'])
def get_radar(start,end):
    if request.method =="GET":
        try:
            start = int(start)
            end= int(end)
            radar = list(mongo.get_radar(start,end))
            if radar:
                return jsonify({"status":"found","data": radar})
        except Exception as e:
            msg=str(e)
            print(f'get_radar() error:{msg}')
    return jsonify({"status":"failed","data": 0})

@app.route('/api/avg/<start>/<end>/<filename>',methods=['GET'])
def average(start,end):
    if request.method == "GET":
        try:
            start=int(start)
            end=int(end)
            avg=list(mongo.average(start,end))
            if avg:
                return jsonify({"status":"found","data": avg} )
        except Exception as e:
            msg=str(e)
            print(f'average() error:{msg}')
    return jsonify({"status":"failed","data": 0})



@app.route('/api/file/get/<filename>', methods=['GET']) 
def get_images(filename):   
    '''Returns requested file from uploads folder'''
   
    if request.method == "GET":
        directory   = join( getcwd(), Config.UPLOADS_FOLDER) 
        filePath    = join( getcwd(), Config.UPLOADS_FOLDER, filename) 

        # RETURN FILE IF IT EXISTS IN FOLDER
        if exists(filePath):        
            return send_from_directory(directory, filename)
        
        # FILE DOES NOT EXIST
        return jsonify({"status":"file not found"}), 404


@app.route('/api/file/upload',methods=["POST"])  
def upload():
    '''Saves a file to the uploads folder'''
    
    if request.method == "POST": 
        file     = request.files['file']
        filename = secure_filename(file.filename)
        file.save(join(getcwd(),Config.UPLOADS_FOLDER , filename))
        return jsonify({"status":"File upload successful", "filename":f"{filename}" })

 


###############################################################
# The functions below should be applicable to all Flask apps. #
###############################################################


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(405)
def page_not_found(error):
    """Custom 404 page."""    
    return jsonify({"status": 404}), 404



