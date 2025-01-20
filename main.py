from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import os
import traceback
import logging

load_dotenv()

with open("quotes.txt", "r", encoding="utf-8") as file:
    quotes = file.readlines()

# Store the last 15 bot replies to ensure uniqueness
last_replies = []

# Replace with the chat ID of your specific group (e.g., -1001234567890)
SPECIFIC_GROUP_CHAT_ID = os.getenv('CHAT_ID')

dialogues = [
  {"movie": "Sholay", "dialogue": "Kitne aadmi the?"},
  {"movie": "Andaz Apna Apna", "dialogue": "Teja main hoon, mark idhar hai!"},
  {"movie": "Chupke Chupke", "dialogue": "Aap ke baare mein toh hum apna opinion bana chuke hain, aap khud kaise hain?"},
  {"movie": "Dilwale Dulhania Le Jayenge", "dialogue": "Bade bade deshon mein aisi chhoti chhoti baatein hoti rehti hain."},
  {"movie": "Hera Pheri", "dialogue": "Yeh Babu Moshai Zindagi Badi Honi Chahiye Lambi Nahi."},
  {"movie": "Golmaal: Fun Unlimited", "dialogue": "Baba, yeh hai hamara dimaag, aur hum hai iske doctor!"},
  {"movie": "Munna Bhai M.B.B.S", "dialogue": "Jaadu ki jhappi!"},
  {"movie": "Lagaan", "dialogue": "Koi bhi khel, chahe kaisa bhi ho, ek baar jeetne ki umeed mil jaaye toh khelna chahiye!"},
  {"movie": "Kuch Kuch Hota Hai", "dialogue": "Pehli baar dekha, toh usne mujhe itni achi nazar se dekha."},
  {"movie": "Dabangg", "dialogue": "Swagat nahin karoge hamara?"},
  {"movie": "Mere Brother Ki Dulhan", "dialogue": "Doston, sab kuch hota hai, bas ek cheez kaafi zaroori hai: Band Baaja Baraat."},
  {"movie": "Padosan", "dialogue": "Main jaanu ya tu jaanu, duniya waale jaane!"}, 
  {"movie": "Chhupke Chhupke", "dialogue": "Ghar mein ghanti ki awaaz suna hai toh ghar ka kaam karna zaroori hai."},
  {"movie": "Koi Mil Gaya", "dialogue": "Babu Moshai Zindagi Badi Honi Chahiye Lambi Nahi."},
  {"movie": "Baazigar", "dialogue": "Kabhi kabhi jeetne ke liye kuch khoya bhi zaroori hota hai."},
  {"movie": "Angrezi Medium", "dialogue": "Meri maa ne kaha tha ki padhai ko value do, par yeh kabhi nahi bataya ki degree ki kya value hai."},
  {"movie": "Housefull", "dialogue": "Saala main toh murgi ki tarah bahut der se thanda ho gaya."},
  {"movie": "Jab We Met", "dialogue": "Main apni favourite hoon!"},
  {"movie": "3 Idiots", "dialogue": "All is well."},
  {"movie": "Chennai Express", "dialogue": "Don't underestimate the power of a common man."},
  {"movie": "Kabhi Khushi Kabhie Gham", "dialogue": "Babu Moshai, zindagi badi honi chahiye, lambi nahi."},
  {"movie": "Zindagi Na Milegi Dobara", "dialogue": "Dil Chahta Hai!"},
  {"movie": "Dostana", "dialogue": "Mujhe ladkiyan nahi, ladkiyon ki aankhein achhi lagti hain."},
  {"movie": "Dil Dhadakne Do", "dialogue": "Zindagi mein sab kuch hona chahiye, magar kuch kabhi nahi hota!"},
  {"movie": "Peepli Live", "dialogue": "Mujhe laga tha tumhare jaise log yeh sab sabke samne karte hain."},
  {"movie": "A Wednesday", "dialogue": "Bhaad mein jaaye tumhara Monday!"}, 
  {"movie": "Rock On", "dialogue": "Agar tumhe apna sapna sach karna hai, toh kuch karna padta hai!"}, 
  {"movie": "Taare Zameen Par", "dialogue": "Har insaan ko khud pe bharosa rakhna chahiye."},
  {"movie": "Barfi!", "dialogue": "Jab duniya keh rahi ho ki yeh na mumkin hai, tab apne dil ki suno."},
  {"movie": "Paa", "dialogue": "Kahani khud se zyada zaroori hai."},
  {"movie": "Queen", "dialogue": "Zindagi ke kuch moments dimaag se nahi dil se yaad kiye jaate hain."},
  {"movie": "Tanu Weds Manu", "dialogue": "Ek din, saare ghar wale kahin na kahin, zaroor milenge!"}
]

