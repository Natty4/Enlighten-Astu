"""
Enlighten-Astu Telegram Bot 
By: Natnael(Mr.PGuy)
From buddies to buddies 
"""

import logging
import os
from uuid import uuid4
from typing import Dict

from telegram import *
from telegram.ext import *
from telegram.utils.helpers import escape_markdown

# import fetcher modul
import fetcher

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
FASTSERVE, FASTSHARE, FASTRECIVE, CUTOMERSERVICE = range(4)

# Callback data
START, END = range(2)
DOWNLOAD = 3333
SHARE = 9999
QUERY = {}
SEMES = { '1': 'Freshman 1st', '2': 'Freshman 2nd', '3': 'Sophomore 1st', '4': 'Sophomore 2nd', '5': 'Junior 1st', '6': 'Junior 2nd', '7': 'Senior 1st', '8': 'Senior 2nd', '9': 'GC 1st', '10': 'GC 2nd'}
CAMPUS = 'ASTU'
SEMESTERS = {}
SCHOOLS = []
NCLOUDX = os.environ.get("NCLOUDX")
NFEEDBACKS = os.environ.get("NFEEDBACKS")
TOKEN = os.environ.get("TOKEN") 
ADMIN = os.environ.get("ADMIN") 
PORT = int(os.environ.get('PORT', '8443'))


    


reply_keyboard_0 = [

    ['Feed Back', 'How To'],
]


markup_zero = ReplyKeyboardMarkup(reply_keyboard_0, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Choose one of the button")



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
 
    reply_text = f" 📖📚📒📕📙📘📗📚📖 \n"
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
            f" any question | Feedback,\nwe would love to hear 🍎"
        )
  
    update.message.reply_text(text=reply_text, reply_markup=markup_zero)
    return FASTSERVE

def start_over(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query:
        user = query.from_user
    else:
        user = update.message.from_user

    reply_text = f" 📖📚📒📕📙📘📗📚📖 \n"
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
            f" any question | Feedback,\nwe would love to hear 🍎"
        )

    if query:
        query.from_user.send_message(text = reply_text, reply_markup = markup_zero)
        return FASTSERVE
    else:
        update.message.reply_text(text=reply_text, reply_markup=markup_zero)
        return FASTSERVE

""" Inline Service Section """

