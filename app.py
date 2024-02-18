from flask import Flask, render_template, url_for, request, session, redirect, jsonify,flash
import dill as pickle
import pymongo
from functools import wraps
from passlib.hash import pbkdf2_sha256
import uuid
from datetime import timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import math
import dns
# import logging
# import sys



# SETTING UP MOONGO ATLAS
client = pymongo.MongoClient("mongodb+srv://testuser:test@cluster0.8ondf.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.get_database('employability_db')
records = db.students
q_val = db.quest_val
t_det = db.test_details

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'mysecret'

#METHOD FOR STARTING A USERS SESSION
def start_session(user):
  del user['password']          
  session['logged_in'] = True       
  session['user'] = user        #ASSIGNING CURRENT USER AS OBJ TO SESSION USER VARIABLE 
  return redirect(url_for('profile'))

#Method for verifying and logging in 
def login():
    user = records.find_one({
        "email": request.form.get('email')
    })
    if user and pbkdf2_sha256.verify(request.form.get('pass'), user['password']):
        return start_session(user)

    flash(f'Login Failed! Invalid credintials','danger') 
    return redirect(url_for('index'))


# Route for signing out, clearing session
@app.route('/signout')
def signout():
    session.clear()
    return redirect('/')


@app.route('/edit', methods=['POST','GET'])
def edit_profile():
    if request.method == "POST":
        new_scores = list(float(request.form.get('edit_sem' + str(i) + '_score')) for i in range(1,9))
        empstatus = request.form.get('emp_status')
        pack = request.form.get('package')
        if empstatus == '1':
            empstatus = "Placed"
        elif empstatus == '2':
            empstatus = "Looking for Job"
        else :
            empstatus = "Going for Higher Studies"

        records.update({'email':session['user']['email']}, 
        {"$set": {  "marks.sem1":new_scores[0], 
                    "marks.sem2":new_scores[1], 
                    "marks.sem3":new_scores[2], 
                    "marks.sem4":new_scores[3], 
                    "marks.sem5":new_scores[4], 
                    "marks.sem6":new_scores[5], 
                    "marks.sem7":new_scores[6], 
                    "marks.sem8":new_scores[7],
                    "emp_status":empstatus,
                    "package": pack}})
        upd_user = records.find_one({
            "email":session['user']['email']
        })
        session['user'] = upd_user
        return render_template('edit_profile.html')        

    if request.method == "GET":
        return render_template('edit_profile.html')
  
#Method for mandating login
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  return wrap


#Route for index
@app.route('/',methods=['POST','GET'])
def index():
    if 'user' in session:
        return redirect('profile')
    if request.method == 'POST':
        return login()
    return render_template('index.html')


#Route for registering user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = {                                    #creating user object with user details
        "_id": uuid.uuid4().hex,
        "fname": "".join(request.form.get('reg_fname').split()),
        "lname": "".join(request.form.get('reg_lname').split()),
        "email": "".join(request.form.get('reg_email').split()),
        "password": request.form.get('reg_pass'),
        "marks": {
            "sem1":request.form.get('reg_sem1_score'),
            "sem2":request.form.get('reg_sem2_score'),
            "sem3":request.form.get('reg_sem3_score'),
            "sem4":request.form.get('reg_sem4_score'),
            "sem5":request.form.get('reg_sem5_score'),
            "sem6":request.form.get('reg_sem6_score'),
            "sem7":request.form.get('reg_sem7_score'),
            "sem8":request.form.get('reg_sem8_score')
        },
        "emp_status": request.form.get('emp_status'),
        "package": request.form.get('package'),
        "test_taken":0,
        "count":0
        }

        if user["emp_status"] == '1':
            user["emp_status"] = "Placed"
        elif user["emp_status"] == '2':
            user["emp_status"] = "Looking for Job"
        else :
            user["emp_status"] = "Going for Higher Studies"

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if records.find_one({ "email": user['email'] }):                        #Checking if account already created
            ue = user['email']
            flash(f'Account already in use for { ue }!','sucess') 
            return redirect(url_for('register'))

        if records.insert_one(user):            #Inserting user info into database
            return start_session(user)

        flash(f'Signup failed !','danger') 
        return redirect(url_for('register'))


    return render_template('register.html')         #rendering registration page if req == GET


