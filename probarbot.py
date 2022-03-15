"""
Enlighten Telegram Bot 
By: Natnael(Mr.PGuy)
From buddies to buddies 
"""

import logging
from typing import Dict

from telegram.ext import *
from telegram import *

# import fetcher modul
import fetcher
import os
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
INITIAL, SEMESTER, DEPARTMENT, COURSE,OPTION, SERVE, LAST, RECIVE  = range(8)

# Callback data
ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, ELEVEN = range(12)
START, END = range(2)
SHARE, FIND = range(2)
CUTOMER_SERVICE, CHOOSING, TYPING_REPLY, TYPING_CHOICE, SERVE = range(5)
RETRIEVE, UPLOAD = range(2)

QUERY = {}
SEMES ={ '1': 'Freshman 1st', '2': 'Freshman 2nd', '3': 'Sophomore 1st', '4': 'Sophomore 2nd', '5': 'Junior 1st', '6': 'Junior 2nd', '7': 'Senior 1st', '8': 'Senior 2nd', '9': 'GC 1st', '10': 'GC 2nd'}
CAMPUS = 'ASTU'
DATA = fetcher.get_semesters(CAMPUS)
SEMESTERS = {}
SCHOOLS = []
NCLOUDX = os.environ.get("NCLOUDX")
TOKEN = os.environ.get("TOKEN") 
ADMIN = os.environ.get("ADMIN") 
PORT = int(os.environ.get('PORT', '8443'))

# DEPARTMENT = []
# for data in DATA:
#     for school in data['school_in_this_semes']:
#         for department in school['department']:
#             departments = {}
#             departments['id'] = department['id'] 
#             departments['short_name'] = department['short_name'] 
#             departments['name'] = department['name'] 
#             departments['school'] = school['name']
#             DEPARTMENT.append(departments)
# for dep in DEPARTMENT:
#     print(dep)
#     print()


reply_keyboard_0 = [
    ['/download', '/share'],
    ['Feed Back', 'How To'],
]
reply_keyboard_1 = [
    ['Semester'],
    ['Reset'],
    ['Home 🛖'],
]

reply_keyboard_2 = [
    ['Semester', 'Department'],
    ['Reset'],
    ['Home 🛖'],
]

reply_keyboard_3 = [
    ['Semester', 'Department'],
    ['Find'],
    ['Reset'],
    ['Home 🛖'],
]


