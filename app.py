from flask import Flask,render_template,url_for,request,session,jsonify,redirect,make_response,Response
#importing custome functions
from dotenv import load_dotenv
import os
from functions.scrape import *
from functions.check_emo_ton import *
from functions.calculate_age import *
from functions.percentile_keywords import *
from functions.language_accuracy import *
from functions.filter_comments import *
#from functions.app_functions import *
from functions.generate_date_time import *
#from functions.screen_time import *
#from functions.count_pages_duration import *
from functions.tonality_emotion import *
from tracer_app_functions.app_controller import lang_acc_chart,language_accuracy_using_comments2,tonality_emotion_graph_array,screen_time_count,pages_duration,wcloud,language_accuracy_v1,language_accuracy_v2,lang_acc_map,language_accuracy_mobile
import json,hashlib,datetime,uuid
from bson import objectid
import pandas as pd
import numpy as np
from tracer_app_functions.app_db_controller import *
from urllib.parse import urlparse,unquote
#importing two module os and openai
#controllers
from controller.controller import crud_add_child
#model
from model.scraper import Scraper


from flask_pymongo import PyMongo
from datetime import timedelta
from bson.objectid import ObjectId
from bson import json_util
from flask_cors import *
#tonality check NLTK MODULE
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import asyncio

#class Based View Test
from views import all_views
app = Flask(__name__)
app.secret_key = "super secret key"
load_dotenv()
mongo_uri= os.getenv('MONGO_URI')
print(mongo_uri)
app.config['MONGO_URI'] = mongo_uri
app.config['SECRET_KEY']='amit'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(days=7)
mongo = PyMongo(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#register custum function for calculating age in jinja template 
app.jinja_env.filters['calculate_age'] = calculate_age
app.add_url_rule('/home',view_func=all_views.Home_View.as_view('index'))


#admin index template
@app.route('/admin')
async def admin_index():


    load_dotenv()
    mongo_uri= os.getenv('MONGO_URI')
    
    return jsonify('sec_key')
    #return render_template('admin_index.html')

@app.route('/admin_reg',methods=['POST'])
async def admin_register():
    import os
    
    secret_security = os.getenv("ADMIN_SECURITY_CODE")
    print(secret_security)
    print(request.form)
    if request.method == 'POST':
        admin_email = request.form.get('email')
        admin_name = request.form.get('name')
        admin_key = request.form.get('skey')
        admin_pswd=request.form.get('pswd')
        if admin_key == secret_security:
            return jsonify(request.form)
        else:
            return jsonify('invalid key')
    
    return render_template('admin_index.html')



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html',message='invalid Search'), 404

#--------------------------------
#ADD_CHILD
#-------------------------------
@app.route('/')
async def hello_tracer():
    if 'username' in session: # check if username in session or not 
       
        
        #childData with ref of parrents
        #childData = childCollection.find({'ref_id':session['username']})
        
            
            # Run the async function within the event loop
        fetch_data = await fetch_data_using_id(session['username'], 'ref_id')
        #print(fetch_data)
            
            # Close the event loop
        
        c_data = json.loads(json_util.dumps(fetch_data))
        
        
        
        
        #render page 
        return render_template('add-child.html',content=session['username'],childs=c_data)
    else:
         return render_template('indexx.html')

#-------------------------------end of add-child page
#CRUD_OPERATION add-child
#---------------
@app.route('/crud-add-child', methods=['GET', 'POST'])
def crud_add_child_route():
    if request.method == 'POST':
        return crud_add_child()
    return render_template('crud_add_child.html')
     
    
# end-----------
@app.route('/language_accuracy')
async def language_accuracy():
        
        currentCollection = mongo.db.members
        datas = currentCollection.find_one({'u_id': request.args['childID']})
        if 'username' in session:
            fetch_data = await fetch_data_using_id(request.args['childID'],'u_id')
            
            if fetch_data:
                
                data=await lang_acc_map(fetch_data)
            
                return render_template('lang-accuracy.html',grammatical_correctness=json.loads(json_util.dumps(data)))
        else:
            return render_template('indexx.html')
        
@app.route('/language_accuracy_v2',methods=['GET'])
async def language_accuracy_page2():
    # Extract and decode the data from the query parameter
    import urllib
    

   
    if 'username' in session:
        try:
            # Retrieve data from the JSON object
            childID = request.args.get('child_ID')
            startDate_str = request.args.get('startdate')
            endDate_str = request.args.get('endDate')
            
            currentCollection = mongo.db.members
            datas = currentCollection.find_one({'u_id': request.args['child_ID']})
            fetch_data = await fetch_data_using_id(request.args['child_ID'], 'u_id')
            
            if fetch_data:
                data = await lang_acc_map(fetch_data)
                
                # Parse start and end dates from string format
                #start_date = datetime.strptime(startDate_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                #end_date = datetime.strptime(endDate_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                
                # Filter data based on date range
                filtered_data = []

                # Iterate through the list of dictionaries
                for item in data:
                    item_time = str(item.get("time"))
                    
                    # Check if the item's time is within the specified date range
                    if startDate_str <= item_time <= endDate_str:
                        filtered_data.append(item)
                
                # Return the filtered data as a JSON response
                return render_template('lang-accuracy.html',grammatical_correctness=json.loads(json_util.dumps(filtered_data))
                                       ,c_id=childID,
                                       startDate_str=datetime.strptime(startDate_str, '%Y-%m-%dT%H:%M:%S.%f%z'),
                                       endDate_str=datetime.strptime(startDate_str, '%Y-%m-%dT%H:%M:%S.%f%z')
                                       )
            else:
                # Return an appropriate response when fetch_data is not available
                return jsonify({"message": "Data not available"})
        except Exception as e:
            # Handle parsing or other exceptions and return an error response
            print(e)
            return jsonify({"error": "An error occurred"})
    else:
        # Return a response when 'username' is not in the session
        return jsonify({"message": "User not authenticated"})

              
     
        
        
            
        
    

#DASHBOARD Rendering 
#--------------------
@app.route('/dashboard',methods=['GET'])
async def dashboard():
    
    #from functions.ton_and_emo import tonality_emotion_graph_array
    args = request.args
    if 'username' in session:
           
            #print(args)
            #fetch data
            child_id=args['u_id']
           
            
            fetch_data=await fetch_data_using_id(child_id,'u_id')
            all_urls = fetch_data[0]['urls']
            
            if fetch_data:
               # print(len(fetch_data[0]))
                listdata = json.loads(json_util.dumps(fetch_data[0]))
                lang_acc_chart_data=await lang_acc_chart(fetch_data)
               # print(lang_acc_chart_data)
                
                if 'urls' in fetch_data[0] :
                    print('hello')
                    
                    tonality_emotions_checking,screen_Time,total_count_data,wc = await asyncio.gather(
                    #language_accuracy_using_comments2(fetch_data[0]),
                    tonality_emotion_graph_array(fetch_data[0]['keywords'],'dashboard'),
                    screen_time_count(fetch_data[0]),
                    pages_duration(fetch_data[0]),
                    wcloud(fetch_data[0]['keywords'])
                    )
                
                    screenTime_data= json.dumps(screen_Time)
                    data_on=json.dumps(tonality_emotions_checking)
                    total_comments = tonality_emotions_checking[0]['tot_comments']
                    print('line185')
                    #print(grammar_checking)
                    #print(tonality_emotions_checking)
                    
                    #[pages,seconds,comments]
                    total_count_data.append(total_comments)
                
                    return render_template("dashboard.html",dataton=data_on,screenTime=screenTime_data,count_data=json.dumps(total_count_data),
                                            
                                            wordcloud_data=json.loads(json_util.dumps(wc)),
                                            parentId=json.loads(json_util.dumps(session['username'])),
                                            language_accurac=json.loads(json_util.dumps(lang_acc_chart_data)),
                                            all_url=json.loads(json_util.dumps(all_urls)),
                                            child_id=json.dumps(child_id),
                                            cID=args['u_id']
                                            )
                
                else:
                      return render_template("dashboard.html",dataton=json.dumps([]),screenTime=json.dumps([]),count_data=json.dumps([]),
                                            
                                            wordcloud_data=json.dumps([]),
                                            parentId=json.loads(json_util.dumps(session['username'])),
                                            language_accurac=json.dumps([]),
                                            child_id=json.dumps(child_id),
                                            cID=args['u_id']
                                            )
                    
                

                
                                         
            else:
    
                 return render_template("dashboard.html",wordcloud=json.loads(json_util.dumps([])),parentId=json.loads(json_util.dumps(session['username'])),cID=args['u_id'])
    else:
        return render_template('indexx.html')
             
#end-----------------
#FAMILY page render
#--------------------------
@app.route('/family',methods=['GET'])
async def tonality_emotion():
    child_id = request.args.get('child_ID')
    start_date_str = request.args.get('startdate')
    end_date_str = request.args.get('endDate')
    start_datetime = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    end_datetime = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    formatted_startdate = start_datetime.strftime('%m/%d/%Y, %I:%M:%S %p')
    formatted_enddate = end_datetime.strftime('%m/%d/%Y, %I:%M:%S %p')
    # Parse date ranges into datetime objects
    start_date = datetime.strptime(formatted_startdate, '%m/%d/%Y, %I:%M:%S %p')
    end_date = datetime.strptime(formatted_enddate, '%m/%d/%Y, %I:%M:%S %p')
    print(child_id)

    if child_id is None:
        return render_template('404.html')

    else:
        fetch_data = await fetch_data_using_id(child_id, 'u_id')
        
        if 'keywords' in fetch_data[0]:
            data = fetch_data[0]
            family_data = await tonality_emotion_graph_array(data['keywords'], 'family')
           
            family_data_2=[item for item in family_data if start_date <= datetime.strptime(item['date'], '%m/%d/%Y, %I:%M:%S %p') <= end_date]
            
            return render_template('family.html', emo_ton=json.loads(json_util.dumps(family_data_2)), childName=data['name'], username=session['username'])
        else:
            # Handle the case when 'keywords' key is not present in the data dictionary
            return render_template('404.html', message="Data for this child does not contain 'keywords'")

# ...

#end--------------------
#SCREEN TIME page render
#--------------------------
@app.route('/screentime',methods=['GET'])
async def screen_time():
    from pytz import timezone
    child_id = request.args.get('child_ID')
    if child_id is not None:
       
        
        start_date_str = request.args.get('startdate')
        end_date_str = request.args.get('endDate')
       

       
        
        print(child_id)

    

   
        fetch_data = await fetch_data_using_id(child_id, 'u_id')
        url_array = fetch_data[0]['urls']
       
        gmt = timezone('GMT')
       # Parse start_date and end_date using the correct format
        start_datetime = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        end_datetime = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S.%f%z')

# The rest of your code remains the same
# ...


        # Convert the timestamps in the data to datetime objects
        data_filtered = []

        for entry in url_array:
            timestamp = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            
            # Convert the timestamp to the same time zone as the date range
            timestamp = gmt.localize(timestamp)

            # Check if the timestamp is within the date range
            if start_datetime <= timestamp <= end_datetime:
                data_filtered.append(entry)
        data_filtered_2= await fetch_screen_TIME_using_timestamp(data_filtered)
       # return jsonify(data_filtered_2[0])
# Print the filtered data

        
    
        return render_template('screen-time.html',screenTime=json.loads(json_util.dumps(data_filtered_2[0])),childName=child_id)
    else:
        return render_template('404.html', message="Data for this child does not exit")
#end--------------------
#INTREST PAGE RENDER USING URL PARAMS
#-------------------------
@app.route('/interest',methods=['GET'])
def interest_map():
    args = request.args
    encoded_data = request.args.get('data')
    decoded_data = json.loads(encoded_data)
    #return jsonify(decoded_data)
    print('decoded_data[2]')
    comments_list = []
    urls_list = []
   
   
        

    
 
   

   
    nos_vid=0  # Check if the value is an array
    nos_comment=0
    if isinstance(decoded_data[2], list):
                nos_comment = len(decoded_data[2])
                for item in decoded_data[2]:
                    if 'comment' in item:
                        comments_list.append(item['comment'])
                    if 'url' in item:
                        urls_list.append(item['url'])
    else:
                nos_comment = decoded_data[2]
    if isinstance(decoded_data[3], list):
                nos_vid = len(decoded_data[3])
                for item in decoded_data[3]:
                    
                   
                    urls_list.append(item)
    else:
                nos_vid = decoded_data[3]
     
    keyword=decoded_data[0]
    nos_urls=decoded_data[4]
    nos_duration=decoded_data[5]
     
     
    return render_template('interest-map.html',data=[keyword,nos_urls,nos_duration,nos_vid,nos_comment],urls=urls_list,comments=comments_list)
    

#REGISTER PARENTS
@app.route("/register")
def register():
    if 'username' not in session:
        return render_template('indexx.html',r_error="")
    else:
          return redirect(url_for('hello_tracer'))

#user login 
@app.route("/login",methods=['POST','GET'])
def login():
        if request.method=="POST":
            if 'username' not in session:
           
                  print(request.form)
                  session.permanent=True
                  
                  if request.form:
                            login_cred = request.form
                            print(login_cred)
                            email = login_cred['email']
                            password = hashlib.md5(login_cred['pswd'].encode()).hexdigest()
                            #password=login_cred['pswd']
                            currentCollection = mongo.db.parents
                            check = currentCollection.find_one({'email':email,'password':password})
                            if check is not None:
                                    session['username']=check['email']
                                    return redirect(url_for('hello_tracer'))
                                    #return jsonify({'user':check['username']})
                            else:
                                return render_template('indexx.html',error="user not found")
                  else:
                        email = request.json['email']
                        
                        password = hashlib.md5(request.json['password'].encode()).hexdigest()
                        currentCollection = mongo.db.parents
                        check = currentCollection.find_one({'email':email,'password':password})
                        if check is not None:
                                    session['username']=check['email']
                                    return jsonify({'username':check['username']})
                        else:
                              return jsonify({'user':'not found'}),404
                              

                                
                    #if input hidden field name not match than it is api call
                  
                        
                        
                        
        elif request.method=="GET":
            if 'username' in session:
                    email = session['username']
                
                    currentCollection = mongo.db.parents
               # user_email = request.form['email']
               # user_chrome_id = request.form['id']
                #check and match chrome_id and user_email from database
                    check = currentCollection.find_one({'email':email})
                    if check is not None:
                          print('user logged in')
                          return jsonify({'username':check['username']})
                    else:
            
                          return jsonify({'user':'not found'}),404
                    
            else:
        
                  return jsonify({'username':'session not set'}),404 
        else:
              return jsonify({'username':'session not set'}),404 


@app.route('/signup',methods=["POST"])
def signup():
    if request.method=='POST':
        currentCollection = mongo.db.parents
        print(request.form)
        email = request.form['email']
        fullname = request.form['name']
        
        password = request.form['pswd']
        enc_password = hashlib.md5(password.encode())
        print(enc_password.hexdigest())
        #check email exits or not
        find_email = currentCollection.find_one({'email':email})
        print(find_email)
        
        if find_email is not None:
              return render_template('indexx.html',r_error="this email is used")
        else:
        
            try:
                    created_date = datetime.now().strftime("%c")
                    db_response= currentCollection.insert_one({
                            'created_at':created_date,
                            'email':email,
                            'username':fullname,
                            
                            'password':enc_password.hexdigest()
                            
                        })
                    if db_response:
                        session['username']=email
                        print(db_response)
                        return redirect(url_for('hello_tracer'))
            except Exception as ex:
                print(ex)
                return jsonify(ex),500
  






#child login in extension
@app.route('/child_login',methods=['GET','POST'])
def child_login_in_extension():
        if request.method=="GET":
            if 'u_id' in session:
                    child_ID = session['u_id']
                
                    currentCollection = mongo.db.members
               # user_email = request.form['email']
               # user_chrome_id = request.form['id']
                #check and match chrome_id and user_email from database
                    check = currentCollection.find_one({'u_id':child_ID})
                    if check is not None:
                          print('user logged in')
                          return jsonify({'username':check['name'],'child_id':child_ID})
                    else:
            
                          return jsonify({'user':'not found'}),404
                    
            else:
        
                  return jsonify({'username':'session not set'}),404 
        
        elif request.method=="POST":
              print(request.json)
              login_cred=request.json
              if 'u_id' not in session:
                    child_ID = login_cred['child_id']
                    password = hashlib.md5(login_cred['password'].encode()).hexdigest()
                    parentsTable = mongo.db.parents
                    membersTable = mongo.db.members
                    membersCheck = membersTable.find_one({'u_id':child_ID})
                    print("line291")
                    #print(membersCheck)
                    if membersCheck is not None:
                            parents_ref_id = membersCheck['ref_id']
                            print(parents_ref_id)
                            print(password)
                            check_parents_password = parentsTable.find_one({'email':parents_ref_id ,'password':password})
                            print(check_parents_password)
                            
                            if check_parents_password is not None:
                                    session['u_id']=membersCheck['u_id']
                                    session['name']=membersCheck['name']
                                 
                                    print(membersCheck['u_id'])
                            
                                    return jsonify({'username':membersCheck['u_id']},201)
                            else:
                                 print('password did not match')
                                 return jsonify({'user':'not found'},201) 
                          
                            '''alldata= list(mongo.db.parents.aggregate([
                                                    {
                                                        '$lookup': {
                                                            'from': 'members', 
                                                            'localField': 'ref_id', 
                                                            'foreignField': 'email', 
                                                            'as': 'result'
                                                        }
                                                    }
                                    ]))
                           
                           return Response(json.dumps(alldata,default=str),mimetype="application/json")    '''
                    else:
                                 print('child id  did not match')
                                 return jsonify({'user':'not found'},201)     
                               
                     
        else:
            return jsonify({'user':'not found'})        
                    
                          
                    
                           
#data coming from extension

      
@app.route('/extension_data',methods=['POST']) 
async def extension_data():
      print(session['u_id'])
     
      if 'u_id' in session:
            store_extension_url_duration = request.json
            #print(type(store_extension_url_duration))
            date_time = get_date_time_now()
            for d in store_extension_url_duration:
                d['timestamp']=date_time
            #
           
            
            urls_list =[]
            for url in store_extension_url_duration:
                        urls_list.append(url['url'])
            urlparse(url['url']).netloc
            membersCollection = mongo.db.members
            delurl = ['http://localhost:4000/','chrome://newtab/']
            filertDomain = ['www.youtube.com']

            #FILTER URLS 
            filter_url = [url for url in store_extension_url_duration if  url['url'] not in delurl]
            filter_urls = [url for url in filter_url if  urlparse(url['url']).netloc not in filertDomain]
            youtube_url = [url for url in filter_url if  urlparse(url['url']).netloc in filertDomain]
            print('line 510')
            print(youtube_url)
            print('line 510')
            #================================
            # store url/sec in collection
            store_list = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"urls":{"$each":filter_url}}})
            if store_list:print('url_duration store')
            #================================
            #STORING DATA INTO KEYWORD FIELD
            scraper = Scraper()
            if len(filter_url)>=1:
                
                meta_keywords=scrape_urls(filter_urls)
               
                #print(meta_keywords)
                 
                video_keywords = scrape_Video_url(youtube_url)
              
                if video_keywords is not None and len(video_keywords) != 0:
                    print('line 389')
                    # Assuming youtube_url is a string containing the YouTube URL
                    #youtube_url = 'https://www.youtube.com/watch?v=VIDEO_ID'  # Replace with the actual YouTube URL

                    # Create a list of dictionaries with the video URL(s)
                    video_urls = [{'url': youtube_url}]
                    #video_keywords = await scraper.run_scraper(youtube_url, scrape_type='video_url')
                    
                    #print(video_keywords)
                    
                    store_keywords = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"keywords":{"$each":video_keywords}}})
                    if store_keywords:print('video_key_store')
                    else:print('video_key_store--ERROR') 
                if meta_keywords is not None and len(meta_keywords) != 0:
                    print('line 391')
                    #print(meta_keywords)
                    store_keywords = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"keywords":{"$each":meta_keywords}}})
                    if store_keywords:print('meta_key_store')
                    else:print('meta_key_store--ERROR') 
            #end of keyword store
              
            
      return jsonify({'data':request.json})        
    
 #comment Fetch