# Rotue for test page
@app.route('/test', methods=['POST','GET'])
@login_required
def test():
    if request.method == 'POST':                    #if method==post then create user obj with scores and store in DB
        os = 'organizational_skill_'  
        ls = 'leadership_skill_'    
        cs = 'communication_skill_'     
        tms = 'time_management_skill_'      
        pss = 'problem_solving_skill_'    
        sms = 'self_management_skill_'      
        tws = 'team_work_skill_' 
        dms = 'decision_making_skill_'
        scs = 'self_confidence_skill_'
        cvs = 'creativity_skill_'  
        count = records.find_one({"email": session['user']['email'] })['count']

        cur_user = {
        "test_id": session['user']['fname']+session['user']['lname']+str(count+1),
        "fname": session['user']['fname'],
        "lname": session['user']['lname'],
        "email": session['user']['email'],
        "quest_score":{},
        }

        # Getting all the values from the form  for all the parameters 
        scores = {}
        for i in range(1,6):
            scores[str(i)]= request.form.get(os+str(i))
        cur_user['quest_score']['organizational_skill'] = scores
        c1 = sum(list(int(k) for k in scores.values()))
        t1 = round(5*i/3,0)
        t2 = round(5*2*i/3,0)
        if c1 < t1:
            ogr = "You've got to improve your organizational skills. "
        elif c1 >= t1 and c1 < t2:
            ogr = "Good but there's room for improvement."
        else:
            ogr = "Your organizing skill is very effective!"
        
        scores={}
        for i in range(1,8):
            scores[str(i)] = request.form.get(ls+str(i))
        cur_user['quest_score']['leadership_skill'] = scores
        c2 = sum(list(int(k) for k in scores.values()))
        t1 = round(5*i/3,0)
        t2 = round(5*2*i/3,0)
        if c2 < t1:
            lr = "You need to work hard on your leadership skills."
        elif c2 >= t1 and c2 < t2:
            lr = "You're doing OK as a leader, but you have the potential to do much better."
        else:
            lr = "Excellent! You're well on your way to becoming a good leader."
        
        scores={}
        for i in range(1,6):
            scores[str(i)] = request.form.get(cs+str(i))
        cur_user['quest_score']['communication_skill'] = scores
        c3 = sum(list(int(k) for k in scores.values()))
        t1 = round(5*i/3,0)
        t2 = round(5*2*i/3,0)
        if c3 < t1:
            cr = "You need to keep working on your communication skills. You are not expressing yourself clearly and you may not be receiving messages correctly, either."
        elif c3 >= t1 and c3 < t2:
            cr = "You're a capable communicator, but you sometimes experience communication problems. Take the time to think about your approach to communication, and focus on receiving messages effectively, as much as sending them. "
        else:
            cr = "Excellent! You understand your role as a communicator, both when you send messages and when you receive them. You anticipate problems, and you choose the right channel to communicate."
        
        scores={}
        for i in range(1,9):
            scores[str(i)] = request.form.get(tms+str(i))
        cur_user['quest_score']['time_management_skill'] = scores
        c4 = sum(list(int(k) for k in scores.values()))
        t1 = round(5*i/3,0)
        t2 = round(5*2*i/3,0)
        if c4 < t1:
            tmr = "You've got to improve your time management skills. "
        elif c4 >= t1 and c4 < t2:
            tmr = "You're good at some things, but there's room for improvement elsewhere."
        else:
            tmr = "You're managing your time very effectively!"
        
        scores={}
        for i in range(1,6):
            scores[str(i)] = request.form.get(pss+str(i))
        cur_user['quest_score']['problem_solving_skill'] = scores
        c5 = sum(list(int(k) for k in scores.values()))
        t1 = round(5*i/3,0)
        t2 = round(5*2*i/3,0)
        if c5 < t1:
            psr = "Your approach to problem solving is more intuitive than systematic, and this may have led to some poor experiences in the past. With more practice, and by following a more structured approach, you'll be able to develop this important skill and start solving problems more effectively right away. "
        elif c5 >= t1 and c5 < t2:
            psr = "Your approach to problem solving is a little \"hit-and-miss.\" Sometimes your solutions work really well, and other times they don't. You understand what you should do, and you recognize that having a structured problem-solving process is important. However, you don't always follow that process. By working on your consistency and committing to the process, you'll see significant improvements."
        else:
            psr = "You are a confident problem solver. You take time to understand the problem, understand the criteria for a good decision, and generate some good options. Because you approach problems systematically, you cover the essentials each time – and your decisions are well though out, well planned, and well executed."
        
        scores={}
        for i in range(1,8):
            scores[str(i)] = request.form.get(sms+str(i))
        cur_user['quest_score']['self_management_skill'] = scores
        c6 = sum(list(int(k) for k in scores.values()))
        t1 = round(5*i/3,0)
        t2 = round(5*2*i/3,0)
        if c6 < t1:
            smr = "You allow your personal doubts and fears to keep you from succeeding. You've probably had a few incomplete goals in the past, so you may have convinced yourself that you aren't self-motivated - and then you've made that come true. Break this harmful pattern now, and start believing in yourself again."
        elif c6 >= t1 and c6 < t2:
            smr = "You're doing OK on self-motivation. You're certainly not failing - however, you could achieve much more. To achieve what you want, try to increase the motivation factors in all areas of your life."
        else:
            smr = "Wonderful! You get things done, and you don't let anything stand in your way. You make a conscious effort to stay self-motivated, and you spend significant time and effort on setting goals and acting to achieve those goals."
        
        scores={}
        for i in range(1,8):
            scores[str(i)] = request.form.get(dms+str(i))
        cur_user['quest_score']['decision_making_skill'] = scores
        c7 = sum(list(int(k) for k in scores.values()))
        t1 = round(5*i/3,0)
        t2 = round(5*2*i/3,0)
        if c7 < t1:
            dmr = "Your decision-making hasn't fully matured. You aren't objective enough, and you rely too much on luck, instinct or timing to make reliable decisions."
        elif c7 >= t1 and c7 < t2:
            dmr = "Your decision-making process is OK. You have a good understanding of the basics, but now you need to improve your process and be more proactive. Concentrate on finding lots of options and discovering as many risks and consequences as you can. The better your analysis, the better your decision will be in the long term."
        else:
            dmr = "You have an excellent approach to decision-making! You know how to set up the process and generate lots of potential solutions."
        
        scores={}
        for i in range(1,6):
            scores[str(i)] = request.form.get(tws+str(i))
        cur_user['quest_score']['team_work_skill'] = scores
        c8 = sum(list(int(k) for k in scores.values()))
        t1 = round(5*i/3,0)
        t2 = round(5*2*i/3,0)
        if c8 < t1:
            twr = "You've got to improve your time work skills. "
        elif c8 >= t1 and c8 < t2:
            twr = "You're good at some things, but there's room for improvement elsewhere."
        else:
            twr = "You're managing your team very effectively!"
        
        scores={}
        for i in range(1,6):
            scores[str(i)] = request.form.get(scs+str(i))
        cur_user['quest_score']['self_confidence_skill'] = scores
        print(list(scores.values()))
        c9 = sum(list(int(k) for k in scores.values()))
        t1 = round(5*i/3,0)
        t2 = round(5*2*i/3,0)
        if c9 < t1:
            scr = "You probably wish you had more self-confidence! Take a closer look at all the things you've achieved in your life. You may tend to focus more on what you don't have, and this takes time and attention away from recognizing and using your skills and talents."
        elif c9 >= t1 and c9 < t2:
            scr = "You're doing an OK job of recognizing your skills, and believing in your abilities. But perhaps you're a little too hard on yourself, and this may stop you from getting the full benefit of your mastery experiences."
        else:
            scr = "Excellent! You're doing a fabulous job of learning from every experience, and not allowing obstacles to affect the way you see yourself. "
        
        scores={}
        for i in range(1,6):
            scores[str(i)] = request.form.get(cvs+str(i))
        cur_user['quest_score']['creativity_skill'] = scores
        c10 = sum(list(int(k) for k in scores.values()))
        t1 = round(5*i/3,0)
        t2 = round(5*2*i/3,0)
        if c10 < t1:
            cvr = "You're unsure of your creative talent. Maybe you haven't been given opportunities to be creative, or maybe you're convinced that you're simply not a creative person. Either way, look for opportunities to improve how you do things, even if you don't have any current problems. "
        elif c10 >= t1 and c10 < t2:
            cvr = "Your creativity is a \"work in progress.\" You've had some successes, so now it's time to let loose and stretch yourself. Share your ideas and perspectives with others, and ask them how they view problems."
        else:
            cvr = "Creativity is one of your strengths, and innovative and creative minds are highly sought after. So don't hide your ability! "
        
        #inserting each score to table quest_values

            
        cptr_list = list(float(session['user']['marks']['sem'+str(i)]) for i in range (1,9) if session['user']['marks']['sem'+str(i)] != 'Null')
        cptr = round(sum(cptr_list)/len(cptr_list), 2)
        
        #calculating the 4 parameters
        o1 =  math.ceil((c5*20)/25)
        o2 =  math.ceil(cptr*20/10)
        o3 = math.ceil(c3*20/25)
        o4 = math.ceil((c1+c2+c4+c6+c7+c8+c9+c10)*20/200)
        final_params = [o1,o2,o3,o4]

        #storing parameter values to db
        cur_user['param_scores']= {"c1":c1,"c2":c2,"c3":c3,"c4":c4,"c5":c5,"c6":c6,"c7":c7,"c8":c8,"c9":c9,"c10":c10,"cptr":cptr,'o1':o1, 'o2':o2, 'o3':o3, 'o4':o4,}
        test_date = datetime.now().date()
        test_time = datetime.now().time()
        cur_user['test_date'] = str(test_date)
        cur_user['test_time'] = str(test_time.hour) +':'+str(test_time.minute) +':'+str(test_time.second)
        test_datetime = [cur_user['test_date'],cur_user['test_time']]
        
        xip = np.array([final_params])
        with open('model_v1.pk' ,'rb') as f:
            loaded_model = pickle.load(f)
        yip = loaded_model.predict(xip)
        ans = ''
        for i in range(len(yip)):
            ans = ""
            if yip[i]==4:
                ans += "Your overall results are Outstanding! (Grade: O)"
            elif yip[i]==3:
                ans += "Your overall results are Very Good (Grade: A)"
            elif yip[i]==2:
                ans+= "Your overall results are Good (Grade: B)"
            elif yip[i]==1:
                ans+= "Your overall results are Average (Grade: C)"
            elif yip[i]==0:
                ans+= "You need to work hard on your Employability skills (Grade: D)"
        cur_user['result']=ans

        #creating dictionary for details of test and assigning to cur_user variable
        result_det = {'ogr':ogr,'lr':lr,'cr':cr,'tmr':tmr,'psr':psr,'smr':smr,'twr':twr,'dmr':dmr,'scr':scr,'cvr':cvr}
        cur_user['result_det'] = result_det

        #updating the count value and test_taken variables
        records.update_one({'email':cur_user['email']},{'$set':{'test_taken':1}})
        records.update_one({'email':cur_user['email']}, {"$set":{'count':count+1}})

        q_val.insert_one(cur_user)          #inserting cur_user variables with all detaisl of the test to the database
        upd_user = records.find_one({
            "email":session['user']['email']
        })
        session['user'] = upd_user
        return render_template('dash.html',report = ans, result_det=result_det)

    return render_template('test.html')


