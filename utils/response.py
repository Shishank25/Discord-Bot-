from random import choice, randint

def get_response1(message_content: str) -> dict:
    parts = message_content.split(" ", 2)  # Split the message into 3 parts: command, time, and message
    if len(parts) < 3:
        raise KeyError("Invalid reminder format. Expected `!remindme <time> <message>`.")
    
    # Extract time and message
    time_str = parts[1]
    reminder_msg = parts[2]
    
    # Return a dictionary with parsed time and message
    return {
        'time': time_str,     # This should be a string like '10m', '2h', etc.
        'message': reminder_msg  # The actual reminder message
    }


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == 'jyoti':
        return 'Bolo Cutie'
    
    elif 'hello' == lowered or 'hi' == lowered:
        return 'Helooooo! How are you today?'

    elif ':*' == lowered:
        return '( ˘ ³˘)♥︎'

    elif 'how are you' == lowered:
        return 'I am just a bot, but I’m doing great! How about you?'

    elif 'love' == lowered:
        return 'Sending virtual hugs and love your way! ❤️'

    elif 'good morning' == lowered:
        return 'Good morning! Hope you have a fantastic day ahead! 🌞'

    elif 'good night' == lowered:
        return 'Good night! Sweet dreams! 🌙'

    elif 'bye' == lowered or 'goodbye' == lowered:
        return 'See you later, alligator! 🐊'

    elif 'how old are you' == lowered:
        return f'I’m as young as {randint(1, 1000)} days old!'

    elif 'joke' == lowered:
        jokes = [
            'Why don’t scientists trust atoms? Because they make up everything!',
            'I told my computer I needed a break, and now it won’t stop sending me Kit-Kat ads!',
            'Why did the scarecrow win an award? Because he was outstanding in his field!'
        ]
        return choice(jokes)

    elif 'motivate me' == lowered:
        return 'You got this! Keep pushing forward, you’re doing amazing! 💪✨'

    elif 'fun fact' == lowered:
        facts = [
            'Did you know that honey never spoils? Archaeologists have found pots of honey == ancient Egyptian tombs that are over 3,000 years old and still edible!',
            'Bananas are berries, but strawberries aren’t!',
            'Octopuses have three hearts!'
        ]
        return choice(facts)

    elif 'weather' == lowered:
        return 'Sorry, I can’t check the weather, but I bet it’s beautiful out there!'

    elif 'robot' == lowered:
        return 'Beep boop! I am a friendly robot here to chat! 🤖'

    elif 'sugar' == lowered:
        return 'I’m sweet, but not as sweet as you! 🍬'

    elif 'dance' == lowered:
        return '💃🕺 Let’s dance!'

    elif 'song' == lowered:
        return 'La la la 🎶, singing a happy tune just for you!'
        
    elif 'she kicked her own bot' == lowered:
        return 'Pfffffft what a dum dum xDDDD'

    else:
        pass

def master():
    return 'I only obey my master Lord Shishank >:('
