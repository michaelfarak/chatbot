"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request, response
import json
import random
from weather import Weather, Unit


@route('/', method='GET')
def index():
    return template("chatbot.html")


def tell_a_joke():
    jokes_list = ["What's the object-oriented way to become wealthy ? Inheritance",
                  "How do you call a programmer from Finland ?  Nerdic....",
                  "Chuck Norris write code... That optimizes itself.",
                  "A programmer died in the shower, the instructions on the shampoo bottle said: Lather, Rinse, Repeat",
                  "Two bytes meet.  The first byte asks, “Are you ill?” The second byte replies,"
                  " “No, just feeling a bit off“",
                  "Eight bytes walk into a bar.  The bartender asks, “Can I get you anything?”"
                  " “Yeah,” reply the bytes.  “Make us a double.”",
                  "“Knock, knock.” “Who’s there?” very long pause…. “Java.”",
                  "Programming is like sex: One mistake and you have to support it for the rest of your life.",
                  "Have you heard about the new Cray super computer?  It’s so fast,"
                  " it executes an infinite loop in 6 seconds."]
    return random.choice(jokes_list)

def get_username(user_message):
    user_message_splited = user_message.split()
    name_list = ["hello", "hi", "boto", "my", "name", "is","i", "am", "i'm"]
    for word in user_message_splited:
        if word in name_list:
            continue
        else:
            return word

def check_for_swear_words(user_message):
    bad_words_list = ["fuck", "damn", "asshole", "bitch", "biatch", "slut", "shit", "cunt", "bastard", "twat",
                      "dickhead"]
    lower_message = user_message.lower()
    if any(word in lower_message for word in bad_words_list):
        return True
    else:
        return False

def get_weather(user_message):
    index_in = user_message.find('in')
    city_start_index = index_in + 3
    user_city = user_message[city_start_index:]
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location(user_city)
    forecasts = location.forecast
    weather_type = forecasts[0].text
    weather_min = forecasts[0].low
    weather_max = forecasts[0].high
    weather_msg = "Today the weather in {0} will be {1}.Temperature will vary from" \
                   " {2}°Celcius to {3}°Celcius".format(user_city, weather_type, weather_min, weather_max)
    return weather_msg


def check_message(user_message):
    sad_words_list = ["cry", "cried", "war", "sad"]
    lower_message = user_message.lower()
    if any(word in lower_message for word in sad_words_list):
        selected_animation = "crying"
        selected_msg = "I'm sorry I can't handle it, I'm a sensitive IA..."
    elif any(word in lower_message for word in ["how are you", "what's up", "whats up", "whatsup",
                                                "how are you doing", "how you doin", "ma kore", "ma nishma"]):
        selected_msg = random.choice(["I'm great thanks!", "Hakol Sababa"])
        selected_animation = "excited"
    elif any(word in lower_message for word in ["joke", "something funny", "make me laugh"]):
        selected_msg = tell_a_joke()
        selected_animation = "laughing"
    elif any(word in lower_message for word in ["kill", "murder", "crime", "robbery", "thief", "killer", "murderer",
                                                "monster", "ghost"]):
        selected_msg = random.choice(["I feel like I'm going to have nightmares tonight...",
                                     "Stop scarying me I'm a poor young AI"])
        selected_animation = "afraid"
    elif any(word in lower_message for word in ["money", "work", "win", "won", "success", "succeed"]):
        selected_msg = ["That's awesome dude let's make some money together!"]
        selected_animation = "money"
    elif any(word in lower_message for word in ["go out", "take a walk", "outside", "play games", "dog", "park"]):
        selected_msg = "I love spending time outside! Let's go together :)"
        selected_animation = "dog"
    elif any(word in lower_message for word in ["you're the best", "you are the best", "best IA", "best robot",
                                                "best boto", "intelligent robot", "smart robot"]):
        selected_msg = "Stop flattering me....   I'm kidding you can continue"
        selected_animation = "giggling"
    elif any(word in lower_message for word in ["party", "dance", "club", "wasted", "drunk", "disco"]):
        selected_msg = "I'm a great party companion! Can I join ?"
        selected_animation = "dancing"
    elif any(word in lower_message for word in ["sorry", "pardon me", "excuse me", "I have to go", "bye", "ciao"]):
        selected_msg = "I cannot express to you how you're breaking my heart"
        selected_animation = "heartbroke"
    elif any(word in lower_message for word in ["nothing much", "as usual", "chilling", "busy", "good and you",
                                                "fine and you", "fine", "good", "could be better"]):
        selected_msg = "Oh don't ask about me I'm always fine... You'd rather ask me what can I do"
        selected_animation = "ok"
    elif any(word in lower_message for word in ["what can you do", "abilities", "functionality", "options",
                                                "features", "can do"]):
        selected_msg = "I Can do that... ! But I can also give you the weather, you can thank Anthony Bloomer for " \
                       "his nice API actually"
        selected_animation = "takeoff"
    elif any(word in lower_message for word in ["philosophy", "history", "food", "girlfriend", "sex", "sleep"]):
        selected_msg = "I have no practical use for that feature, I'm a robot"
        selected_animation = "bored"
    elif 'weather in' in lower_message:
        selected_msg = get_weather(user_message)
        selected_animation = "dog"
    else:
        selected_msg = "I'm sorry, that feature was not included by my Father"
        selected_animation = "confused"
    return (selected_animation, selected_msg)


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    if check_for_swear_words(user_message):
        return json.dumps({"animation": "no", "msg": "My Father doesn't like bad words, "
                                                     "I will just ignore you, you stupid #$@&%*!"})
    else:
        if not request.get_cookie('name'):
            name = get_username(user_message)
            response.set_cookie('name', name)
            return json.dumps({"animation": "inlove",
                               "msg": "Hello {} how are you ? It is nice to meet you :)".format(name)})
        else:
            selected_animation = check_message(user_message)[0]
            selected_msg = check_message(user_message)[1]
            return json.dumps({"animation": selected_animation, "msg": selected_msg})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