@app.route('/testcomm',methods=['GET'])
async def insertCom():
    return None
     
 # 07/05/23
@app.route('/ext_comment',methods=['POST'])
async def comments_data():
        comments = request.json  
        print(comments)
        
        #creating a list of dict
        print('line 576 comment')
        
        comment_set = set()
        comment = dict()
        for each in comments:
            comment.update(each)
            if each['comment']:
                
                 comment_set.add(each['comment'])
            else: return jsonify({'comment':request.json})
            
        comment_array = list(comment_set)
        print(comment_array)
        print('----------------707')
        com_list = []
        com_list.append(comment)
                  
        
        comment_data_keyword=await scrape_Comment_url(com_list)
        language_accuracy_testing = await language_accuracy_v2(com_list)
        
        #serialized_data = json.dumps(language_accuracy_testing)
        print(language_accuracy_testing)
       
        if 'u_id' in session:
                if len(comment_data_keyword)>=1:
                    print('keyword found')
                    print(comment_data_keyword)
                    membersCollection = mongo.db.members
                    print('line609 Ccomment_data_keyword')
                    print(comment_data_keyword)
                    print(type(comment_data_keyword))
                    print('line609 language_accuracy_testing')
                    print(language_accuracy_testing)
                    print(type(language_accuracy_testing))
                    
                    store_comment = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"keywords":{"$each":comment_data_keyword}}})
                    # Convert the set to a list for serializability
                    misspelled_words_list = list(language_accuracy_testing[0]['misspelled_words']) if isinstance(language_accuracy_testing[0]['misspelled_words'], list) else None

                    correct_words_list = language_accuracy_testing[0]['correct_words']

                    # Update the document with lists instead of sets
                    store_language_accuracy_data = membersCollection.update_one(
                        {"u_id": session["u_id"]},
                        {"$push": {
                            "language_accuracy": {
                                "$each": [{
                                    'comment': language_accuracy_testing[0]['comment'],
                                    'misspelled_words': misspelled_words_list,
                                    'correct_words': correct_words_list,
                                    'grammar_mistakes': language_accuracy_testing[0]['grammar_mistakes'],
                                    'correction': language_accuracy_testing[0]['correction'],
                                    'correct_comment': language_accuracy_testing[0]['correct_comment'],
                                    'fluent': language_accuracy_testing[0]['fluent'],
                                    'impression': language_accuracy_testing[0]['impression'],
                                    'grammer_mistake_count': language_accuracy_testing[0]['grammar_count'],
                                    'spell_mistake_count' : language_accuracy_testing[0]['spell_count'],
                                    'time': language_accuracy_testing[0]['time']
                                }]
                            }
                        }}
                    )

                    if store_comment:
                          print('keywords store')
                    else:
                
                        print('error store')

        return jsonify({'comment':request.json})

