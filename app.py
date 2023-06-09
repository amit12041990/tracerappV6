from flask import Flask,render_template,url_for,request,session,jsonify,redirect,make_response,Response
#importing custome functions
from functions.scrape import *
from functions.check_emo_ton import *
import json,hashlib,datetime,uuid,bson
import pandas as pd
import numpy as np
from urllib.parse import urlparse,unquote
#importing two module os and openai
import os
import io
import openai
from flask_pymongo import PyMongo
from datetime import timedelta
from bson.objectid import ObjectId
from bson import json_util
from flask_cors import *
#tonality check NLTK MODULE
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

#class Based View Test
from views import all_views
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MONGO_URI'] = 'mongodb://localhost:27017/childTrace'
app.config['SECRET_KEY']='amit'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(days=7)
mongo = PyMongo(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


app.add_url_rule('/home',view_func=all_views.Home_View.as_view('index'))

@app.route("/")
def hello_world():
    #return "<p>Hello, World!</p>"
   
    if 'username' in session:
        currentCollection = mongo.db.parents
        childCollection = mongo.db.members
        data = currentCollection.find_one({'_id': ObjectId('641ed8fd525a62d526068e43')})
        alldata= list(mongo.db.parents.aggregate(
              [
                    {
                        '$lookup': {
                            'from': 'members', 
                            'localField': 'ref_id', 
                            'foreignField': 'email', 
                            'as': 'result'
                        }
                    }
            ]
        ))
        
        childData = childCollection.find({'ref_id':session['username']})
        c_data = json.loads(json_util.dumps(childData))
        #print(c_data)
        
        
        #print(alldata[0]["result"])
        return render_template('parrent_dashboard.html',content=session['username'],childs=c_data)
    else:
         return render_template('register.html')
# child data 
@app.route("/child_report",methods=['GET'])
def report_card():
  
    
      if 'username' in session:
            args = request.args
            print(args)
            #fetch data 
            currentCollection = mongo.db.members
            data = currentCollection.find_one({'u_id': args['id']})
            '''
            alldata= list(mongo.db.members.aggregate(
                    [
                            {
                                '$lookup': {
                                    'from': 'parents', 
                                    'localField': 'email', 
                                    'foreignField': args['id'], 
                                    'as': 'parent'
                                }
                            }
                    ]
                    ))
            '''
            
            if 'urls' in data  :
                if not data['urls']:
                    listdata = json.loads(json_util.dumps(data))
                    return render_template("child_report.html",content=listdata,parentId=session['username'])
                     
                        
                else:
                        surf_urls = data['urls']
                        new_list = []
                        for i in surf_urls:
                            #print(i)
                            new_list.append(i)
                        
                    
                        df = pd.DataFrame(new_list)
                        result = df.groupby(by=["url"], as_index=False).sum()
                        urls_list = result.to_dict()['url']
                        sec_list = result.to_dict()['sec']
                        print(result.to_dict())
                        merge_lists_into_dict = np.array([{'url':urls_list[u],'sec':sec_list[s]} for (u,s) in zip(urls_list,sec_list)])
                        print(type(merge_lists_into_dict))
                        
                        #print(f"url: {result.to_dict()['url'][110]} sec : {result.to_dict()['sec'][110]}")

                        
                            
                        listdata = json.loads(json_util.dumps(data))
                        
                        #print(listdata)
                        return render_template("child_report.html",content=listdata,parentId=session['username'],browse_record=merge_lists_into_dict)
                      
            else:
                  return render_template("child_report.html",content=listdata,parentId=session['username'])
              
#Tag Cloud
@app.route("/child_report_tag",methods=['GET'])
def report_tag_cloud():
  
    
      if 'username' in session:
            args = request.args
            #print(args)
            #fetch data 
            currentCollection = mongo.db.members
            data = currentCollection.find_one({'u_id': args['id']})
            listdata = json.loads(json_util.dumps(data))
            
            if 'keywords' in listdata: 
                 # wc= words_cloud(listdata['keywords'])
                  wc=wcloud(listdata['keywords'])
                  print('line 131')
                  #print(wc)
                  #print(json.loads(json_util.dumps(wc)))
                  return render_template("child_tag_cloud.html",wordcloud=json.loads(json_util.dumps(wc)),parentId=json.loads(json_util.dumps(session['username'])),childdata=json.loads(json_util.dumps(listdata)))
            else:
                 return render_template("child_tag_cloud.html",wordcloud=json.loads(json_util.dumps([])),parentId=json.loads(json_util.dumps(session['username'])),childdata=json.loads(json_util.dumps(listdata))) 
            
            
#REGISTER PARENTS
@app.route("/register")
def register():
    if 'username' not in session:
        return render_template('register.html',r_error="")
    else:
          return redirect(url_for('hello_world'))

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
                                    return redirect(url_for('hello_world'))
                                    #return jsonify({'user':check['username']})
                            else:
                                return render_template('register.html',error="user not found")
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
              return render_template('register.html',r_error="this email is used")
        else:
        
            try:
                    created_date = datetime.datetime.now().strftime("%c")
                    db_response= currentCollection.insert_one({
                            'created_at':created_date,
                            'email':email,
                            'username':fullname,
                            
                            'password':enc_password.hexdigest()
                            
                        })
                    if db_response:
                        session['username']=email
                        print(db_response)
                        return redirect(url_for('hello_world'))
            except Exception as ex:
                print(ex)
                return jsonify(ex),500
  



@app.route('/create_child',methods=["POST"])
def create_child():
    data = request.form
    childname = data['childname']
    #age = data['age']
    gender = data['sex']
    dob = request.form['birthday']
    print(dob)
    currentCollection = mongo.db.members
    unique_id = str(uuid.uuid4())
    #idd = bson.Binary.from_uuid(unique_id)

    print(unique_id)
    ref_email= session['username']  
    print(ref_email)
    try:
                created_date = datetime.datetime.now().strftime("%c")
                db_response= currentCollection.insert_one({
                        'name':childname,
                        
                        'gender':gender,
                        'ref_id':ref_email,
                        'u_id':unique_id,
                        'dob':dob,
                        'urls':[]
                        
                    })
                if db_response:
                      #print(db_response)
                      return redirect(url_for('hello_world'))
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
def extension_data():
      print(request.json)
      if 'u_id' in session:
            store_extension_url_duration = request.json
            print(type(store_extension_url_duration))
            
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
            #================================
            # store url/sec in collection
            store_list = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"urls":{"$each":store_extension_url_duration}}})
            if store_list:print('url_duration store')
            #================================
            #STORING DATA INTO KEYWORD FIELD
            if len(filter_url)>=1:
                  
                meta_keywords=scrape_urls(filter_urls)
                video_keywords = scrape_Video_url(youtube_url)
                if len(video_keywords)!=0:
                    print('line 389')
                    store_keywords = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"keywords":{"$each":video_keywords}}})
                    if store_keywords:print('video_key_store')
                    else:print('video_key_store--ERROR') 
                if len(meta_keywords)!=0:
                    print('line 391')
                    print(meta_keywords)
                    store_keywords = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"keywords":{"$each":meta_keywords}}})
                    if store_keywords:print('meta_key_store')
                    else:print('meta_key_store--ERROR') 
            #end of keyword store
                '''
                if len(meta_keywords)>=1:
                    print('keyword found')
                    print(meta_keywords)
                    store_keywords = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"keywords":{"$each":meta_keywords}}})
                    if store_keywords:
                          print('keywords store')
                    else:
                
                        print('error store')  
                elif len(video_keywords)>=1:
                    print('video keyword found')
                    print(video_keywords)
                    store_keywords = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"keywords":{"$each":video_keywords}}})
                    if store_keywords:
                          print('video')
                    else:
                
                        print('error store') 
                      
                else:
                    
                    print('no')    
                store_list = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"urls":{"$each":store_extension_url_duration}}})
                if store_list:
                    print('hello ext')
                '''
            
      return jsonify({'data':request.json})        
    
 #comment Fetch
 # 07/05/23