def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    if query == "":
        return
    course = fetcher.get_course_tg(query.upper())
    if course:
        for c in course:
            result = course[c]

        filespdf = result['filespath'].get('PDF', '')
        filesppt = result['filespath'].get('PPT', '')
        print(result, '-----result----')
        [print(cm, '------cm--------') for cm in filespdf]
    else:
        return
    keyboard = [

           [InlineKeyboardButton(' 🧲 More ', switch_inline_query_current_chat=query,), InlineKeyboardButton(' Share 🚀 ', switch_inline_query=query,)]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    results = [
        InlineQueryResultDocument(
            id=str(uuid4()),
            title=query,
            document_url=cm,
            mime_type="application/pdf",
            caption=f"course_code : {result['course_code']} \ncourse_name : {result['course_name']} \ndepartment {result['department']['short_name']} \nsemester : {SEMES[str(result['semester'])]}",
            reply_markup = reply_markup
            ) for cm in filespdf]
    results += [
        InlineQueryResultDocument(
            id=str(uuid4()),
            title=query,
            document_url=cm,
            mime_type="application/pdf",
            caption=f"course_code : {result['course_code']} \ncourse_name : {result['course_name']} \ndepartment {result['department']['short_name']} \nsemester : {SEMES[str(result['semester'])]}",
            reply_markup = reply_markup
            ) for cm in filesppt

    ]

    update.inline_query.answer(results, auto_pagination=True,)




""" Courses Menu Sction """

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



""" Choose Rout Sction """

def download_or_share(update: Update, context: CallbackContext) -> int:
    
    query = update.message
    # query.answer("✨ commingsoon ✨")
    keyboard = [
        [
            InlineKeyboardButton(" ⬇️ Download ", callback_data=str(DOWNLOAD) + 'MrPGuy' + query.text.upper()),
            InlineKeyboardButton("Share ↗️ ", callback_data=str(SHARE) + 'MrPGuy' + query.text.upper()),
        ],
       
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
   
    query.reply_text(
        text=" ✨ Wanna Share or Download ✨ ", reply_markup=reply_markup
    )
    return FASTSERVE




""" Download Sction """


def fast_show_download_option(update: Update, context: CallbackContext):

    query = update.callback_query
    QUERY['course_code'] = query.data.split('MrPGuy')[-1].upper()
    data = fetcher.get_fast(query.data.split('MrPGuy')[-1].upper())
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
            [InlineKeyboardButton(f'{av} ⬇️', callback_data=av + 'MrPGuy' + course['course_code'] )] for av in available_formats
       
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)   

        query.edit_message_text(text= reply_text, reply_markup = reply_markup)
        return FASTSERVE
    else :
        query.from_user.send_message(text=f"Invalid Course code: \"{query.data.split('MrPGuy')[-1]} \n make sure that all characters are correct",)
        return FASTSERVE
  

def fast_serve_file(update: Update, context: CallbackContext):

    query = update.callback_query
    context.bot.sendChatAction(chat_id=query.from_user.id ,action = ChatAction.UPLOAD_DOCUMENT)
    data = fetcher.get_course_tg(query.data.split('MrPGuy')[-1])
    user = query.from_user
    MSG = 'Sending requested files ' + user.first_name
    query.answer("✨" + MSG + "✨")
    if data:
        files = []
        for key,value in data.items():
            files = value['filesid'][query.data.split('MrPGuy')[0]]
        MSG = f"<strong> {value['course_name']} </strong> "
        MSG += '\n__________________________________________\n\n'
        MSG += "<strong>course_name </strong>: " + f"{value['course_name']} \n"
        MSG += "<strong>course_description </strong>: " + f"{value['course_description']} \n"
        MSG += "<strong>semester </strong>: " + f"{value['semester']} \n"
        MSG += "<strong>department </strong>: " + f"{value['department']['name']} \n"
        MSG += "<strong>contributors </strong>: " + f"{value['created_by'], value['filescontributor'].get('tg_contributor', ' ')} \n"
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
        MSG = f"Invalid Course code: \"{query.data.split('MrPGuy')[-1]}re that all characters are correct"
        reply_text = MSG
       
        update.message.reply_text(text= reply_text)
        return FASTSERVE




""" Upload Sction """

def fast_show_share_option(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    global QUERY
    QUERY['course_code'] = query.data.split('MrPGuy')[-1].upper()
    data = fetcher.get_fast(query.data.split('MrPGuy')[-1].upper())
    COURSES = data
    QUERY['course'] = COURSES
    if COURSES:
        reply_text = f" Course {QUERY['course_code']} "
        reply_text += '\n__________________________________________\n'
        for item in COURSES:
            if COURSES[item]['course_code'] == QUERY['course_code']:
                course = COURSES[item] 

        available_formats = course['ava']  
        txt = ''
        for k,v in available_formats.items():
            txt += f"{k} - {v} | "
        reply_text += '\n\ncourse_name : ' + course['course_name']
        reply_text += '\ncourse_code : ' + course['course_code']
        reply_text += '\ncourse_description : ' + course['course_description']
        reply_text += f"\navailable : " + txt if txt else f"\n available in : " + ' 0 '
        reply_text += f"\n _______ {course['course_code']} _______"
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

        return FASTSHARE
    else:
        query.from_user.send_message(text=f"Invalid Course code: \"{query.data.split('MrPGuy')[-1]}\" \n make sure that all characters are correct",)
        return FASTSHARE

def fast_recive_file(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = query.message.chat
    MSG = 'ready to grab files Mr/Mss' + user.first_name
    query.answer(MSG)

    COURSES = QUERY['course']
    if COURSES:
        reply_text = f" Course {QUERY['course_code']} "
        reply_text += '\n__________________________________________\n'
        for item in COURSES:
            if COURSES[item]['course_code'] == QUERY['course_code']:
                course = COURSES[item] 

        available_formats = course['ava']  
        txt = ''
        for k,v in available_formats.items():
            txt += f"{k} - {v} | "
        reply_text += '\n\ncourse_name : ' + course['course_name']
        reply_text += '\ncourse_code : ' + course['course_code']
        reply_text += '\ncourse_description : ' + course['course_description']
        reply_text += f"\navailable : " + txt if txt else f"\n available in : " + ' 0 '
        reply_text += f"\n _______ {course['course_code']} _______"
        reply_text += f"\n Fantastic Now Send Files Releted to This 👆 Course  - ! "
        query.edit_message_text(text = reply_text)
        return FASTRECIVE
    else:
        MSG = f" 🐙 Oops! somthing wrong happend,  use /start to continue "
        keyboard = [
            
            [ InlineKeyboardButton("Back", callback_data=str(START)),]


        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_text = MSG
       
        query.edit_message_text(text= reply_text, reply_markup = reply_markup)
        return FASTSHARE 

def ppt_manager(update: Update, context: CallbackContext):
    global QUERY
    COURSES = QUERY['course']
    if COURSES:
        
        caption_text = f"Course {QUERY['course_code']}"
        caption_text += '\n__________________________________________\n'
        for item in COURSES:
            if COURSES[item]['course_code'] == QUERY['course_code']:
                course = COURSES[item] 

        available_formats = course['ava']  
        txt = ''
        for k,v in available_formats.items():
            txt += f"{k} - {v} | "
        caption_text += '\n\ncourse_name : ' + course['course_name']
        caption_text += '\ncourse_code : ' + course['course_code']
        caption_text += '\ncourse_description : ' + course['course_description']
        caption_text += f"\navailable : " + txt if txt else f"\n available in : " + ' 0 '
        caption_text += f"\n _______ {course['course_code']} _______"
    msg_id = update.effective_message.message_id
    file_id = update.effective_message.document.file_id 
    file_caption = update.effective_message.caption
    file_from = update.effective_message.from_user 
    QUERY['msg_id'] = update.effective_message.message_id
    typ = 'ppt'
    file_obj = {
            "cm": course['course_id'],
            "tg_file_id": str(file_id),
            "tg_file_url": context.bot.get_file(file_id).file_path,
            "title": file_caption if file_caption else file_from.first_name

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
    return FASTRECIVE

def pdf_manager(update: Update, context: CallbackContext):
    global QUERY
    COURSES = QUERY['course']
    if COURSES:
        
        caption_text = f"Course {QUERY['course_code']}"
        caption_text += '\n__________________________________________\n'
        for item in COURSES:
            if COURSES[item]['course_code'] == QUERY['course_code']:
                course = COURSES[item] 

        available_formats = course['ava']  
        txt = ''
        for k,v in available_formats.items():
            txt += f"{k} - {v} | "
        caption_text += '\n\ncourse_name : ' + course['course_name']
        caption_text += '\ncourse_code : ' + course['course_code']
        caption_text += '\ncourse_description : ' + course['course_description']
        caption_text += f"\navailable : " + txt if txt else f"\n available in : " + ' 1 '
        caption_text += f"\n _______ {course['course_code']} _______"
    msg_id = update.effective_message.message_id
    file_id = update.effective_message.document.file_id 
    file_caption = update.effective_message.caption 
    file_from = update.effective_message.from_user 
    QUERY['msg_id'] = update.effective_message.message_id
    typ = 'pdf'
    file_obj = {
            "cm": course['course_id'],
            "tg_file_id": str(file_id),
            "tg_file_url": context.bot.get_file(file_id).file_path,
            "title": file_caption if file_caption else file_from.first_name

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
    
    reply_text = f" {course['course_name']} PDF File recived 📚. Thanks {update.message.from_user.first_name} !\n"
    QUERY['done_msg'] = reply_text
    update.message.reply_text(text ='reading ...' , reply_markup = reply_markup)
    return FASTRECIVE

def invalid_data_manager(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(" <strong> Please send a valid data ! </strong> \n\n The only supported file formats are PPT and PDF  \n thank you for your smile 😊 ", parse_mode = ParseMode.HTML)
    return FASTRECIVE 




""" Customers Service Section """

def feed_back(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(" Please Welcome! \n\n The only thing worse than not requesting feedback is not acting on it. ― Frank Sonnenberg, Listen to Your Conscience: That's Why You Have One ")
    return CUTOMERSERVICE 

def how_to(update: Update, context: CallbackContext):
    user = update.message.from_user
    reply_text = f"follow The instructions properly\n video guide coming soon!"
    update.message.reply_text(reply_text)

def customer_service_information(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    user = update.message.from_user
    MSG = f"Feedback from [ \n user_id: {user.id} \n usr_name: @{user.username} \n first_name: {user.first_name} \n last_name: {user.last_name} \n is_bot: {user.is_bot} ] \n starts with mrpguybot"
    MSG += '\n___Feedback-Message___\n\n '
    MSG += text 
    context.bot.send_message(chat_id = NFEEDBACKS, text=MSG)
    reply_text = f"Thanks for your feedback, 🧡 {user.first_name} "
    update.message.reply_text(
        text = reply_text,
        reply_markup=markup_zero,
    )
    return FASTSERVE  

def end(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    if query:
        query.answer()
        query.edit_message_text(text="See you next time! /start")
        return ConversationHandler.END
    else:
        update.message.reply_text(text="See you next time! /start")
        return ConversationHandler.END

def help_command(update: Update, context: CallbackContext) -> None:

    update.message.reply_text(
        "Use /start to use this bot. \n for more look the How To section \n for your comment use Feed Back section "
    )

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename='my_astu_enlghten_bot')
    updater = Updater(token = TOKEN, persistence = persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
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


                    download_or_share),
                ],
        states={
     

            FASTSERVE: [
                       
                CommandHandler('list', show_course),
                CommandHandler('start', start), 
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


                    download_or_share),
                CallbackQueryHandler(fast_show_download_option, pattern='^' + str(DOWNLOAD)),
                CallbackQueryHandler(fast_show_share_option, pattern='^' + str(SHARE)),
                MessageHandler(Filters.regex('^Feed Back$'), feed_back),
                MessageHandler(Filters.regex('^How To$'), how_to),
                

            ],
     

            FASTSHARE: [

                CallbackQueryHandler(fast_recive_file, pattern='^' + 'PPT' + '|' + 'PDF' + '|' + 'Book' + '$'),
                CallbackQueryHandler(fast_show_share_option, pattern='^' + '[' + 'A' + '-' + 'Z' + str(0) + '-' + str(9) + ']'  + '{' + str(3) + ',' + '}' + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(START) + '$'),
                MessageHandler(Filters.regex('^Feed Back$'), feed_back),
                MessageHandler(Filters.regex('^How To$'), how_to),
                
               

            ],
            FASTRECIVE: [
                
                MessageHandler(Filters.document.mime_type("application/pdf"),pdf_manager),
                MessageHandler((Filters.document.mime_type("application/vnd.ms-powerpoint") | Filters.document.mime_type("application/vnd.openxmlformats-officedocument.presentationml.presentation")),ppt_manager),
                MessageHandler(~(Filters.document.mime_type("application/pdf") | Filters.document.mime_type("application/vnd.ms-powerpoint") | Filters.document.mime_type("application/vnd.openxmlformats-officedocument.presentationml.presentation") | (~Filters.document)), invalid_data_manager),
                MessageHandler(Filters.regex(pattern='^' + str(START) + '$'),start_over),
                MessageHandler(Filters.regex('^Done$'),start_over),
              
            ],
            CUTOMERSERVICE: [

                MessageHandler(Filters.text & ~(
                                                Filters.command | 
                                                Filters.regex('^Feed Back$') | 
                                                Filters.regex('^How To$') | 
                                                Filters.regex(pattern='^' + '[' + 'A' + '-' + 'Z' + str(0) + '-' + str(9) + ']'  + '{' + str(3) + ',' + '}' + '$')
                                                ), customer_service_information),

            ]
            
            
        },
        fallbacks=[
            CommandHandler('end', end),
        ],
        name="my_astu_enlghten_fast_download",
        persistent=True,
    )




    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(fast_download_handeler)
    dispatcher.add_handler(InlineQueryHandler(inlinequery))



    # Start the Bot
    # updater.start_polling()
    
    # Start the Bot on Cloud
    updater.start_webhook(listen="0.0.0.0", port = PORT, url_path = TOKEN, webhook_url = "https://enlightentgbot.herokuapp.com/" + TOKEN)
    

    updater.idle()


if __name__ == '__main__':
    main()
    
    
    