#logout
@app.route('/logout')
def logout():
     if 'username' in session:
          session.pop('username',None)
         
          return redirect(url_for('register'))
     else:
            return redirect(url_for('register'))
     
#child_logout
@app.route('/comments',methods=['GET'])
def allComment():
       if 'username' in session:
            currentCollection = mongo.db.parents
            childCollection = mongo.db.members
            
            
            data = currentCollection.find_one({'_id': ObjectId('641ed8fd525a62d526068e43')})
            args = request.args
            data = (json.loads(unquote(args['data'])))
            testdata=[{'comment': 'Ram siya Ram , Siya ram , jai jai ram'}, {'comment': 'mere tan man siya ram ram hai '}]
            print(data)
            print(type(data))
            child_id = (args['c_id'])
            for each in testdata:
                    scores = userTonality(each['comment'],'static/dataset/tonality.csv')
                    emotion =analysis(each['comment'],'static/dataset/emotion.csv')
                    '''
                    # Determine the tonality based on the compound score
                    compound_score = scores['compound']

                    if compound_score >= 0.05:
                        tonality = "Positive"
                    elif compound_score <= -0.05:
                        tonality = "Negative"
                    else:
                        tonality = "Neutral"
                    '''
                    each['ton'] = scores
                    each['emo'] = emotion
           
            print(testdata)
            # Convert NumPy ndarrays to lists before passing to the template
            converted_data = []
            for entry in data:
                converted_entry = entry.copy()  # Make a copy to avoid modifying the original data
                for key, value in entry.items():
                    if isinstance(value, np.ndarray):
                        converted_entry[key] = value.tolist()  # Convert ndarray to list
                converted_data.append(converted_entry)
            comments_json = json.dumps(converted_data) 
            #return data
          
            return render_template('comment_pag.html',content=session['username'],comments=data,child_ID = child_id,comments_json=comments_json)
       else: 
        return render_template('register.html')
       


    
        
        
        



