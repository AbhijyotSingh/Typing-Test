import openai,time
import mysql.connector as sql

def register():
    cur.execute("SELECT names from login_details")
    name_lis=[i[0] for i in cur.fetchall()]
    name1=input("Enter your username:")
    password1=input("Enter your password:")
    if name1 not in name_lis:
        cur.execute("INSERT INTO login_details(names,passwords) VALUES(%s,%s)",(name1,password1))
        db.commit()
        print("Registered successfully! Enjoy.")
    else:
        print("Username already exists. Try logging in.")
    
def login():
    print("Welcome back!")
    name1=input("Please enter your username to confirm:")
    password1=input("Please enter your password to confirm:")
    cur.execute("SELECT names from login_details")
    names=[i[0] for i in cur.fetchall()]
    cur.execute("SELECT passwords from login_details where names=%s",(name1,))
    passwords=cur.fetchone()
    if name1 in names and password1==passwords[0]:
        print(f"Welcome back {name1}!")
    else:
        print("You are not a registered user. Try again.")    
        return        
  
def typing_test():
    name=input("Enter your username:")
    #Creating a table for the user
    cur.execute("USE typing_test")
    cur.execute(f"CREATE TABLE IF NOT EXISTS {name}(id int AUTO_INCREMENT PRIMARY KEY, wpm FLOAT,acc FLOAT)")
    db.commit()
    
    #Random paragraph generation through OpenAI
    key=input("Enter your api key from OpenAI to proceed further:")
    client=openai.OpenAI(api_key=key)
    message="Generate a random paragraph not too big in order to test typing speed. Include punctuation marks also. You can source it from any song, any literature or piece together your own. Do not announce that youre giving the paragraph, just do."
    response=client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":message}])
    para=response.choices[0].message.content
    print("Please type in this paragraph to test your typing speed.\n")
    print(para,"\n")
    
    #Timer and typing starts
    input("Press enter when ready to start typing:")
    start_time=time.perf_counter()
    type=input()
    end_time=time.perf_counter()
    time_elapsed=end_time-start_time
    time_min=time_elapsed/60
    
    #Time and accuracy calculated
    print(f"\nIt took you: {time_min:.2f} minutes to write the entire thing.")
    type_lis=type.split(" ")
    para_lis=para.split(" ")
    count=0
    for typed_word, para_word in zip(type_lis,para_lis):
        try:
            if typed_word==para_word:
                count+=1
            else:
                pass
        except IndexError:
            print("You did not write the complete thing.")
            break
    per=(count/len(para_lis))*100
    wpm=count/time_min
    print(f"Your typing speed is: {wpm:.2f} wpm.")
    if per==100:
        print("Congratulations! You have 100% accuracy.")
    else:
        print(f"Congrats! You have {per:.2f}% accuracy.")
    print("Thank you for taking part in this typing test.")
    cur.execute(f"INSERT INTO {name}(wpm,acc) values(%s,%s)",(wpm,per))
    db.commit()
  
def show_details():
    ques=input("Do you want to see login details or typing details (login/typing):")
    if ques.lower()=="typing":
        cur.execute("SELECT names from login_details")
        name=input("Enter your username:")
        names=[i[0] for i in cur.fetchall()]  
        if name in names:
            print("(Number of races, Words/Min, Accuracy)")
            cur.execute(f"SELECT * from {name}")
            for i in cur:
                print(i)
        else:
            print("User not found. Try registering.")
    elif ques.lower()=="login":
        name=input("Enter your username:")
        cur.execute("SELECT names from login_details")
        names=[i[0] for i in cur.fetchall()] 
        print("(ID, Username, Password)") 
        if name in names:
            cur.execute("SELECT * from login_details where names=%s",(name,))
            for i in cur:
                print(i)
        else:
            print("User not found.")
            return
    else:
        print("Only these options are available.")
        return
  
def update():
    name=input("Enter your old username:")
    password=input("Enter your old password:")
    cur.execute("SELECT names from login_details")
    names=[i[0] for i in cur.fetchall()]  
    cur.execute("SELECT passwords from login_details where names=%s",(name,))
    passwords=cur.fetchone()
    if name in names and password==passwords[0]:
        ques=input("Which part do you want to update (username/password):")
        if ques.lower()=="username":
            new_user=input("Enter new username:")
            cur.execute("UPDATE login_details set names=%s where passwords=%s",(new_user,password))
            db.commit()
        elif ques.lower()=="password":
            new_pass=input("Enter new password:")
            cur.execute("UPDATE login_details set passwords=%s where names=%s",(new_pass,name))
            db.commit()
        else:
            print("Only these options are available.")
            return
  
def main():
    print("\n-----Welcome to Typing Test-----")
    print("Challenge yourself to type small, randomly generated paragraphs as fast as you can!")
    ques=input("Do you want to login or register (login/register):")
    if ques.lower()=="register":
        register()
    elif ques.lower()=="login":
        login()
    else:
        print("No more options available.")
        return
    print("Press 0 to exit.")
    print("Press 1 to start to the Typing Test.")
    print("Press 2 to show your details.")
    print("Press 3 to update your username or password.")
    try:
        choice=int(input("Enter choice:"))
    except ValueError:
        print("Only integral values allowed.")
    else:
        if choice==0:
            return 
        elif choice==1:
            typing_test()
        elif choice==2:
            show_details()
        elif choice==3:
            update()
        else:
            print("Only these options are available.")
            return 
        
if __name__=="__main__":
    pass1=input("Enter the password for your SQL Database:")
    db=sql.connect(
        host="localhost",
        user="root",
        password=pass1
    )
    cur=db.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS Typing_test")
    print("Database created successfully.")
    cur.execute("USE Typing_test")
    cur.execute("CREATE TABLE IF NOT EXISTS login_details (id INT AUTO_INCREMENT PRIMARY KEY, names VARCHAR(255) NOT NULL, passwords varchar(255) NOT NULL)")
    print("Login table created.")
    main()

