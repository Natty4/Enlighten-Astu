"""
ASTU 2022
Enlighten Telegram BOT
BY: Natnael(MrPGuy)
Free Book Store
"""
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler, 
    Filters,
)
import fetcher
import os
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
INITIAL, SEMESTER, DEPARTMENT, COURSE,OPTION, SERVE, LAST  = range(7)

# Callback data
ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, ELEVEN = range(12)
START, END = range(2)
RETRIEVE, UPLOAD = range(2)
SEMES ={ '1': 'Freshman 1st', '2': 'Freshman 2nd', '3': 'Sophomore 1st', '4': 'Sophomore 2nd', '5': 'Junior 1st', '6': 'Junior 2nd', '7': 'Senior 1st', '8': 'Senior 2nd', '9': 'GC 1st', '10': 'GC 2nd'}
QUERY = {}
TOKEN = os.environ.get("TOKEN") 
ID = os.environ.get("ID") 
PORT = int(os.environ.get('PORT', '8443'))
def start(update: Update, context: CallbackContext) -> int:
    QUERY = {}
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    context.bot.send_message(chat_id=ID ,text=f"new user [ \n user_id: {user.id} \n usr_name: @{user.username} \n first_name: {user.first_name} \n is_bot: {user.is_bot} ] \n starts with transtobot")
    context.bot.send_message(chat_id=ID ,text=f'{update}')
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Get CM ⬇️", callback_data=str(RETRIEVE)),
            InlineKeyboardButton("Share ↗️", callback_data=str(UPLOAD)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(text="Welcom to ASTU ENLIGHTENMENT \n Morthan 20000 files 1100< users", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return INITIAL


def start_over(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    QUERY = {}
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Get CM ⬇️", callback_data=str(RETRIEVE)),
            InlineKeyboardButton("Share ↗️", callback_data=str(UPLOAD)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(text="Welcom back 🙋‍♂️ {query.from_user.first_name} to Enlighten ASTU  \n Morthan 20000 files 1100< users are in this platform !", reply_markup=reply_markup)
    return INITIAL


def upload(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    QUERY = {}
    query = update.callback_query
    query.answer("✨ commingsoon ✨")
    keyboard = [
        [
            InlineKeyboardButton("Get CM ⬇️", callback_data=str(RETRIEVE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
   
    query.edit_message_text(
        text="Component under 🚧 Construction 🚧, commingsoon! ", reply_markup=reply_markup
    )
    return INITIAL




CAMPUS = 'ASTU'
SEMESTERS = {}
SCHOOLS = []
COURSES = []
DATA = fetcher.get_semesters(CAMPUS)
def retrieve(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    if DATA:
        query = update.callback_query
        query.answer()
        QUERY = {}
        keyboard = [

            [InlineKeyboardButton(DATA[semester]['name'], callback_data=str(DATA[semester]['semes_number'])), InlineKeyboardButton(DATA[semester+1]['name'], callback_data=str(DATA[semester+1]['semes_number']))] for semester in range(0,len(DATA)-1,2)
          
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text=" Choose your semester", reply_markup=reply_markup
        )
        return SEMESTER
    else:
        keyboard = [
        [
        InlineKeyboardButton("Home 🛖", callback_data=str(START)),
        ],

        ]

        reply_markup = InlineKeyboardMarkup(keyboard) 
        query.from_user.edit_message_text(text=f"Oops something wrong \n\n use /start command to continue", reply_markup = reply_markup)
        return INITIAL




def school(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
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
            text="Choose your School", reply_markup=reply_markup)

        return DEPARTMENT
    else:
        keyboard = [
        [
        InlineKeyboardButton("Home 🛖", callback_data=str(START)),
        ],

        ]

        reply_markup = InlineKeyboardMarkup(keyboard) 
        query.from_user.edit_message_text(text=f"Oops some Thing wrong \n\n use /start command to continue", reply_markup = reply_markup)
        return INITIAL


def department(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    QUERY['school'] = query.data
    
    
    
    
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
        keyboard = [
        [
        InlineKeyboardButton("Home 🛖", callback_data=str(START)),
        ],

        ]

        reply_markup = InlineKeyboardMarkup(keyboard) 
        query.from_user.edit_message_text(text=f"Oops some Thing wrong \n\n use /start command to continue", reply_markup = reply_markup)
        return INITIAL


def courses(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
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
            reply_text += 'author : ' + course['created_by'] + '\n\n\n'
        
        query.edit_message_text(text=reply_text, reply_markup=reply_markup)

        return OPTION
    else:
        keyboard = [
        [
        InlineKeyboardButton("Home 🛖", callback_data=str(START)),
        ],

        ]

        reply_markup = InlineKeyboardMarkup(keyboard) 
        query.edit_message_text(text=f"No courses in {QUERY['department']} yet  \n\n use /start command to continue", reply_markup = reply_markup)
        return INITIAL

def show_option(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
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
            

 

        keyboard = [
        [InlineKeyboardButton(f"{av} ⬇️", callback_data=str(av)) for av in available_formats],

        [
        InlineKeyboardButton("Home 🛖", callback_data=str(START)),
        ],

        ]

        reply_markup = InlineKeyboardMarkup(keyboard)    
        query.edit_message_text(text= reply_text, reply_markup = reply_markup)
        return SERVE
    else:
        keyboard = [
        [
        InlineKeyboardButton("Home 🛖", callback_data=str(START)),
        ],

        ]

        reply_markup = InlineKeyboardMarkup(keyboard) 
        query.edit_message_text(text="Oops something Wrong  \n\n use /start command to continue",)
        return INITIAL
 





def quick_access(update: Update, context: CallbackContext)-> int:
    query = update.message
    course_code = query.text
    
    user = query.chat
    available_formats = {}
    data = fetcher.get_fast(course_code)
    if data:
        # files = ['https://www.physics.smu.edu/sekula/phy3305/lecturenotes002.pdf', 'https://personal.tcu.edu/hdobrovolny/GenPhys_notes.pdf', 'http://www.sci.sdsu.edu/johnson/phys564/lecturenotes.pdf']
        reply_text = f"Course {course_code}"
        reply_text += '\n__________________________________________\n'
        for key,val in data.items():
            available_formats = val['ava']
            txt = ''
            for k,v in available_formats.items():
                txt += f"{k} - {v} | "
            
            reply_text += '\n\n course_name : ' + val['course_name']
            reply_text += '\n course_code : ' + val['course_code']
            reply_text += '\n course_description : ' + val['course_description']
            reply_text += f"\n available in : " + txt
            reply_text += f"\n ___________{val['course_code']}__________"
            

 

        keyboard = [
        [InlineKeyboardButton(f"{av} ⬇️", callback_data=str(av)) for av in available_formats],

        [
        InlineKeyboardButton("Home 🛖", callback_data=str(START)),
        ],

        ]

        reply_markup = InlineKeyboardMarkup(keyboard)    
        context.bot.send_message(user.id, reply_text, reply_markup = reply_markup)
        return SERVE
    else:
        MSG = f"Invalid Course code: {query.text} \n make sure that all characters are correct"
        keyboard = [
            
            [ InlineKeyboardButton("Home 🛖", callback_data=str(START)),]


        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_text = MSG
       
        update.message.reply_text(text= reply_text, reply_markup = reply_markup)
        return INITIAL

def serve_file(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    data = fetcher.get_course(QUERY['semester'], QUERY['department'], QUERY['course_code'])
    user = query.message.chat
    MSG = 'Sending requested files ' + user.first_name
    query.answer(MSG)
    
    if data:
        files = []
        for i,j in data.items():
            files = j['files'][query.data]
        for file in files:
          
            # context.bot.send_message(user.id, file)
            context.bot.send_document(user.id, file)

       
        reply_text = f"Lots of Thank 🙏 for choosing us  {user.first_name}! "
        query.from_user.send_message(reply_text)
        # context.bot.send_message(user.id, reply_text)
        return SERVE
    else:
        MSG = f"Invalid Course code: {query.data} \n make sure that all characters are correct"
        keyboard = [
            
            [ InlineKeyboardButton("Home 🛖", callback_data=str(START)),]


        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_text = MSG
       
        query.edit_message_text(text= reply_text, reply_markup = reply_markup)
        return INITIAL 


def end(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer('session closed')
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text(
        "Use /start to use this bot. \n\n and if face any anomality pleas let us know in the feed back section"
    )

def error(update: Update, context: CallbackContext) -> None:
    """Displays info on error."""
    context.bot.send_message(update.message.chat.id, "Oops an error occurred | 500  \n\n use /start command to start again")

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token = TOKEN,use_context = True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            INITIAL: [
                CallbackQueryHandler(retrieve, pattern='^' + str(RETRIEVE) + '$'),
                CallbackQueryHandler(upload, pattern='^' + str(UPLOAD) + '$'),
            ],
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
                CallbackQueryHandler(serve_file, pattern='^' + 'PPT' + '|' + 'PDF' + '|' + 'Book' + '$'),
                CallbackQueryHandler(show_option, pattern='^' + '[' + 'A' + '-' + 'Z' + str(0) + '-' + str(9) + ']'  + '{' + str(3) + ',' + '}' + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(START) + '$'),
            ],
                
                


            LAST: [
                CallbackQueryHandler(start_over, pattern='^' + str(START) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(END) + '$'),
            ],
            
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, quick_access))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)

    # Start the Bot on Local Machin
    # updater.start_polling()

    # Start the Bot on Cloud
    updater.start_webhook(listen="0.0.0.0", port = PORT, url_path = TOKEN, webhook_url = "https://enlightentgbot.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