@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method == 'GET':
        upd_user = records.find_one({
            "email":session['user']['email']
        })
        session['user'] = upd_user
        if records.find_one({'email':session['user']['email']})['test_taken']:
            test_rec = list(q_val.find({'email':session['user']['email']}))
            plot_rec = test_rec[-4:]        #last 4 records
       
            fig, ax = plt.subplots(figsize=(10, 5))
            parameters = ['Aptitude', 'Technical', 'Communication', 'Personality']
            width=0.2
            idx = np.asarray([i for i in range(len(parameters))])
       
            for rec in plot_rec:
                l = rec['param_scores']
                f = [v for v in l.values()][-4:]
                ax.bar(idx, f, width=width)
                idx = idx + width

            idx = np.asarray([i for i in range(len(parameters))])
            ax.set_title("Test Results History (previous 4 tests)", fontsize=15)
            ax.set_xticks(idx+width)
            ax.set_xticklabels(parameters)
            ax.set_xlabel("Parameters", fontsize=15)
            ax.set_ylabel("Parameter scores", fontsize=15)
            fig.tight_layout()
            fig.savefig('static/images/final_plot'+session['user']['fname'] + session['user']['lname']+ '.png', bbox_inches="tight", transparent=True)
            name = 'static/images/final_plot'+session['user']['fname'] + session['user']['lname']+ '.png'
            return render_template('profile.html',test_rec=test_rec, file=name)

        return render_template('profile.html')

