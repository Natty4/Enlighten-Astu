"""
Enlighten-Astu Telegram Bot 
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
INITIAL, SEMESTER, DEPARTMENT, COURSE, OPTION, SERVE, FASTSERVE, LAST, RECIVE  = range(9)

# Callback data
ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, ELEVEN = range(12)
START, END = range(2)
SHARE, FIND = range(2)
CUTOMER_SERVICE, CHOOSING, TYPING_REPLY, TYPING_CHOICE, SERVE = range(5)
RETRIEVE, UPLOAD = range(2)

QUERY = {}
SEMES = { '1': 'Freshman 1st', '2': 'Freshman 2nd', '3': 'Sophomore 1st', '4': 'Sophomore 2nd', '5': 'Junior 1st', '6': 'Junior 2nd', '7': 'Senior 1st', '8': 'Senior 2nd', '9': 'GC 1st', '10': 'GC 2nd'}
RSEMES = { 'Freshman 1st': '1',  'Freshman 2nd': '2',  'Sophomore 1st': '3',  'Sophomore 2nd': '4',  'Junior 1st': '5',  'Junior 2nd': '6',  'Senior 1st': '7',  'Senior 2nd': '8',  'GC 1st': '9',  'GC 2nd': '10'}
CAMPUS = 'ASTU'
SEMESTERS = {}
SCHOOLS = []
NCLOUDX = os.environ.get("NCLOUDX")
TOKEN = os.environ.get("TOKEN") 
ADMIN = os.environ.get("ADMIN") 
PORT = int(os.environ.get('PORT', '8443'))


reply_keyboard_0 = [

    ['Feed Back', 'How To'],
]



markup_zero = ReplyKeyboardMarkup(reply_keyboard_0, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Choose one of the button")

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
    context.bot.send_message(chat_id = NCLOUDX ,text=f"new user [ \n user_id: {user.id} \n usr_name: @{user.username} \n first_name: {user.first_name} \n last_name: {user.last_name} \n is_bot: {user.is_bot} ] \n starts with enlightenastubot")
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
 
    reply_text = f"📖📚📒📕📙📘📗📚📖\n"
    reply_text += f"Hi! {user.first_name} Welcome "
    if context.user_data:
        reply_text += (
            f"Again To Enlighten us too, knowldge shelf. "
        )
    else:
        reply_text += (
            f"To Enlighten us too, knowldge shelf. "
            f" you can download any availabel course materials in your department easly by senading course_code "
            f" or you can see availabel courses list by useing /list command ! \n\n"
            f" any question | Feedback, we would love ro hear 🍎"
        )
  
    update.message.reply_text(text=reply_text, reply_markup=markup_zero)
    return FASTSERVE

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
            f"To Enlighten us too, knowldge shelf. "
            f" you can download any availabel course materials in your department easly by senading course_code "
            f" or you can see availabel courses list by useing /list command ! \n\n"
            f" any question | Feedback, we would love ro hear 🍎"
        )

    if query:
        query.edit_message_text(text = reply_text, reply_markup = markup_zero)
        return ConversationHandler.END
    else:
        update.message.reply_text(text=reply_text, reply_markup=markup_zero)
        return ConversationHandler.END


""" --Download Sction-- """

def download(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user

    reply_text = f"📖📚📒📕📙📘📗📚📖\n"
    reply_text += f"Hi! {user.first_name} Welcome "
    if context.user_data:
        reply_text += (
            f"Again To Enlighten us too, knowldge shelf. "
        )
    else:
        reply_text += (
            f"To Enlighten us too, knowldge shelf. "
            f" you can download any availabel course materials in your department easly by senading course_code "
            f" or you can see availabel courses list by useing /list command ! \n\n"
            f" any question | Feedback, we would love ro hear 🍎"
        )
  
    update.message.reply_text(text=reply_text, reply_markup=markup_zero)
    return ConversationHandler.END

def show_course(update: Update, context: CallbackContext):
    query = update.message
    global QUERY, COURSES
    page = 1
    COURSES = fetcher.get_courses()
    if COURSES:
        courses = fetcher.get_courses_of(COURSES,page)
        keyboard = [

           [InlineKeyboardButton('Next ⏩ ', callback_data= str(int(page) + 1))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_text = f" {SEMES[str(page)]} Courses List "
        reply_text += '\n__________________________________________\n'
        for key,course in courses.items():

            reply_text += 'course_name : ' + course['course_name'] + '\n'
            reply_text += 'course_code : ' + course['course_code'] + '\n'
            reply_text += 'department : ' + str(course['department']['short_name']) + '\n'
            reply_text += 'contributor : ' + course['created_by'] + '\n\n\n'
        reply_text += f'\n\n copy and pase the course_code you want to download .'
        query.reply_text(text=reply_text, reply_markup=reply_markup)

        return FASTSERVE
    else:
        query.from_user.send_message(text=" 🐙 Oops! somthing wrong happend,  use /start to continue ",)
        return FASTSERVE

def paginate_show_course(update: Update, context: CallbackContext):
    query = update.callback_query
    page = query.data
    global COURSES
    try:
        if COURSES:
            pass

    except:
        COURSES = fetcher.get_courses()

    courses = fetcher.get_courses_of(COURSES,page)
    if courses:
        if int(page) < 2 :

            keyboard = [

               [InlineKeyboardButton('Next ⏩ ', callback_data= str(int(page) + 1))]
            ]
        elif int(page) >= 10 :

            keyboard = [

               [InlineKeyboardButton(' ⏪ Preview ', callback_data= str(int(page) - 1))]
            ]
        else:

            keyboard = [

               [InlineKeyboardButton(' ⏪ Preview ', callback_data= str(int(page) - 1)), InlineKeyboardButton('Next ⏩ ', callback_data= str(int(page) + 1))]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_text = f" {SEMES[str(page)]} Courses List "
        reply_text += '\n__________________________________________\n'
        for key,course in courses.items():

            reply_text += 'course_name : ' + course['course_name'] + '\n'
            reply_text += 'course_code : ' + course['course_code'] + '\n'
            reply_text += 'department : ' + str(course['department']['short_name']) + '\n'
            reply_text += 'contributor : ' + course['created_by'] + '\n\n\n'
        reply_text += f'\n\ncopy and paset the course_code you want to download .'
        query.edit_message_text(text=reply_text, reply_markup=reply_markup)

        return FASTSERVE
    else:
        query.from_user.send_message(text=" 🐙 Oops! somthing wrong happend,  use /start to continue ",)
        return FASTSERVE


def fast_show_download_option(update: Update, context: CallbackContext):

    query = update.message
    QUERY['course_code'] = query.text.upper()
    data = fetcher.get_fast(query.text.upper())
    courses = data
    if courses:
        reply_text = f" Course {QUERY['course_code']} "
        reply_text += '\n__________________________________________\n'
        for item in courses:
            if courses[item]['course_code'] == QUERY['course_code']:
                course = courses[item] 

        available_formats = course['ava']  
        txt = ''
        for k,v in available_formats.items():
            txt += f"{k} - {v} | "
        reply_text += '\n\ncourse_name : ' + course['course_name']
        reply_text += '\ncourse_code : ' + course['course_code']
        reply_text += '\ncourse_description : ' + course['course_description']
        reply_text += f"\navailable : " + txt if txt else f"\n available in : " + ' 0 '
        reply_text += f"\n _______ {course['course_code']} _______"
            

        keyboard = [
            [InlineKeyboardButton(f'{av} ⬇️', callback_data=av + 'N' + course['course_code'] )] for av in available_formats
       
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)   

        update.message.reply_text(text= reply_text, reply_markup = reply_markup)
        return FASTSERVE
    else :
        update.message.reply_text(text=f"Invalid Course code: {query.text} \n make sure that all characters are correct",)
        return FASTSERVE
  


def fast_serve_file(update: Update, context: CallbackContext):
    # print(context.user_data, 'Serve File')
    query = update.callback_query
    context.bot.sendChatAction(chat_id=query.from_user.id ,action = ChatAction.UPLOAD_DOCUMENT)
    data = fetcher.get_course_tg(query.data.split('N')[-1])
    user = query.from_user
    MSG = 'Sending requested files ' + user.first_name
    query.answer("✨" + MSG + "✨")
    if data:
        files = []
        for key,value in data.items():
            files = value['files'][query.data.split('N')[0]]
        MSG = f"<strong> {value['course_name']} </strong> "
        MSG += '\n__________________________________________\n\n'
        MSG += "<strong>course_name </strong>: " + f"{value['course_name']} \n"
        MSG += "<strong>course_description </strong>: " + f"{value['course_description']} \n"
        MSG += "<strong>semester </strong>: " + f"{value['semester']} \n"
        MSG += "<strong>department </strong>: " + f"{value['department']['name']} \n"
        MSG += "<strong>contributors </strong>: " + f"{value['created_by']} \n"
        MSG += "<strong>file format </strong>: " + f"{value['ava' ]} "
        MSG += '\n__________________________________________\n'
        query.from_user.send_message( MSG, parse_mode = ParseMode.HTML)
        for file in files:
            file_id = file
            context.bot.send_document(query.from_user.id, file_id)
       
        reply_text = f"Lots of Thank 🙏 for choosing us  {user.first_name}! "
        query.from_user.send_message(reply_text)
        # context.bot.send_message(user.id, reply_text)
        return FASTSERVE
    else:
        MSG = f"Invalid Course code: {query.text} \n make sure that all characters are correct"
        reply_text = MSG
       
        update.message.reply_text(text= reply_text)
        return FASTSERVE





""" --Upload Sction-- """

def upload(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    
    query = update.message
    # query.answer("✨ commingsoon ✨")
    keyboard = [
        [
            InlineKeyboardButton("Continue", callback_data=str(SHARE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
   
    query.reply_text(
        text=" Press Continue to proceed ", reply_markup=reply_markup
    )
    return ConversationHandler.END

def share(update: Update, context: CallbackContext) -> int:
    global DATA
    CAMPUS = 'ASTU'
    DATA = fetcher.get_semesters(CAMPUS)
    SEMESTERS = {}
    SCHOOLS = []
    COURSES = []
    query = update.callback_query
    if query:
        query.answer("✨ sharing is caring ✨")
    if DATA:
        
        global QUERY
        QUERY = {}
        keyboard = [

            [InlineKeyboardButton(DATA[semester]['name'], callback_data=str(DATA[semester]['semes_number'])), InlineKeyboardButton(DATA[semester+1]['name'], callback_data=str(DATA[semester+1]['semes_number']))] for semester in range(0,len(DATA)-1,2)
          
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if query:

            query.edit_message_text(text="Choose your semester ", reply_markup=reply_markup)
        else:
            update.message.reply_text(text="Choose your semester ", reply_markup=reply_markup)
       
        return SEMESTER
    else:
        update.message.from_user.send_message(text=" 🐙 Oops! somthing wrong happend,  use /start to continue ",)
        return ConversationHandler.END

def school(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    global QUERY
    QUERY['semester'] = query.data

    
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
        query.from_user.send_message(text=" 🐙 Oops! somthing wrong happend,  use /start to continue ",)
        return ConversationHandler.END

def department(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    global QUERY
    QUERY['school'] = query.data

    
    SEMESTERS = [semester for semester in DATA if semester['semes_number'] == int(QUERY['semester'])]
 
    for semester in SEMESTERS:
        SCHOOLS = semester['school_in_this_semes']
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
        query.from_user.send_message(text=" 🐙 Oops! somthing wrong happend,  use /start to continue ",)
        return ConversationHandler.END

def courses(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    global QUERY
    QUERY['department'] = query.data

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
        reply_text += f"\n available : " + txt if txt else f"\n available : " + " 0 "
        reply_text += f"\n ___________{course['course_code']}__________"
        QUERY['course_name'] = course['course_name']
        QUERY['course_code'] = course['course_code']
        QUERY['course_description'] = course['course_description']
            

 

        keyboard = [
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

        return SERVE
    else:
        query.from_user.send_message(text=" 🐙 Oops! somthing wrong happend,  use /start to continue ",)
        return ConversationHandler.END

def recive_file(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    data = fetcher.get_course_tg(QUERY['course_code'])
    user = query.message.chat
    MSG = 'ready to grab files Mr/Mss' + user.first_name
    query.answer(MSG)

    if data:

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
            reply_text += f"\n _______ {course['course_code']} _______ "
            reply_text += f"\n Fantastic Now Send Files Releted to This 👆 Course  - ! "
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
            "tg_file_id": str(file_id),
            "tg_file_url": str(msg_id) + 'N' + str(update.effective_message.chat_id),
            "title": file_caption if file_caption else ""

        }
    fetcher.upload_file(file_obj, typ)
    context.bot.copy_message(chat_id=NCLOUDX,
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

        available_formats = course['available']  
        txt = ''
        for k,v in available_formats.items():
            txt += f"{k} - {v} | "
        caption_text += '\n\n course_name : ' + course['course_name']
        caption_text += '\n course_code : ' + course['course_code']
        caption_text += '\n course_description : ' + course['course_description']
        caption_text += f"\n _______ {course['course_code']} _______"
    msg_id = update.effective_message.message_id
    file_id = update.effective_message.document.file_id 
    file_caption = update.effective_message.caption 
    QUERY['msg_id'] = update.effective_message.message_id
    typ = 'pdf'
    file_obj = {
            "cm": course['course_id'],
            "tg_file_id": str(file_id),
            "tg_file_url": str(msg_id) + 'N' + str(update.effective_message.chat_id),
            "title": file_caption if file_caption else ""

        }
    fetcher.upload_file(file_obj, typ)
    context.bot.copy_message(chat_id=NCLOUDX,
                    from_chat_id=update.effective_message.chat_id,
                    message_id=update.effective_message.message_id,
                    caption = caption_text)
    
    reply_keyboard = [
                        ['Done'],
                    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Press Done When You Finsh Adding PDF")
    
    reply_text = f"{course['course_name']} PDF File recived 📚. Thaks {update.message.from_user.first_name} !"
    QUERY['done_msg'] = reply_text
    update.message.reply_text(text ='reading ...' , reply_markup = reply_markup)
    return RECIVE


def invalid_data_manager(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(" <strong> Please send a valid data ! </strong> \n\n The only supported file formats are PPT and PDF  \n thank you for your smile 😊 ", parse_mode = ParseMode.HTML)
    return RECIVE 

def feed_back(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(" Please Welcome! \n\n The only thing worse than not requesting feedback is not acting on it. ― Frank Sonnenberg, Listen to Your Conscience: That's Why You Have One ")
    return FASTSERVE 

def how_to(update: Update, context: CallbackContext):
    user = update.message.from_user
    reply_text = f"follow The instructions properly\n video guid coming soon!"
    update.message.reply_text(reply_text)


def customer_service_information(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    user = update.message.from_user
    MSG = f"Feedback from [ \n user_id: {user.id} \n usr_name: @{user.username} \n first_name: {user.first_name} \n last_name: {user.last_name} \n is_bot: {user.is_bot} ] \n starts with mrpguybot"
    MSG += '\n___Feedback-Message___\n'
    MSG += text 
    context.bot.send_message(chat_id= NCLOUDX ,text=MSG)
    reply_text = f"Lots of thanks {user.first_name} for your feedback !"
    update.message.reply_text(
        text = reply_text,
        reply_markup=markup_zero,
    )
    return FASTSERVE
   

def end(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

def help_command(update: Update, context: CallbackContext) -> None:

    update.message.reply_text(
        "Use /start to use this bot. Use "
    )

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename='my_astu_enlghten_bot')
    updater = Updater(token = TOKEN, persistence = persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # Feed Back|How To
    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    
    fast_download_handeler = ConversationHandler(
        entry_points=[
                        CommandHandler('start', start), 
                        CommandHandler('list', show_course),
                        MessageHandler(
                            Filters.regex(pattern='^' + '[' + 'A' + '-' + 'Z' + str(0) + '-' + str(9) + ']'  + '{' + str(3) + ',' + '}' + '$'
                                ) & ~(


                                   Filters.regex('^Back$') |
                                   Filters.regex('^Home 🛖$') |
                                   Filters.regex('^Feed Back$') |
                                   Filters.regex('^How To$') 

                                ), 


                            fast_show_download_option),
                        ],
        states={
     

            FASTSERVE: [
                        CommandHandler('list', show_course),
                        CallbackQueryHandler(paginate_show_course, pattern='^' + '[' + str(1) + '-' + str(9) + ']' + '+'  + '$'),
                        CallbackQueryHandler(fast_serve_file, pattern='^' + 'PPT' + '|' + 'PDF' + '|' + 'Book' + '$'),
                        MessageHandler(
                            Filters.regex(pattern='^' + '[' + 'A' + '-' + 'Z' + str(0) + '-' + str(9) + ']'  + '{' + str(3) + ',' + '}' + '$'
                                ) & ~(


                                   Filters.regex('^Back$') |
                                   Filters.regex('^Home 🛖$') |
                                   Filters.regex('^Feed Back$') |
                                   Filters.regex('^How To$') 

                                ), 


                            fast_show_download_option),
                        CommandHandler('start', start),
                        MessageHandler(Filters.regex('^Feed Back$'), feed_back),
                        MessageHandler(Filters.regex('^How To$'), how_to),
                        MessageHandler(Filters.text & ~(
                                                        Filters.command | 
                                                        Filters.regex('^Feed Back$') | 
                                                        Filters.regex('^How To$') | 
                                                        Filters.regex(pattern='^' + '[' + 'A' + '-' + 'Z' + str(0) + '-' + str(9) + ']'  + '{' + str(3) + ',' + '}' + '$')
                                                        ), customer_service_information),
                       

            ],
            
            
        },
        fallbacks=[
            CommandHandler('share', upload),
        ],
        name="my_astu_enlghten_fast_download",
        persistent=True,
    )



    upload_handler = ConversationHandler(
        entry_points=[
                        CallbackQueryHandler(share, pattern='^' + str(SHARE) + '$'),
                        CommandHandler('share', share),
                        ],
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
                MessageHandler((Filters.document.mime_type("application/vnd.ms-powerpoint") | Filters.document.mime_type("application/vnd.openxmlformats-officedocument.presentationml.presentation")),ppt_manager),
                MessageHandler(~(Filters.document.mime_type("application/pdf") | Filters.document.mime_type("application/vnd.ms-powerpoint") | Filters.document.mime_type("application/vnd.openxmlformats-officedocument.presentationml.presentation") | (~Filters.document)), invalid_data_manager),
                MessageHandler(Filters.regex(pattern='^' + str(START) + '$'),start_over),
                MessageHandler(Filters.regex('^Done$'),start_over),
              
            ],
                

            
        },
        fallbacks=[
            CommandHandler('start', download),
            CommandHandler('list', download),
            MessageHandler(
                Filters.regex(pattern='^' + '[' + 'A' + '-' + 'Z' + str(0) + '-' + str(9) + ']'  + '{' + str(3) + ',' + '}' + '$'
                    ) & ~(


                       Filters.regex('^Back$') |
                       Filters.regex('^Home 🛖$') |
                       Filters.regex('^Feed Back$') |
                       Filters.regex('^How To$') 

                    ), 


                download),
            MessageHandler(Filters.regex('^Feed Back$'), download),
            MessageHandler(Filters.regex('^How To$'), download),
            MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Feed Back$') | Filters.regex('^How To$')),download),    

        ],
        name = 'my_astu_enlghten_upload',
        persistent=True,
    )




    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(fast_download_handeler)
    dispatcher.add_handler(upload_handler)
    # dispatcher.add_handler(share_handeler)


    # Start the Bot
    # updater.start_polling()
    
    # Start the Bot on Cloud
    updater.start_webhook(listen="0.0.0.0", port = PORT, url_path = TOKEN, webhook_url = "https://enlightentgbot.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
    
    
    