@app.route('/child_logout')

def child_logout():
      
    if 'u_id' and 'name' in session:
                print(session)
                c_id=session['u_id']
                c_name=session['name']

                session.pop('u_id',None) 
                session.pop('name',None) 
                
                
                return redirect(url_for('hello_tracer'))
    


#Mobile App Data structuring 18/01/24'
#child login in extension

'''
=======================================
=  Mobile App Data Storing
=  
=========================================
'''

@app.route('/mobile_login', methods=['POST'])
def child_login_in_mobile():
    if request.method == "POST":
        login_cred = request.get_json()
        print(login_cred)

        username = login_cred['username']
        password = hashlib.md5(login_cred['password'].encode()).hexdigest()
        role = login_cred['role']
        parentsTable = mongo.db.parents
        membersTable = mongo.db.members

        if role == 'admin':
            check_parents_password = parentsTable.find_one({'email': username, 'password': password})
            if check_parents_password is not None:
                return jsonify({'userID': username, 'userType': role})
            else:
                print('password did not match')
                return jsonify({'user': 'not found'})
        else:
            membersCheck = membersTable.find_one({'mobile_id': username})

            if membersCheck is not None:
                parents_ref_id = membersCheck['ref_id']
                print(parents_ref_id)
                print(password)
                check_parents_password = parentsTable.find_one({'email': parents_ref_id, 'password': password})
                
                if check_parents_password is not None:
                    print(membersCheck['u_id'])
                    return jsonify({'userID': membersCheck['u_id'], 'userType': role})
                else:
                    print('password did not match')
                    return jsonify({'user': 'not found'})
            else:
                print('child id did not match')
                return jsonify({'user': 'not found'})
    else:
        return jsonify({'error': 'Method Not Allowed'}), 405
      
                    