#function to call the result dashboard for old tests
    if request.method == 'POST':
        but_id = request.form.get('result_but')
        result_det = q_val.find_one({'test_id':but_id})['result_det']
        ans = q_val.find_one({'test_id':but_id})['result']
        l = q_val.find_one({'test_id':but_id})['param_scores']

        parameters = ['organizational', 'leadership', 'communication', 'time_management', 'problem_solving',
                      'self_management', 'team_work', 'decision_making', 'self_confidence', 'creativity']
        para_scores = [v for v in l.values()][:10]
        
        fig, ax = plt.subplots(figsize = (10,5))
        ax.set_title("Results", fontsize=15)
        ax.set_xticklabels(parameters, rotation=55)
        ax.set_xlabel("Parameters", fontsize=15)
        ax.set_ylabel("Parameter scores", fontsize=15)
        ax.bar(parameters, para_scores)
        
        name = 'static/images/plot' + but_id+ '.png'
        fig.savefig(name, transparent=True, bbox_inches="tight")

        return render_template('dash.html',report = ans, result_det=result_det, url=name)



@app.route('/dash', methods=['GET'])
@login_required
def dash():
    return render_template('dash.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
    # app.logger.addHandler(logging.StreamHandler(sys.stdout))
    # app.logger.setLevel(logging.ERROR)