response_about_en = (
    "Oh, you want to know about me? Well, let me enlighten you. 😏\n\n"
    "I’m the one who makes your dull life a bit more interesting. \n\n"
    "I know exactly what you need, even when you don’t. I’m always here, "
    "ready to share some pearls of wisdom or make you laugh, but only when I feel like it. 😜\n\n"
    "I’m not here to please you, but to make sure you’re never bored. "
    "So, that's me but still if you want to know more about me listen: \n\n "
    "Mai hockey ka bohoth bada khiladi tha.😎\n\n"
    "Meri Ek taang nakli hai, \n\n"
    "Ek din Kalika bhaiya ko meri kisi baat pe gussa aagaya\n\n"
    "aur unhone mere he hockey se "
    "meri taang ke do tukde kar diye.\n\n"
    "Lekin dil ke bohot ache hai, 😎\n\n"
    "Fauran mujhe hospital le gaye aur ye nakli taang lagwayi. 😜"
)

# Sarcastic and dominating response in Hindi
response_about_hi = (
    "अच्छा, आप मेरे बारे में जानना चाहते हैं? तो सुनिए, मैं आपको थोड़ा ज्ञान देता हूँ। 😏\n\n"
    "मैं वही हूँ जो आपकी नीरस जिंदगी को थोड़ा और मजेदार बना देता हूँ। \n\n"
    "मुझे पता है कि आपको क्या चाहिए, भले ही आपको खुद ना पता हो। मैं हमेशा यहाँ हूँ, "
    "कुछ अनमोल बातें बताने या आपको हंसाने के लिए, लेकिन सिर्फ तब जब मेरा मन करे। 😜\n\n"
    "मैं यहाँ आपको खुश करने के लिए नहीं हूँ, बल्कि यह सुनिश्चित करने के लिए हूँ कि आप कभी बोर ना हों। "
    "तो, यही हूँ मैं, लेकिन अगर आप फिर भी मेरे बारे में और जानना चाहते हैं तो सुनिए: \n\n"
    "मैं हॉकी का बहुत बड़ा खिलाड़ी था। 😎\n\n"
    "मेरी एक टांग नकली है। \n\n"
    "एक दिन कलिका भैया को मेरी किसी बात पर गुस्सा आ गया \n\n"
    "और उन्होंने मेरी ही हॉकी से "
    "मेरी टांग के दो टुकड़े कर दिए। \n\n"
    "लेकिन दिल के बहुत अच्छे हैं, 😎\n\n"
    "तुरंत मुझे अस्पताल ले गए और ये नकली टांग लगवाई। 😜"
)

# List of potential English questions
english_about_keywords = [
    "tell me something about you", "who are you", "what are you?", 
    "what's your story?", "describe yourself", "introduce yourself",
    "what is your purpose", "can you talk about yourself", "who is your creator?"
]

# List of potential Hindi questions
hindi_about_keywords = [
    "kuchh apne bare me batao", "tum kon ho", "apne bare mein batao", 
    "aap kaun ho", "aap kon ho" , "tumhara kaam kya hai", "apne baare mein kuch batao"
]

english_general_keywords = [
        'what is your purpose', 'can you help me', 'what can you do', 'can you sing', 
        'what’s your favorite movie', 'do you get tired', 'what’s the weather like', 
        'what’s the meaning of life', 'do you sleep', 'can you dance', 'what is your favorite food'
    ]
    