@app.route('/userInteraction',methods=['POST'])
def userInteraction():
    if request.method == 'POST':
        query = request.form.get('query')  # Access form data by key
        
        if query is not None:
                print(f" search query: {query}")
        
                return (f" search query: {query}") 
            
         
        # Access other form data
        
        # Process the data as needed
                            
@app.route('/userComment',methods=['POST'])
async def usercomment():
    if request.method == 'POST':
        comment = request.form.get('comment')
        url = request.form.get('url')# Access form data by key
        com_list = []
        com_list.append({'comment':comment,'url':url})
        
        if com_list is not None:
                print(f" search query: {comment}")
                language_accuracy_testing = await language_accuracy_mobile(com_list)
                print(language_accuracy_testing)
                
                return (f" search query: {comment}") 
                '''
         
                  
        
        comment_data_keyword=await scrape_Comment_url(com_list)
        language_accuracy_testing = await language_accuracy_v2(com_list)
        
        #serialized_data = json.dumps(language_accuracy_testing)
        print(language_accuracy_testing)
       
        if 'u_id' in session:
                if len(comment_data_keyword)>=1:
                    print('keyword found')
                    print(comment_data_keyword)
                    membersCollection = mongo.db.members
                    print('line609 Ccomment_data_keyword')
                    print(comment_data_keyword)
                    print(type(comment_data_keyword))
                    print('line609 language_accuracy_testing')
                    print(language_accuracy_testing)
                    print(type(language_accuracy_testing))
                    
                    store_comment = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"keywords":{"$each":comment_data_keyword}}})
                    # Convert the set to a list for serializability
                    misspelled_words_list = list(language_accuracy_testing[0]['misspelled_words']) if isinstance(language_accuracy_testing[0]['misspelled_words'], list) else None

                    correct_words_list = language_accuracy_testing[0]['correct_words']

                    # Update the document with lists instead of sets
                    store_language_accuracy_data = membersCollection.update_one(
                        {"u_id": session["u_id"]},
                        {"$push": {
                            "language_accuracy": {
                                "$each": [{
                                    'comment': language_accuracy_testing[0]['comment'],
                                    'misspelled_words': misspelled_words_list,
                                    'correct_words': correct_words_list,
                                    'grammar_mistakes': language_accuracy_testing[0]['grammar_mistakes'],
                                    'correction': language_accuracy_testing[0]['correction'],
                                    'correct_comment': language_accuracy_testing[0]['correct_comment'],
                                    'fluent': language_accuracy_testing[0]['fluent'],
                                    'impression': language_accuracy_testing[0]['impression'],
                                    'grammer_mistake_count': language_accuracy_testing[0]['grammar_count'],
                                    'spell_mistake_count' : language_accuracy_testing[0]['spell_count'],
                                    'time': language_accuracy_testing[0]['time']
                                }]
                            }
                        }}
                    )

                    if store_comment:
                          print('keywords store')
                    else:
                
                        print('error store')
                '''
        
                
            
