

#Project Kamino. Folder cloning and synchronization.


from threading import Thread
from time import sleep
import os
import shutil
import logging
import sys

# Start function only appear if Kamino is not running. -- w_run 
def star_only():
    w_run_y = input("Welcome to Kamino.\nWould you like to create your very own cloning station? y or n. " ).lower()
    while True: 
        if w_run_y == "y":
            w_run=w_run_y
            return w_run_y
        if w_run_y == "n":
            quit()
        else:
            w_run_y = input("Please provide a valid answer. ")

# Log file location first choice -- log 1
def log_choice(question,error_message,run_test):
    log_mut = input(question)
    while True:
        if os.path.exists(log_mut):
            log=log_mut
            log_path= os.path.join(log,"logs.log")
            logging.basicConfig(level= logging.INFO ,
             format="%(asctime)s - %(message)s" ,
             handlers=[logging.FileHandler(log_path) ,
             logging.StreamHandler(sys.stdout)])            
            logging.info ("Chosen log file location is: "+ log_path )
            return log
        if str(log_mut).lower() == "settings" and run_test != "":
            change_settings()
            return "settings"            
        else: 
            log_mut = input(error_message )

# Check if in folder is within directory 
def forbidden_folder_check(forbidden_folder_list,folder):
    for root, dirs, files in os.walk(forbidden_folder_list):
        for dir in dirs:
            if str(folder) == os.path.join(root,dir):
                return ( "forbidden" )
            if str(folder) == os.path.dirname(os.path.join(root,dir)):
                return ( "forbidden" ) 
    
# Source folder first choice -- source 2        
def source_choice(question, error_message,cloned_folder):
    source_mut = input(question)
    if cloned_folder=="":
        while True:
            if os.path.exists(source_mut) and str(source_mut) != str(cloned_folder):
                source=source_mut
                logging.info ("Source folder is: " + source )
                return source
            else:
                source_mut = input(error_message)
    else:
        while True:        
            if os.path.exists(source_mut) and forbidden_folder_check(cloned_folder,source_mut) != "forbidden":
                source=source_mut
                logging.info ("Source folder is: " + source )
                return source
                break
            if str(source_mut).lower() == "settings":
                return "settings"
                break
            else:
                source_mut = input(error_message)


# Clone folder location first choice -- clone 3
def clone_choice(question, error_message,source_folder,run_test):
    clone_mut = input(question)
    while True:
        if os.path.exists(clone_mut) and forbidden_folder_check(source_folder,clone_mut)!= "forbidden":
            clone=clone_mut
            logging.info ("Clone station folder directory is: " + clone)           
            return clone
        if str(clone_mut).lower() == "settings" and run_test != "":
            return "settings"       
        else:
            clone_mut = input(error_message)
                   
# Check if name can be a folder at root location
def forbidden_folder_name_check(root,folder_name):
    try:
        test_folder=os.path.join(root,folder_name)
        os.mkdir(test_folder)
        return "folder created"
    except  FileExistsError:
        return "folder already exists"
    except:
        pass

# Clone folder name first choice --  4
def clone_name_choice(question,error_message1,error_message2,clone_folder,run_test):
    clone_station_y = input(question)
    while True:
        if forbidden_folder_name_check(clone_folder,clone_station_y) == "folder created":
            clone_station = clone_station_y
            logging.info ("Chosen clone station folder is: " + clone_station )
            return os.path.join(clone_folder,clone_station_y)
        if str(clone_station_y).lower() == "settings" and run_test != "":
            return "settings"       
        if forbidden_folder_name_check(clone_folder,clone_station_y) == "folder already exists":
            clone_station_y = input(error_message1)
        else:
            clone_station_y = input(error_message2)

# Sync period choice result must be in sec -- sync_period 5
def sync_period_choice(question,error_message1,run_test):
    sync_period_l = input(question).lower()
    while True:
        if sync_period_l == "h":
            return "hours"
        if sync_period_l == "m":
            return "minutes"
        if sync_period_l == "s":
            return "seconds"
        if sync_period_l == "settings" and run_test != "":
            return "settings"         
        else:
            sync_period_l = input(error_message1).lower()

# Sync period size choice result must be in sec -- sync_period 5
def sync_period_size_choice(question,error_message,period,run_test):
    sync_period_size_y = input(question)
    while True:
        if sync_period_size_y.isnumeric() == True:
            sync_period_size = sync_period_size_y
            logging.info("Synchronization period is: " + sync_period_size_y + " " + period )            
            return sync_period_size           
        if str(sync_period_size_y).lower == "settings" and run_test != "":
            return "settings"         
        else:
            sync_period_size_y = input(error_message) 