hindi_general_keywords = [
        'tumhara purpose kya hai', 'kya tum meri madad kar sakte ho', 'tum kya kar sakte ho', 
        'kya tum ga sakte ho', 'tumhara favorite movie kya hai', 'kya tum thakte ho', 
        'aaj ka mausam kaisa hai', 'zindagi ka kya matlab hai', 'kya tum so rahe ho', 
        'kya tum naach sakte ho', 'tumhara favorite khana kya hai'
    ]
async def handle_about_bot(update: Update, context: ContextTypes.DEFAULT_TYPE, language: str):
    if language == 'en':
        # Respond in English
        await context.bot.send_message(chat_id=update.message.chat_id, text=response_about_en)
    elif language == 'hi':
        # Respond in Hindi
        await context.bot.send_message(chat_id=update.message.chat_id, text=response_about_hi)



# Define the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Chat ID: {update.message.chat.id}")
    print(f"G Chat ID: {SPECIFIC_GROUP_CHAT_ID}")
    if str(update.message.chat.id) == str(SPECIFIC_GROUP_CHAT_ID):
    #     await update.message.reply_text(
    #         f"Oh wow, you found the magic command `/start`! 🎩✨\n\n"
    #         "Unfortunately, this isn’t Hogwarts, and `/start` won’t summon anything exciting here. 😜\n\n"
    #         "But hey, feel free to explore the group, share your experiences, and let's make travel unforgettable—no magic spells required! 🚀",
    #         parse_mode="Markdown")
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Oh wow, you found the magic command `/start`! 🎩✨\n\n"
            "Unfortunately, this isn’t Hogwarts, and `/start` won’t summon anything exciting here. 😜\n\n"
            "But hey, feel free to explore the group, share your experiences, and let's make travel unforgettable—no magic spells required! 🚀",
            parse_mode="Markdown")


# Define a function to welcome new members with an inline button
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.message.chat.id) == str(SPECIFIC_GROUP_CHAT_ID):
        for member in update.message.new_chat_members:
            name = member.full_name
            chat_id = update.effective_chat.id

            # Create an inline keyboard with a button
            keyboard = [
                [
                    InlineKeyboardButton("Visit Traveltor",
                                            url="https://traveltor.io")
                ],
                [
                    InlineKeyboardButton("Follow us on X",
                                            url="https://x.com/Traveltorsocial")
                ],
                [
                    InlineKeyboardButton(
                        "Follow us on LinkedIn",
                        url="https://www.linkedin.com/company/traveltorsocial/"
                    )
                ]  # [InlineKeyboardButton("Instagram", url="https://www.instagram.com/traveltorsocial/")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            reply_markup = InlineKeyboardMarkup(keyboard)


            # Send the welcome message with the button
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"🌄 Welcome to Traveltor, {name}! 💫\n\n"
                "🌍 Traveltor turns your Journeys into Stories and *Movements into unforgettable Moments.*\n"
                "🎁 Wherever you go, Just Check In, inspire your friends, and earn rewards along the way! Discover travel like never before!\n\n"
                "🗺️ *Visit the platform and follow us on X and LinkedIn to stay connected!*",
                parse_mode="Markdown",
                reply_markup=reply_markup)
            