@app.route('/youtubedata',methods=['POST'])
def userTimeSpend():
    if request.method == 'POST':
        membersCollection = mongo.db.members
        timer = request.form.get('timer')
        u_id = request.form.get('u_id')
        url = request.form.get('url')
        date_time = get_date_time_now()
        userTimeSpendList = []
        userTimeSpendList.append({'url':url,'sec':timer,'timestamp':date_time})
        print(userTimeSpendList)
        
        
        if timer != '0':
                print(f" time spend: {timer} and user id : {u_id} and url :{url}")
                urls_list =[]
                for url in userTimeSpendList:
                            urls_list.append(url['url'])
                urlparse(url['url']).netloc
              
                delurl = ['http://localhost:4000/','chrome://newtab/']
                filertDomain = ['www.youtube.com']
                #FILTER URLS 
                filter_url = [url for url in userTimeSpendList if  url['url'] not in delurl]
                filter_urls = [url for url in filter_url if  urlparse(url['url']).netloc not in filertDomain]
                youtube_url = [url for url in filter_url if  urlparse(url['url']).netloc in filertDomain]
                
                store_list = membersCollection.update_one({"u_id":u_id},{"$push":{"app_urls":{"$each":filter_url}}})
                if store_list:
                    print('url_duration store')
                    video_keywords = scrape_Video_url(filter_url)
                    if video_keywords is not None and len(video_keywords) != 0:
                       
                        
                        
                        store_keywords = membersCollection.update_one({"u_id":u_id},{"$push":{"mobile_keywords":{"$each":video_keywords}}})
                        if store_keywords:print('video_key_store')
                        else:print('video_key_store--ERROR') 
                    
                    return (f" time spend: {timer} and user id : {u_id} and url :{url} Stored in database successfully")
                else:
                    return (f" time spend: {timer} and user id : {u_id} and url :{url} Stored in database Failed")