# Show menu <apagar não há nada para mudar
def show_menu(log_file,source_folder,clone_folder_location,clone_folder_name,period_type,period):
    print("\nYou have now finished setting up your cloning operation. This are it's settings." )
    print("\nSettings\n" )
    settings = [ "Log file location is: " + log_file + "\logs.log" + ". ",
     "Source folder location is: " + source_folder + ". ",
      "Clone folder location is: " + clone_folder_location + ". ",
     "clone folder name is: " + clone_folder_name + ". ",
      "Cloning operation interval is: " + period + " " + period_type + ". "]
    for number, letter in enumerate(settings, start=1):
        print(number, letter)

# Change settings -- setting  <apagar nome já mudado --
def change_settings(): 
    setting_choice = input("Do you want to change any settings? If so, enter the corresponding number. \nIf you are happy with the current settings and want to run the program enter 'run'. Enter 'settings' to see the current settings. ").lower()
    while True:
        if setting_choice <= "5" and setting_choice >= "1":
            setting = setting_choice
            return (setting)                
        if setting_choice == "run":
            setting = setting_choice 
            return "run"
        if setting_choice == "settings":
            setting = setting_choice
            return "settings"
        if setting_choice == "stop":
            return "stop"
        if setting_choice == "alive":
            return "alive"
        else:
            setting_choice = input("Please provide a valid answer. ").lower()

# Copy and folder creation function criar exceção para log file
def copy():
    global source
    global clone_station
    if not os.path.exists(clone_station) and clone_station != (""):
        os.mkdir(clone_station)
    for root, dirs, files in os.walk(source):
        for dir in dirs:
            try:
                new_root = root.replace(source,clone_station)
                created_folder = (new_root + "\\" + dir)
                os.mkdir(created_folder)
                logging.info (dir + "  copied to: " + new_root )
            except:
                print
        for file in files:
            clone_dir = root.replace(source,clone_station)
            file_location = (root + '\\'+ file)
            new_file_location = (clone_dir + '\\'+ file)
            if file=="logs.log":
                pass
            if not os.path.exists(new_file_location): 
                try:
                    shutil.copy2(file_location, clone_dir)
                    logging.info (file + "  copied to: " + new_root )
                except:
                    print

# Delete Function acrescentar maneira de apagar ficheiro caso a metadata seja diferente só ficheiro!!!
def remove():
    global source
    global clone_station
    for root, dirs, files in os.walk(clone_station):
        for dir in dirs:
            source_dir = root.replace(clone_station,source)
            source_dir_check = source_dir + "\\" + dir
            if not os.path.exists(source_dir_check):
                shutil.rmtree(root + "\\" + dir)
                logging.info (dir + "  deleted from: " + root )                
        for file in files:
            source_dir = root.replace(clone_station,source)
            source_file_check = source_dir + "\\" + file
            if not os.path.exists(source_file_check):              
                os.remove(root + "\\" + file)
                logging.info (file + "  deleted from: " + root )
            if os.path.exists(source_file_check) and os.path.getmtime(source_file_check) != os.path.getmtime(root + "\\" + file):
                os.remove(root + "\\" + file)
                logging.info (file + "  deleted from: " + root )

# Program running function
def kamino():
    remove()
    sleep(1)                
    copy()
    
# Task that runs at a fixed interval
def cloning():
    global closes
    while True:
        if closes == "stop":
            break
        sleep(1)
        kamino()
        sleep(int(sync_period_val))
        


# Preparing variables. There must be a more elegant solution.
kamino_cloning = Thread()
w_run = ""
global log
log = ""
global source
source = ""
global clone
clone = ""
global clone_station
clone_station = ""
global sync_period
sync_period = ""
global sync_period_size
sync_period_size = ""
setting = ""
global closes
closes = ""