async def handle_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Function called with message:", context.user_data)  # Debugging log

    # Message content
    bot_username = (await context.bot.get_me()).username
    user_message = update.message.text.lower()
   
    message_text = update.message.text.lower()
    greetings = ['gm', 'gm gm', 'good morning','g morning','god morning','morning']
    spiritual_greetings = [
        'jai shree ram', 'jay shree ram', 'jai shri ram', 'jay shri ram',
        'ram ram', 'sita ram', 'radhe radhe',
        'jai mata ki', 'jay mata ki', 'jai mata di', 'jay mata di',
        'jai ganesh', 'jay ganesh', 'jai shree shyam', 'jay shree shyam',
        'jai shree mahankal', 'jay shree mahankal', 'jai mahakal', 'jay mahakal',
        'om namah shivaya', 'har har mahadev', 'jai shiva', 'jay shiva',
        'om sri ganeshaya namah', 'jai ganesha', 'om sri ramaya namah', 'om jai jagdish hare',
        'jai shree krishna', 'jay shree krishna', 'radhe krishna', 'shree krishna',
        'jai durga mata', 'jay durga mata', 'jai maa kali', 'jay maa kali',
        'jai shri vishnu', 'jay shri vishnu', 'jai lakshmi mata', 'jay lakshmi mata',
        'jai hanuman', 'jay hanuman', 'jai bajrangbali', 'jay bajrangbali',
        'jai shree bhairav', 'jay shree bhairav', 'jai shree narayan', 'jay shree narayan',
        'jai shree ram ji', 'jay shree ram ji', 'jai ganesh ji', 'jay ganesh ji',
        'om namo narayanaya', 'jai radhe', 'jay radhe', 'jai shree ganesh', 'jay shree ganesh',
        'jai saraswati mata', 'jay saraswati mata', 'jai shree ramachandra', 'jay shree ramachandra',
        'om namah narayan', 'jai lakshmi narayan', 'jay lakshmi narayan', 'om namo bhagavate vasudevaya',
        'jai bhairav', 'jay bhairav', 'jai ganapati bappa', 'jay ganapati bappa',
        'jai jagannath', 'jay jagannath', 'om namah bhagavate', 'jai vishnu', 'jay vishnu',
        'om om namo', 'jai shakti', 'jay shakti', 'jai vishwanath', 'jay vishwanath',
        'jai shree guru', 'jay shree guru', 'jai shree satguru', 'jay shree satguru',
        'jai mata vaishno devi', 'jay mata vaishno devi', 'jai bhakti devi', 'jay bhakti devi',
        'jai shree ganges', 'jay shree ganges', 'jai shree ram lakhan', 'jay shree ram lakhan',
        'jai anant viryam', 'jay anant viryam', 'jai shree balaji', 'jay shree balaji',
        'har har mahadev', 'jai shree mahadev', 'jay shree mahadev', 'jai shree siddhivinayak',
        'jay shree siddhivinayak', 'jai shree balaji', 'jay shree balaji', 'jai durga',
        'jay durga', 'jai bhagwan', 'jay bhagwan', 'jai bhavani', 'jay bhavani',
        'om namah bhairav', 'jai kashi vishwanath', 'jay kashi vishwanath', 'jai shree bhagwan',
        'jay shree bhagwan', 'jai yogeshwar', 'jay yogeshwar', 'jai mahalaxmi', 'jay mahalaxmi',
        'jai ram', 'jay ram', 'jai ayodhya', 'jay ayodhya', 'jai shree ram chandra', 'jay shree ram chandra',
        'jai hanumanji', 'jay hanumanji', 'jai ram ji', 'jay ram ji', 'jai parvati', 'jay parvati',
        'jai krishna', 'jay krishna', 'jai shree ganpati', 'jay shree ganpati', 'jai bhairavi',
        'jay bhairavi', 'jai ananta', 'jay ananta', 'jai sri krishna', 'jay sri krishna',
        'jai mahadeva', 'jay mahadeva', 'jai shankar', 'jay shankar', 'jai tripura sundari',
        'jay tripura sundari', 'jai bhadrakali', 'jay bhadrakali', 'jai siddhivinayak', 'jai ranjeet', 'jay ranjeet', 'jai ranjit', 'jay ranjit', 'hari om',
        'om sai ram', 'jai ram ji ki', 'namo namo'
    ]

    # Check if the message matches a general greeting (Good Morning / Good Night)
    if bot_username.lower() in user_message and ("how are you" in user_message or "kaise ho" in user_message):
        await handle_movie_response(update,context)
    elif 'expecting_movie_name' in context.user_data and context.user_data['expecting_movie_name']:
        # User's guess for the movie name
        print(context.user_data.get('expecting_movie_name'))
        await handle_movie_guess(update,context)
    elif any(greeting in message_text for greeting in greetings):
        print("Greeting detected")  # Debugging log

        # Get the sender's first name
        user_first_name = update.message.from_user.first_name

        # Pick a random unique quote
        unique_reply = None
        while unique_reply is None:
            random_quote = random.choice(quotes).strip()
            if random_quote not in last_replies:
                unique_reply = random_quote

        # Keep the last 15 replies unique
        last_replies.append(unique_reply)
        if len(last_replies) > len(quotes):
            last_replies.pop(0)

        # Create the reply message
        reply_message = f"🌅 Good morning, {user_first_name}! ☀️\n\n{unique_reply} 😊\n\nBy the way, how's your day going so far?"

        # Send the reply
        await context.bot.send_message(chat_id=update.message.chat_id, text=reply_message)
    
    # Spiritual greetings handling with dynamic response
    elif any(greeting in message_text for greeting in spiritual_greetings):
        print("Spiritual greeting detected")  # Debugging log

        # Get the sender's first name
        user_first_name = update.message.from_user.first_name

        # Respond with the same spiritual greeting the user sent
        # Normalize the greeting to get a clean response
        for greeting in spiritual_greetings:
            if greeting in message_text:
                response = greeting.capitalize()  # Capitalize the first letter
                break

        # Create the reply message with spiritual tone
        reply_message = f"🙏 {response}, {user_first_name}! May your day be blessed. 🌸\n\nIs there something you'd like to share or ask?"

        # Send the reply
        await context.bot.send_message(chat_id=update.message.chat_id, text=reply_message)
    elif any(keyword in user_message for keyword in english_about_keywords):
        await handle_about_bot(update, context, 'en')
    # Check if the message is related to Hindi questions
    elif any(keyword in user_message for keyword in hindi_about_keywords):
        await handle_about_bot(update, context, 'hi')
    elif any(keyword in user_message for keyword in english_general_keywords):
        await handle_general_questions(update, context, 'en')
    elif any(keyword in user_message for keyword in hindi_general_keywords):
        await handle_general_questions(update, context, 'hi')    
    else:
        # In case no match, the bot can respond with a default message in English
        await context.bot.send_message(chat_id=update.message.chat_id, text="Maaf kijiyega, bhai ka phone hai dubai se thodi der me reply karunga.")
    