@app.route('/ext_comment',methods=['POST'])
def comments_data():
        comments = request.json  
        # print(comments[3])
        
        #creating a list of dict
        comment = dict()
        for each in comments:
            comment.update(each)
        com_list = []
        com_list.append(comment)
        
        comment_data_keyword=scrape_Comment_url(com_list)
        if 'u_id' in session:
                if len(comment_data_keyword)>=1:
                    print('keyword found')
                    print(comment_data_keyword)
                    membersCollection = mongo.db.members
                    store_comment = membersCollection.update_one({"u_id":session["u_id"]},{"$push":{"keywords":{"$each":comment_data_keyword}}})
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
            nltk.data.path.append('env/path/ntlt_data')
            sid = SentimentIntensityAnalyzer()
            data = currentCollection.find_one({'_id': ObjectId('641ed8fd525a62d526068e43')})
            args = request.args
            data = (json.loads(unquote(args['data'])))
            child_id = (args['c_id'])
            for each in data:
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
            #return data
            return render_template('comment_pag.html',content=session['username'],comments=data,child_ID = child_id)
       else: 
        return render_template('register.html')
       

@app.route('/videos',methods=['GET'])
def allvideo():
       if 'username' in session:
            currentCollection = mongo.db.parents
            childCollection = mongo.db.members
            data = currentCollection.find_one({'_id': ObjectId('641ed8fd525a62d526068e43')})
            args = request.args
            data = (json.loads(unquote(args['data'])))
            print(data)
          
            return render_template('comment_pag.html',content=session['username'],comments=data,child_ID = session['u_id'])
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
                
                
                return render_template('index.html',child_id=c_id,name=c_name)
    


@app.route('/pagi',methods=['GET'])
def pagination():
      return render_template('comment_pag.html')




if __name__ == "__main__":

    app.run(debug=True,port=4000)