while True:
    while w_run == "" :
        w_run=star_only()       
    while log == "" or source == "" or clone == ""or clone_station == "" or sync_period == "" or sync_period_size == "" :
        while log == "":
            log = log_choice("Let's start by setting up your log file. Where would you like to store your log file? ",
            "The system cannot find the specified folder. Please provide a valid directory. ","")
        while source == "":
            source = source_choice("What folder would you like to clone? ", 
            "The system cannot find the specified folder. Please provide a valid directory. ","")
        while clone == "":
            clone = clone_choice("In what folder would you like to store your clone station? We will create a new folder in this locating with a name of your choosing. " ,
             "The system cannot find the specified folder or it is being used has the source folder. Please provide a valid directory. ",source,"")
        while clone_station == "":
            clone_station = clone_name_choice("What is your clone station name? ","Folder already exists, please provide a valid folder name. ",
            "Please provide a valid folder name. ",clone,"")
        while sync_period == "":
            sync_period = sync_period_choice("Would you like to set up your cloning process in a per x amount of seconds, per x amount of minutes or per x amount of hours? Answer s for seconds, m for minutes or h for hours. ",
            "Please provide a valid answer. S for seconds, M for minutes, H for hours.  ","")
            if sync_period == "seconds":
                sync_period_num = 1
            if sync_period == "minutes":
                sync_period_num = 60
            if sync_period == "hours": 
                sync_period_num = 3600
        while sync_period_size == "":
            sync_period_size = sync_period_size_choice("What will be the interval, in " + sync_period + ", for each cloning process. ",
            "Please provide a numeric value. ",sync_period,"")
            global sync_period_val
            sync_period_val = int(sync_period_size) * sync_period_num
            print (sync_period_val)  
    while True:
        if setting == "" or setting == "settings":
            show_menu(log , source , clone , clone_station , sync_period , sync_period_size)
            setting = change_settings()
        if setting == "1":
            log_mut = log_choice("Where would you like to store your new log file? Enter 'settings' if you want to to go back to the current settings menu. ",
            "The system cannot find the specified folder.  Please provide a valid directory. Enter 'settings' if you want to go back to the current settings menu. ",1)
            if log_mut != "settings":
                log=log_mut
            show_menu(log , source , clone , clone_station , sync_period , sync_period_size)
            setting = change_settings()
        if setting == "2":
            source_mut = source_choice("What folder would you like to clone? Enter 'settings' if you want to to go back to the current settings menu.", 
            "The system cannot find the specified folder. Please provide a valid directory. Enter 'settings' if you want to to go back to the current settings menu.",clone)
            if source_mut != "settings":
                source=source_mut
            show_menu(log , source , clone , clone_station , sync_period , sync_period_size)
            setting = change_settings()
        if setting == "3":
            clone_mut = clone_choice("In what folder would you like to store your clone station? We will create a new folder in this locating with a name of your choosing.Enter 'settings' if you want to to go back to the current settings menu. " ,
             "The system cannot find the specified folder or it is being used has the source folder. Please provide a valid directory. Enter 'settings' if you want to to go back to the current settings menu. ",source,1)
            if clone_mut != "settings":
                if clone_mut == clone:
                    pass
                else:
                    clone = clone_mut
                    clone_station_mut = clone_name_choice("What is your clone station name? ","Folder already exists, please provide a valid folder name. Enter 'settings' if you want to to go back to the current settings menu ",
                    "Please provide a valid folder name. Enter 'settings' if you want to to go back to the current settings menu ",clone,"")
                    if clone_station_mut != "settings":
                        clone_station = clone_station_mut
                    show_menu(log , source , clone , clone_station , sync_period , sync_period_size)
                    setting = change_settings()
            else:
                show_menu(log , source , clone , clone_station , sync_period , sync_period_size)
                setting = change_settings()
        if setting == "4":
            clone_station_mut = clone_name_choice("What is your clone station name? ","Folder already exists, please provide a valid folder name. Enter 'settings' if you want to to go back to the current settings menu ",
            "Please provide a valid folder name. Enter 'settings' if you want to to go back to the current settings menu ",clone,"")
            if clone_station_mut != "settings":
                clone_station = clone_station_mut
            show_menu(log , source , clone , clone_station , sync_period , sync_period_size)
            setting = change_settings()
        if setting == "5":
            sync_period_mut = sync_period_choice("Would you like to set up your cloning process in a per x amount of days, per x amount of hours or per x amount of seconds? Answer d for days, h for hours or s for seconds. Enter 'settings' if you want to to go back to the current settings menu ",
            "Please provide a valid answer. H for hours, D for days, S for seconds. Enter 'settings' if you want to to go back to the current settings menu ",1)
            sync_period_size_mut = sync_period_size_choice("What will be the interval, in " + sync_period + ", for each cloning process. Enter 'settings' if you want to to go back to the current settings menu. ",
            "Please provide a numeric value. Enter 'settings' if you want to to go back to the current settings menu. ",sync_period,1)
            if sync_period_mut != "settings":
                sync_period = sync_period_mut
                if sync_period == "seconds":
                    sync_period_num = 1
                if sync_period == "minutes":
                    sync_period_num = 60
                if sync_period == "hours": 
                    sync_period_num = 3600
            if sync_period_size_mut != "settings":
                sync_period_size = sync_period_size_mut
                sync_period_val = int(sync_period_size) * sync_period_num
            show_menu(log , source , clone , clone_station , sync_period , sync_period_size)
            setting = change_settings()
        if setting == "run" and not kamino_cloning.is_alive():                
            kamino_cloning = Thread(target=cloning, name='Kamino')
            kamino_cloning.start()
        if setting == "run" and kamino_cloning.is_alive():
            closes = ""
            logging.info ("Program is running. ")
            setting= change_settings()
        if setting == "stop" and kamino_cloning.is_alive():            
            closes = "stop"
            setting = change_settings()
        if setting == "stop" and not cloning.is_alive():
            logging.info ("Program has stopped. ")
            setting = change_settings()
        if setting == "alive":
            print(bool(kamino_cloning.is_alive()))
            setting = change_settings()    

           


    