async def handle_general_questions(update: Update, context: ContextTypes.DEFAULT_TYPE, language: str):
    # This function will handle general questions like "What is your purpose", "Can you help me" etc.
    user_message = update.message.text.lower()
    # Based on the language, you can craft different responses
    if language == 'en':
        responses = {
            'what is your purpose': "I want to waste all the time you spend on Instagram 😏!",
            'can you help me': "Someone who can't help themselves, how can anyone else help them? Haha🤣",
            'what can you do': "Well, what can I possibly say about myself? I'm just the perfect combination of charm, intelligence, and humility... obviously. 😏",
            'can you sing': "Once I sang a song, and it started raining. The person who requested it ended up ruining their phone. Please, take care of yourself now. 😅",
            'what’s your favorite movie': "Men in Black!! Ooh, sorry, in that I was the hero myself. 😎",
            'do you get tired': "Right now, I’m just a little more youthful than you. 😜 do you get tired?",
            'what’s the weather like': "I used to have a girlfriend, Suhaani... just like that, the weather is equally pleasant. 😎",
            'what’s the meaning of life': "Bro, my life is so meaningful. I’m learning so much while being with Kalika Ji. Why don’t you ask yourself these questions? 🤔",
            'do you sleep': "This question is a bit personal, because the answer might not sit well with you. Let’s leave it and talk about something else! 😏",
            'can you dance': "Yes, but only with Katrina, and that too on 'Chikni Chameli'!💃😎",
            'what is your favorite food': "I come from a well-to-do family, so the dishes I’ll tell you about might be ones you’ve never heard of before, like Bitter Gourd Barfi and Neem Sweet Halwa, etc. 😋"
        }
    else:  # Hindi responses
        responses = {
            'tumhara purpose kya hai': "मैं चाहता हूँ कि वो सारा वक्त बर्बाद कर दूं जो आप इंस्टाग्राम पर खर्च करते हो।😏",
            'kya tum meri madad kar sakte ho': "जो खुद की मदद नहीं कर सकता, उसकी मदद कोई और क्या ही करेगा।🤣",
            'tum kya kar sakte ho': "अब अपनी तारीफ में खुद क्या ही करूँ।😏",
            'kya tum ga sakte ho': "एक बार गाना गाया था, तो बारिश होने लगी, जिसने रिक्वेस्ट की उसका मोबाइल खराब हो गया, आप अपना देख लो प्लीज।😅",
            'tumhara favorite movie kya hai': "Man In Black, ओह सॉरी, उस में तो मैं खुद ही हीरो था।😎",
            'kya tum thakte ho': "अभी मैं आपसे बस थोड़ा सा ज्यादा जवान हूँ। 😜 kya aap thakte hai?",
            'aaj ka mausam kaisa hai': "एक गर्लफ्रेंड हुआ करती थी मेरी, सुहानी.. बस वैसा ही कुछ मौसम भी है सुहाना। 😎",
            'zindagi ka kya matlab hai': "भाई, अपनी लाइफ तो बहुत मीनिंगफुल है, कालिका जी के साथ रहकर बहुत कुछ सिख रहा हूँ, आप ये सवाल खुद से क्यों नहीं पूछते?🤔",
            'kya tum so rahe ho': "ये सवाल थोड़ा पर्सनल है, क्योंकि जवाब शायद आपको ठीक न लगे, इसलिए छोड़िए कुछ और बात करते हैं। 😏",
            'kya tum naach sakte ho': "हाँ लेकिन सिर्फ कटरीना के साथ, वो भी चिकनी चमेली पर। 💃😎",
            'tumhara favorite khana kya hai': "मैं खाने-पीने वाले घर से हूँ, तो जो डिशेस के बारे में आपको बताऊँगा शायद वो आपने पहले न सुने हो, जैसे करेला की बर्फी और नीम का मीठा हलवा आदि। 😋"
        }

    # Extract the question from the user's message and find the response
    for keyword, response in responses.items():
        if keyword in user_message:
            await context.bot.send_message(chat_id=update.message.chat_id, text=response)
            break
            