markup_zero = ReplyKeyboardMarkup(reply_keyboard_0, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Choose one of the button")
markup_one = ReplyKeyboardMarkup(reply_keyboard_1, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Choose one of the button")
markup_two = ReplyKeyboardMarkup(reply_keyboard_2, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Choose one of the button")
markup_three = ReplyKeyboardMarkup(reply_keyboard_3, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Choose one of the button")

def space(n):
    s = ' '
    for i in range(n):
        s+=s
    return s
def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key}  -  {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])
def clean_data(user_data):
        l = []
        for d in user_data:
            l.append(d)
        for i in l:
           del user_data[i]
        return user_data




""" --Download Section-- """

def start(update: Update, context: CallbackContext) -> int:
    QUERY = {}
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    # context.bot.send_message(chat_id= ADMIN ,text=f"new user [ \n user_id: {user.id} \n usr_name: @{user.username} \n first_name: {user.first_name} \n last_name: {user.last_name} \n is_bot: {user.is_bot} ] \n starts with mrpguybot")
    context.bot.send_message(chat_id = NCLOUDX ,text=f"new user [ \n user_id: {user.id} \n usr_name: @{user.username} \n first_name: {user.first_name} \n last_name: {user.last_name} \n is_bot: {user.is_bot} ] \n starts with mrpguybot")
    context.bot.send_message(chat_id = NCLOUDX ,text=f'{update}')
    user_obj = {
    'user_tg_id': user.id,
    'username': user.username,
    'first_name': user.first_name,
    'last_name': user.last_name 
    }
    try:

        fetcher.recored_new_user(user_obj)
    except Exception as e:
        print(e,'already exist')
    # logger.info("User %s started the conversation.", user.first_name)
 
    reply_text = f"📖📚📒📕📙📘📗📚📖\n"
    reply_text += f"Hi! {user.first_name} Welcome "
    if context.user_data:
        reply_text += (
            f"Again To Enlighten us too, knowldge shelf. "
        )
    else:
        reply_text += (
            f"To Enlighten us too, knowldge shelf. you can specify your semester and department to see what courses are there in your department . "
            " and then you can download any availabel course materials in your department easly "
            f" or you can share what you have !"
        )
  
    update.message.reply_text(text=reply_text, reply_markup=markup_zero)
    

def start_over(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query:
        user = query.from_user
    else:
        user = update.message.from_user

    reply_text = f"📖📚📒📕📙📘📗📚📖\n"
    try:
        MSG = QUERY['done_msg']
        reply_text += MSG + '\n'
    except Exception as e:
        pass
    reply_text += f"Hi! {user.first_name} Welcome "
    if context.user_data:
        reply_text += (
            f"Again To Enlighten us too, knowldge shelf. \n"
        )
    else:
        reply_text += (
            f"To Enlighten us too, knowldge shelf. you can specify your semester and department to see what courses are there in your department . "
            " and then you can download any availabel course materials in your department easly "
            f" or you can share what you have ! \n"
        )

    if query:
        query.from_user.send_message(text = reply_text, reply_markup = markup_zero)
    else:
        update.message.reply_text(text=reply_text, reply_markup=markup_zero)


def download(update: Update, context: CallbackContext) -> int:
    """download the conversation, display any stored data and ask user for input."""
    user = update.message.from_user
    print(context.user_data, 'download')
    reply_text = f"📖📚📒📕📙📘📗📚📖\n"
    reply_text += f"Hi! {user.first_name} Welcom "
    if context.user_data:
        reply_text += (
            f"Again To Enlighten us too, knowldge shelf. You already told me your {', '.join(context.user_data.keys())}. "
            f"<em>change anything you already set. </em>"
        )
    else:
        reply_text += (
            f"To Enlighten us too, knowldge shelf. you can specify your semester and department to see what courses are there in your department . "
            "and then you can download any availabel course materials in your department easly "
        )
    update.message.reply_text(reply_text, reply_markup=markup_one, parse_mode=ParseMode.HTML)

    return CHOOSING


def semester_choice(update: Update, context: CallbackContext) -> int:

    print(context.user_data, 'Semester')
    if update.callback_query:
        query = update.callback_query
        text = 'semester'
    else:
        text = update.message.text.lower()
    context.user_data['query'] = text
    if DATA:
        keyboard = [

            [str(DATA[semester]['semes_number']), str(DATA[semester + 1]['semes_number'])] for semester in range(0,len(DATA)-1,2)
          
        ]
        # keyboard += [['Back']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Choose one of the button")
        if context.user_data.get(text):
            reply_text = (
                f'Your {text} is {context.user_data[text]}, wanna change? '
            )
        else:
            reply_text = f'Enter {text} ,From the below list  {facts_to_str(SEMES)}'
        update.message.reply_text(reply_text, reply_markup = reply_markup)
    else:
        reply_text = f"Ther is No semester add to The database in this campus"
        update.message.reply_text(reply_text)


    return TYPING_REPLY


def department_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    print(context.user_data, 'Department')
    text = update.message.text.lower()
    print(text, "______text")
    context.user_data['query'] = text
    if context.user_data.get('semester'):
        context.bot.sendChatAction(chat_id=update.message.from_user.id ,action = ChatAction.TYPING)

        data = fetcher.get_departments_by_semester(context.user_data['semester'])
        keyboard = [

            [str(data[department]['id']), str(data[department + 1]['id'])] for department in range(0,len(data)-1,2)
          
        ]
        # keyboard +=[['Home']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Choose one of the button")
        if context.user_data.get(text):
            reply_text = f"Your {text} is {context.user_data[text]}, wanna change?"
        else:


            reply_text = f'Enter {text} ,From the below list'
            reply_text += '\n__________________________________________\n\n'
            dept = []
            # print(data)
            for dep in data:
                # print(dep)
                text = ' '
                text +=  '<strong> School </strong> :  ' + '<em>' + dep['school'] + '</em>' + '\n'
                text +=  '<strong> Department </strong> :  ' + '<em>' + dep['name'] + '</em>' + '\n'
                text +=  '<strong> ShortName </strong>:  ' + '<em>' + dep['short_name'] + '</em>' + '\n'
                text +=  '<strong> Button </strong> :  ' + '<em>' + str(dep['id']) + '</em>' + '\n'
                dept.append(text)
                
              
            reply_text += '\n'.join(dept)
        update.message.reply_text(reply_text, reply_markup = reply_markup, parse_mode = ParseMode.HTML)
        return TYPING_REPLY
    else:
        update.message.reply_text(f"please Selecte wich semister you  want first")
        return TYPING_REPLY
    return TYPING_REPLY


def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    def is_number(n):
        is_number = True
        try:
            num = float(n)
            # check for "nan" floats
            is_numberr = num == num   # or use `math.isnan(num)`
        except ValueError:
            is_number = False
        return is_number
    print(context.user_data, 'Recived Info')
    text = update.message.text
    category = context.user_data['query']
    if is_number(text):
        context.user_data[category] = text.lower()
    else:
        context.user_data[category] = ''
    del context.user_data['query']
    if context.user_data.get('semester') and context.user_data.get('department'):
        markup = markup_three
        r_text = f"this is a semester & department you're looking for ? "
        r_text += f" if that is right press the Find button "
    elif context.user_data.get('semester'):
        markup = markup_two
        r_text = f"this is a semester you're looking for ?, if that is right press the department button "
        r_text += f" or change your query on semester. "
    else:
        markup = markup_one
        r_text = f" <h1 color='blue'> Please Selecte Semester </h1>"
    if not context.user_data.get('semester'):
        reply_text = f" please Selecte Your Semester First Department {context.user_data.get('semester')} "
        update.message.reply_text(
            reply_text,
            reply_markup=markup,
            parse_mode = ParseMode.HTML
        )
    else:
        reply_text = f" Sweet! "
        reply_text += f"{facts_to_str(context.user_data)}"
        reply_text += r_text
        update.message.reply_text(
                
                reply_text,
                reply_markup=markup,
            )

    return CHOOSING


def Reset_history(update: Update, context: CallbackContext):
    """Store info provided by user and ask for the next category."""
    print(context.user_data, 'Reset History')
    text = update.message.text
    print(text)
    clean_data(context.user_data)
    if context.user_data.get('semester') and context.user_data.get('department'):
        markup = markup_three
    elif context.user_data.get('semester'):
        markup = markup_two
    else:
        markup = markup_one
    update.message.reply_text(
        "sweet ! Just so you know, all queries you enterd befor all cleaned, "
      
        "You can find more, or change your query on something, department or semester. ",
        reply_markup=markup,
    )

    return CHOOSING


def show_history(update: Update, context: CallbackContext) -> None:
    """Display the gathered info."""
    print(context.user_data, 'show_history')
    update.message.reply_text(
        f"This is your current : {facts_to_str(context.user_data)}"
    )


def find(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    # print(context.user_data, 'Find C')
    if 'query' in context.user_data:
        del context.user_data['query']
    # print(context.user_data['semester'])
    # print('_______________________________')
    # print(context.user_data['department'])
    # print('__________update_____________')
    # print(update)
    # print('__________update___________end__')
    context.bot.sendChatAction(chat_id=update.message.from_user.id ,action = ChatAction.TYPING)
    COURSES = fetcher.get_all_by_sem_and_dep(context.user_data['semester'], context.user_data['department'])
    QUERY['courses'] = COURSES
    if COURSES:
        # print(COURSES)
        # print(COURSES[1])
        keyboard = [

            [course['course_code']]for course in COURSES
            
            
        ]
        keyboard += [['Back']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Choose one of the button")
        text = ''
        for course in COURSES:

            text += '<strong> course_name </strong> :  ' + course['course_name'] + '\n'
            text += '<strong> course_code </strong> :  ' + course['course_code'] + '\n'
            text += '<strong> department </strong> :  ' + str(course['department']['short_name']) + '\n'
            text += '<strong> contributor </strong> :  ' + course['created_by'] + '\n\n\n'
            reply_text = f"{course['department']['name']} Semester - {course['semester']} Courses List"
        reply_text += '\n__________________________________________\n'
        reply_text += text
        update.message.reply_text(reply_text, reply_markup=reply_markup, parse_mode = ParseMode.HTML)
    else:
        keyboard = [['Back']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Choose one of the button")
        reply_text = f"no course add in department - {context.user_data['department']} Yet ! "

        update.message.reply_text(reply_text, reply_markup = reply_markup)
    return SERVE


def show_download_option(update: Update, context: CallbackContext):
    """Show new choice of buttons"""
    # print(context.user_data, 'Show Option')
    QUERY['course_code'] = update.message.text
    COURSES = QUERY['courses']
    if COURSES:
        
        reply_text = f" Course {QUERY['course_code']} "
        reply_text += '\n__________________________________________\n'
        for item in COURSES:
            if item['course_code'] == QUERY['course_code']:
                course = item 

        available_formats = course['available']  
        txt = ''
        for k,v in available_formats.items():
            txt += f"{k} - {v} | "
        reply_text += '\n\n course_name : ' + course['course_name']
        reply_text += '\n course_code : ' + course['course_code']
        reply_text += '\n course_description : ' + course['course_description']
        reply_text += f"\n available in : " + txt
        reply_text += f"\n ___________{course['course_code']}__________"
            

        keyboard = [

            [str(av) for av in available_formats],
            ['Back'],
       

        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Choose one of the button")   
        update.message.reply_text(text= reply_text, reply_markup = reply_markup)
        return SERVE
    else:
        update.message.reply_text(text="Invalid Callback Data | 404",)
        return ConversationHandler.END


def serve_file(update: Update, context: CallbackContext):
    # print(context.user_data, 'Serve File')
    query = update.message
    context.bot.sendChatAction(chat_id=update.message.from_user.id ,action = ChatAction.UPLOAD_DOCUMENT)
    data = fetcher.get_course_tg(context.user_data['semester'], context.user_data['department'], QUERY['course_code'])
    user = update.message.from_user
    MSG = 'Sending requested files ' + user.first_name
    if data:
        files = []
        for i,j in data.items():
            files = j['files'][query.text]
            print(j)
        MSG = f"<strong> {j['course_name']} </strong> \n"
        MSG += '\n__________________________________________\n\n'
        MSG += "<strong> course_name </strong>: " + f"{j['course_name']} \n"
        MSG += "<strong> course_description </strong>: " + f"{j['course_description']} \n"
        MSG += "<strong> semester </strong>: " + f"{j['semester']} \n"
        MSG += "<strong> department </strong>: " + f"{j['department']['name']} \n"
        MSG += "<strong> contributor </strong>: " + f"{j['created_by']} \n"
        MSG += "<strong> file format </strong>: " + f"{j['ava' ]} "
        query.from_user.send_message( MSG, parse_mode = ParseMode.HTML)
        for file in files:
            # print(file, "_____T____")
            # context.bot.send_message(user.id, file)
            # context.bot.send_document(user.id, file)
            file_id = file.split('N')[0]
            file_from = file.split('N')[-1]
            context.bot.copy_message(chat_id=update.effective_message.chat_id,
                    from_chat_id=file_from,
                    message_id=file_id)
       
        reply_text = f"Lots of Thank 🙏 for choosing us  {user.first_name}! "
        query.from_user.send_message(reply_text)
        # context.bot.send_message(user.id, reply_text)
        return SERVE
    else:
        MSG = f"Invalid Course code: {query.text} \n make sure that all characters are correct"
        reply_text = MSG
       
        update.message.reply_text(text= reply_text)
        return ConversationHandler.END



def upload(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    QUERY = {}
    query = update.callback_query
    # query.answer("✨ commingsoon ✨")
    keyboard = [
        [
            InlineKeyboardButton("Continue", callback_data=str(SHARE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
   
    query.edit_message_text(
        text=" ", reply_markup=reply_markup
    )
    return INITIAL





""" --Upload Sction-- """

CAMPUS = 'ASTU'
DATA = fetcher.get_semesters(CAMPUS)
SEMESTERS = {}
SCHOOLS = []
COURSES = []
def share(update: Update, context: CallbackContext) -> int:

    if DATA:
        
        global QUERY
        QUERY = {}
        keyboard = [

            [InlineKeyboardButton(DATA[semester]['name'], callback_data=str(DATA[semester]['semes_number'])), InlineKeyboardButton(DATA[semester+1]['name'], callback_data=str(DATA[semester+1]['semes_number']))] for semester in range(0,len(DATA)-1,2)
          
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            text="Choose your semester ", reply_markup=reply_markup
        )
        return SEMESTER
    else:
        update.message.from_user.send_message(text="Invalid Data | 404\n use /start re initiate",)
        return ConversationHandler.END

def school(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    global QUERY
    QUERY['semester'] = query.data
    # print('__________DICT__________School__')
    # print(QUERY)
    # print('__________END____________')
    
    SEMESTERS = [semester for semester in DATA if semester['semes_number'] == int(query.data)]
    if SEMESTERS:

        for semester in SEMESTERS:
            SCHOOLS = semester['school_in_this_semes']

        keyboard = [

           [InlineKeyboardButton(schools['name'], callback_data=str(schools['id']))] for schools in SCHOOLS
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text=" Choose your School ", reply_markup=reply_markup)

        return DEPARTMENT
    else:
        query.from_user.send_message(text="Invalid Callback Data | 404",)
        return ConversationHandler.END

def department(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    global QUERY
    QUERY['school'] = query.data
    # print('__________DICT__________Depart__')
    # print(QUERY)
    # print('__________END____________')
    
    SEMESTERS = [semester for semester in DATA if semester['semes_number'] == int(QUERY['semester'])]
 
    for semester in SEMESTERS:
        SCHOOLS = semester['school_in_this_semes']
    # DEPARTMENTS = [school for school in SCHOOLS if school['id'] == int(QUERY['school'])]
    for school in SCHOOLS:
        if school['id'] == int(QUERY['school']):
            DEPARTMENTS = school['department'] 
    if DEPARTMENTS:

        keyboard = [

           [InlineKeyboardButton(department['short_name'], callback_data=str(department['id']))] for department in DEPARTMENTS
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="Choose your Department", reply_markup=reply_markup)


        return COURSE
    else:
        query.from_user.send_message(text="Invalid Data | 404",)
        return ConversationHandler.END

def courses(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    global QUERY
    QUERY['department'] = query.data
    # print('__________DICT_________Courses__')
    # print(QUERY)
    # print('__________END____________')
    
    COURSES = fetcher.get_all_by_sem_and_dep(QUERY['semester'], QUERY['department'])
    QUERY['course'] = COURSES
    if COURSES:
        keyboard = [

           [InlineKeyboardButton(course['course_name'], callback_data=str(course['course_code']))] for course in COURSES
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_text = f"{QUERY['department']} {QUERY['semester']} Courses List"
        reply_text += '\n__________________________________________\n'
        for course in COURSES:

            reply_text += 'course_name : ' + course['course_name'] + '\n'
            reply_text += 'course_code : ' + course['course_code'] + '\n'
            reply_text += 'department : ' + str(course['department']['short_name']) + '\n'
            reply_text += 'contributor : ' + course['created_by'] + '\n\n\n'
        
        query.edit_message_text(text=reply_text, reply_markup=reply_markup)

        return OPTION
    else:
        query.from_user.send_message(text="Currentlly No courses specified in this department for this semester",)
        return ConversationHandler.END

def show_option(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    global QUERY
    QUERY['course_code'] = query.data
    
    COURSES = QUERY['course']
    if COURSES:
        
        reply_text = f"Course {QUERY['course_code']}"
        reply_text += '\n__________________________________________\n'
        for item in COURSES:
            if item['course_code'] == QUERY['course_code']:
                course = item 

        available_formats = course['available']  
        txt = ''
        for k,v in available_formats.items():
            txt += f"{k} - {v} | "
        reply_text += '\n\n course_name : ' + course['course_name']
        reply_text += '\n course_code : ' + course['course_code']
        reply_text += '\n course_description : ' + course['course_description']
        reply_text += f"\n available in : " + txt
        reply_text += f"\n ___________{course['course_code']}__________"
        QUERY['course_name'] = course['course_name']
        QUERY['course_code'] = course['course_code']
        QUERY['course_description'] = course['course_description']
            

 

        keyboard = [
        # [InlineKeyboardButton(av, callback_data=str(av)) for av in available_formats],
        [
        InlineKeyboardButton('PPT', callback_data='PPT'),
        InlineKeyboardButton('PDF', callback_data='PDF'), 
        InlineKeyboardButton('Book', callback_data='Book'),
        ],
        [
        InlineKeyboardButton("Back", callback_data=str(START)),
        ],

        ]

        reply_markup = InlineKeyboardMarkup(keyboard)    
        query.edit_message_text(text= reply_text, reply_markup = reply_markup)
        # print('QUERY_______________________________________start')
        # print(QUERY)
        # print('QUERY_______________________________________END')
        return SERVE
    else:
        query.from_user.send_message(text="Invalid Data | 404",)
        return ConversationHandler.END

def recive_file(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    data = fetcher.get_course_tg(QUERY['semester'], QUERY['department'], QUERY['course_code'])
    user = query.message.chat
    MSG = 'ready to grab files Mr/Mss' + user.first_name
    query.answer(MSG)

    # print('__________DICT_________Option__')
    # print(QUERY)
    # print('__________END____________')
    if data:
        # files = []
        # for i,j in data.items():
        #     print(j, j['files'], 'BOOOOOOOOOOOOOOOOOOOOO_M_______')
        #     files = j['files'][query.data]
        COURSES = QUERY['course']
        if COURSES:
            
            reply_text = f"Course {QUERY['course_code']}"
            reply_text += '\n__________________________________________\n'
            for item in COURSES:
                if item['course_code'] == QUERY['course_code']:
                    course = item 

            available_formats = course['available']  
            txt = ''
            for k,v in available_formats.items():
                txt += f"{k} - {v} | "
            reply_text += '\n\n course_name : ' + course['course_name']
            reply_text += '\n course_code : ' + course['course_code']
            reply_text += '\n course_description : ' + course['course_description']
            reply_text += f"\n available in : " + txt
            reply_text += f"\n ___________{course['course_code']}__________"
            reply_text += f"\n Fantastic Now Send Files Releted to This 👆 Course  - ! "
            # query.from_user.send_message(reply_text)
            query.edit_message_text(text = reply_text)
            return RECIVE
    else:
        MSG = f"Invalid Course code: {query.data} \n make sure that all characters are correct"
        keyboard = [
            
            [ InlineKeyboardButton("Back", callback_data=str(START)),]


        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_text = MSG
       
        query.edit_message_text(text= reply_text, reply_markup = reply_markup)
        return SERVE 


def ppt_manager(update: Update, context: CallbackContext):
    global QUERY
    COURSES = QUERY['course']
    if COURSES:
        
        caption_text = f"Course {QUERY['course_code']}"
        caption_text += '\n__________________________________________\n'
        for item in COURSES:
            if item['course_code'] == QUERY['course_code']:
                course = item
                # print(course, 'CO---')

        available_formats = course['available']  
        txt = ''
        for k,v in available_formats.items():
            txt += f"{k} - {v} | "
        caption_text += '\n\n course_name : ' + course['course_name']
        caption_text += '\n course_code : ' + course['course_code']
        caption_text += '\n course_description : ' + course['course_description']
        caption_text += f"\n available in : " + txt
        caption_text += f"\n ___________{course['course_code']}__________"
    msg_id = update.effective_message.message_id
    file_id = update.effective_message.document.file_id 
    file_caption = update.effective_message.caption 
    QUERY['msg_id'] = update.effective_message.message_id
    typ = 'ppt'
    file_obj = {
            "cm": course['course_id'],
            "tg_file_id": str(msg_id) + 'N' + str(update.effective_message.chat_id),
            "tg_file_url": file_id,
            "title": file_caption if file_caption else ""

        }
    fetcher.upload_file(file_obj, typ)
    context.bot.copy_message(chat_id=UDBID,
                    from_chat_id=update.effective_message.chat_id,
                    message_id=update.effective_message.message_id,
                    caption = caption_text)
    
    reply_keyboard = [
                        ['Done'],
                    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Press Done When You Finsh Adding PDF")
    
    QUERY['done_msg'] = f"{course['course_name']} PPT File recived 📚. Thaks {update.message.from_user.first_name} !"
    reply_text = 'is that all you got ??! Press Done, otherwise keep senading 🖖 '
    update.message.reply_text(text =reply_text , reply_markup = reply_markup)
    return RECIVE


def pdf_manager(update: Update, context: CallbackContext):
    global QUERY
    COURSES = QUERY['course']
    if COURSES:
        
        caption_text = f"Course {QUERY['course_code']}"
        caption_text += '\n__________________________________________\n'
        for item in COURSES:
            if item['course_code'] == QUERY['course_code']:
                course = item
                # print(course, 'CO---')

        available_formats = course['available']  
        txt = ''
        for k,v in available_formats.items():
            txt += f"{k} - {v} | "
        caption_text += '\n\n course_name : ' + course['course_name']
        caption_text += '\n course_code : ' + course['course_code']
        caption_text += '\n course_description : ' + course['course_description']
        # caption_text += f"\n available in : " + txt
        caption_text += f"\n ___________{course['course_code']}__________"
    msg_id = update.effective_message.message_id
    file_id = update.effective_message.document.file_id 
    file_caption = update.effective_message.caption 
    QUERY['msg_id'] = update.effective_message.message_id
    typ = 'pdf'
    file_obj = {
            "cm": course['course_id'],
            "tg_file_id": str(msg_id) + 'N' + str(update.effective_message.chat_id),
            "tg_file_url": file_id,
            "title": file_caption if file_caption else ""

        }
    fetcher.upload_file(file_obj, typ)
    context.bot.copy_message(chat_id=UDBID,
                    from_chat_id=update.effective_message.chat_id,
                    message_id=update.effective_message.message_id,
                    caption = caption_text)
    
    reply_keyboard = [
                        ['Done'],
                    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Press Done When You Finsh Adding PDF")
    
    reply_text = f"{course['course_name']} PDF File recived 📚. Thaks {update.message.from_user.first_name} !"
    QUERY['done_msg'] = reply_text
    # reply_text = 'is that all you got ??! Press Done, otherwise keep senading 🖖 '
    update.message.reply_text(text ='reading ...' , reply_markup = reply_markup)
    return RECIVE


def invalid_data_manager(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(" <strong> Please send a valid data ! </strong> \n\n The only supported file formats are PPT and PDF  \n thank you for your smile 😊 ", parse_mode = ParseMode.HTML)
    return RECIVE 

def feed_back(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(" Please Welcome! \n\n The only thing worse than not requesting feedback is not acting on it. ― Frank Sonnenberg, Listen to Your Conscience: That's Why You Have One ")
    return CUTOMER_SERVICE 

def how_to(update: Update, context: CallbackContext):
    user = update.message.from_user
    reply_text = f"follow The instructions properly\n video guid coming soon!"
    update.message.reply_text(reply_text)


def customer_service_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    text = update.message.text
    user = update.message.from_user
    MSG = f"Feedback from [ \n user_id: {user.id} \n usr_name: @{user.username} \n first_name: {user.first_name} \n last_name: {user.last_name} \n is_bot: {user.is_bot} ] \n starts with mrpguybot"
    MSG += '\n___Feedback-Message___\n'
    MSG += text 
    context.bot.send_message(chat_id= UDBID ,text=MSG)
    reply_text = f"Lots of thanks {user.first_name} for your feedback !"
    update.message.reply_text(
        text = reply_text,
        reply_markup=markup_zero,
    )
    return CHOOSING
   

def end(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text(
        "Use /start to use this bot. Use "
    )

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename='conversationbot')
    updater = Updater(token = TOKEN, persistence = persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # Feed Back|How To
    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    

    download_handeler = ConversationHandler(
        entry_points=[CommandHandler('download', download)],
        states={
     
            CUTOMER_SERVICE: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Find$')),customer_service_information),
                MessageHandler(Filters.regex('^Reset$'), Reset_history),
                MessageHandler(Filters.regex('^Back$'), download),
                MessageHandler(Filters.regex('^Home 🛖$'), start_over),
                CommandHandler('Download', download),
            ],
            CHOOSING: [
                MessageHandler(Filters.regex('^(Semester)$'), semester_choice),
                MessageHandler(Filters.regex('^Department$'), department_choice),
                MessageHandler(Filters.regex('^Reset$'), Reset_history),
                MessageHandler(Filters.regex('^Back$'), download),
                MessageHandler(Filters.regex('^Home 🛖$'), start_over),
                MessageHandler(Filters.regex('^Feed Back$'), feed_back),
                MessageHandler(Filters.regex('^How To$'), how_to),
                CommandHandler('Download', download),
            ],
            TYPING_CHOICE: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Find$')), semester_choice),
                MessageHandler(Filters.regex('^Reset$'), Reset_history),
                MessageHandler(Filters.regex('^Back$'), download),
                MessageHandler(Filters.regex('^Home 🛖$'), start_over),
                MessageHandler(Filters.regex('^Feed Back$'), feed_back),
                MessageHandler(Filters.regex('^How To$'), how_to),
                CommandHandler('Download', download),
            ],
            TYPING_REPLY: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Find$')),received_information),
                MessageHandler(Filters.regex('^Reset$'), Reset_history),
                MessageHandler(Filters.regex('^Back$'), download),
                MessageHandler(Filters.regex('^Home 🛖$'), start_over),
                MessageHandler(Filters.regex('^Feed Back$'), feed_back),
                MessageHandler(Filters.regex('^How To$'), how_to),
                CommandHandler('Download', download),
            ],
            SERVE: [
                MessageHandler(Filters.regex('^Back$'), download),
                MessageHandler(Filters.regex(pattern='^' + 'PPT' + '|' + 'PDF' + '|' + 'Book' + '$'), serve_file),
                MessageHandler(Filters.regex(pattern='^' + '[' + 'A' + '-' + 'Z' + str(0) + '-' + str(9) + ']'  + '{' + str(3) + ',' + '}' + '$'), show_download_option),
                MessageHandler(Filters.regex('^Home 🛖$'), start_over),
                MessageHandler(Filters.regex('^Feed Back$'), feed_back),
                MessageHandler(Filters.regex('^How To$'), how_to),
                CommandHandler('Download', download),
              
            ],
            
            
        },
        fallbacks=[MessageHandler(Filters.regex('^Find$'), find),
        ],
        name="my_astu_enlghten_download",
        persistent=True,
    )
    
    upload_handler = ConversationHandler(
        entry_points=[CommandHandler('share', share)],
        states={

            SEMESTER: [
          
                CallbackQueryHandler(school, pattern='^'  + str(ONE) + '|' + str(TWO) + '|' + str(THREE) + '|' + str(FOUR) + '|' + str(FIVE) + '|' + str(SIX) + '|' + str(SEVEN) + '|' + str(EIGHT) + '|' + str(NINE) + '|' + str(TEN) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(START) + '$'),
            ],
            DEPARTMENT: [
                CallbackQueryHandler(department, pattern='^' + '[' + str(1) + '-' + str(9) + ']' + '+'  + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(START) + '$'),
            ],
            COURSE: [
               
                CallbackQueryHandler(courses, pattern='^' + '[' + str(1) + '-' + str(9) + ']' + '+'  + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(START) + '$'),
              
            ],
            OPTION: [
                CallbackQueryHandler(show_option, pattern='^' + '[' + 'A' + '-' + 'Z' + str(0) + '-' + str(9) + ']'  + '{' + str(3) + ',' + '}' + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(START) + '$'),
            ],
            SERVE: [
                CallbackQueryHandler(recive_file, pattern='^' + 'PPT' + '|' + 'PDF' + '|' + 'Book' + '$'),
                CallbackQueryHandler(show_option, pattern='^' + '[' + 'A' + '-' + 'Z' + str(0) + '-' + str(9) + ']'  + '{' + str(3) + ',' + '}' + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(START) + '$'),
            ],
            RECIVE: [
                MessageHandler(Filters.document.mime_type("application/pdf"),pdf_manager),
                MessageHandler(Filters.document.mime_type("application/pptx"),ppt_manager),
                MessageHandler(~(Filters.document.mime_type("application/pdf") | Filters.document.mime_type("application/pptx") | (~Filters.document)), invalid_data_manager),
                MessageHandler(Filters.regex(pattern='^' + str(START) + '$'),start_over),
                MessageHandler(Filters.regex('^Done$'),start_over),
              
            ],
                

            
        },
        fallbacks=[CommandHandler('share', share)],
        name = 'my_astu_enlghten_upload',
        persistent=True,
    )


    dispatcher.add_handler(CommandHandler("help", help_command))
    # dispatcher.add_handler(MessageHandler(Filters.regex('^Feed Back$'), feed_back))
    dispatcher.add_handler(upload_handler)
    dispatcher.add_handler(download_handeler)
    # dispatcher.add_handler(share_handeler)

    show_history_handler = CommandHandler('show_history', show_history)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(show_history_handler)
    dispatcher.add_handler(start_handler)

    # Start the Bot
    # updater.start_polling()
    
    # Start the Bot on Cloud
    updater.start_webhook(listen="0.0.0.0", port = PORT, url_path = TOKEN, webhook_url = "https://enlightentgbot.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
    
    
    