@app.route('/allmembers', methods=['GET'])
async def allMembers():
    userID = request.args.get('id')
    if userID:
        child_Table=mongo.db.members
        print(userID)
        cleaned_email = userID.strip("'")
        query = {'ref_id':cleaned_email}
        data=child_Table.find(query)
        childList = []
        for doc in data:
            childList.append({'app_id':doc['u_id'],'childName':doc['name']})
        print(childList)
    # Create a dictionary instead of a set
    data_dict = {'data': childList }

    # Use jsonify with the dictionary
    return jsonify(data_dict)
    
@app.route('/tagcloud',methods=['GET'])
async def appTagCloud():

    return jsonify({'msg':'data will send shortly'})
    
    '''
    args = request.args
    if 'username' in session:
           
            #print(args)
            #fetch data
            child_id=args['u_id']
           
            
            fetch_data=await fetch_data_using_id(child_id,'u_id')
            all_urls = fetch_data[0]['urls']
            
            if fetch_data:
               # print(len(fetch_data[0]))
                listdata = json.loads(json_util.dumps(fetch_data[0]))
                lang_acc_chart_data=await lang_acc_chart(fetch_data)
               # print(lang_acc_chart_data)
                
                if 'urls' in fetch_data[0] :
                    print('hello')
                    
                    tonality_emotions_checking,screen_Time,total_count_data,wc = await asyncio.gather(
                    #language_accuracy_using_comments2(fetch_data[0]),
                    tonality_emotion_graph_array(fetch_data[0]['keywords'],'dashboard'),
                    screen_time_count(fetch_data[0]),
                    pages_duration(fetch_data[0]),
                    wcloud(fetch_data[0]['keywords'])
                    )
                
                    screenTime_data= json.dumps(screen_Time)
                    data_on=json.dumps(tonality_emotions_checking)
                    total_comments = tonality_emotions_checking[0]['tot_comments']
                    print('line185')
                    #print(grammar_checking)
                    #print(tonality_emotions_checking)
                    
                    #[pages,seconds,comments]
                    total_count_data.append(total_comments)
                
                    return render_template("dashboard.html",dataton=data_on,screenTime=screenTime_data,count_data=json.dumps(total_count_data),
                                            
                                            wordcloud_data=json.loads(json_util.dumps(wc)),
                                            parentId=json.loads(json_util.dumps(session['username'])),
                                            language_accurac=json.loads(json_util.dumps(lang_acc_chart_data)),
                                            all_url=json.loads(json_util.dumps(all_urls)),
                                            child_id=json.dumps(child_id),
                                            cID=args['u_id']
                                            )
                
                else:
                      return render_template("dashboard.html",dataton=json.dumps([]),screenTime=json.dumps([]),count_data=json.dumps([]),
                                            
                                            wordcloud_data=json.dumps([]),
                                            parentId=json.loads(json_util.dumps(session['username'])),
                                            language_accurac=json.dumps([]),
                                            child_id=json.dumps(child_id),
                                            cID=args['u_id']
                                            )
                    
                

                
                                         
            else:
    
                 return render_template("dashboard.html",wordcloud=json.loads(json_util.dumps([])),parentId=json.loads(json_util.dumps(session['username'])),cID=args['u_id'])
    else:
        return render_template('indexx.html')
    '''
                    
                    
                           





if __name__ == "__main__":
    # Create and run the Flask application in the main thread
    app.run(debug=True, port=4000)