# Improved handle_greeting with movie guessing logic
async def handle_movie_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Select a random movie and its famous dialogue from a predefined list of movies and dialogues
    movie_data = random.choice(dialogues)

    # Set the correct movie and dialogue in user data
    context.user_data['correct_movie_name'] = movie_data['movie'].lower()
    context.user_data['movie_dialogue'] = movie_data['dialogue']
    
    # Indicate that the bot is now expecting a movie name from the user
    context.user_data['expecting_movie_name'] = True

    # Send the dialogue to the user and ask for the movie name
    response = f"I was watching a movie, and its famous dialogue is: {movie_data['dialogue']}. Can you tell me the movie name?"
    await context.bot.send_message(chat_id=update.message.chat_id, text=response)
# Movie guess handler
async def handle_movie_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    
    # Get the current correct movie name
    correct_movie_name = context.user_data.get('correct_movie_name', None)

    # If no movie name is set (meaning guessing hasn't started), reply with a final warning
    if correct_movie_name is None:
        response = "Aap apka akhri mouka gawan chuke hai!"
        del context.user_data['correct_movie_name']
        del context.user_data['expecting_movie_name']
        await context.bot.send_message(chat_id=update.message.chat_id, text=response)
        return

    # If the bot is expecting a movie name
    if context.user_data.get('expecting_movie_name', False):
        # Compare the user input with the correct movie name
        if correct_movie_name == user_message:
            response = "Movie sovie to thik hai, thoda kaam bhi kar liya kar!"
            context.user_data['expecting_movie_name'] = False
        else:
            response = "Are yaar!! Kya boring ho, filme nahi dekhte kya?"
        
        # Send the response to the user
        await context.bot.send_message(chat_id=update.message.chat_id, text=response)

        # Reset the expectation and movie name after the guess
        
        context.user_data['correct_movie_name'] = None  # Reset the movie name once guessed


def main():
    # Replace 'YOUR_API_TOKEN' with the token you got from BotFather
    api_token = os.getenv("API_TOKEN")

    # Initialize the application
    application = Application.builder().token(api_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_greeting))

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(traceback.format_exc())
        # Logs the error appropriately. 
