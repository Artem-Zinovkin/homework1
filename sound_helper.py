from gtts import gTTS
import playsound


def listen_command():
    return input("введите вашу фразу")

def do_this_command(message):
    message = message.lower()
    if "привет" in message:
        say_messege("привет друг")

    elif "пока" in message:
        say_messege("пока")
        exit()

    else:
        say_messege("команда не распознана")

def say_messege(messege):
    voice = gTTS(messege, lang= "ru")
    file_name = "_audio.mp3"
    voice.save(file_name)
    playsound.playsound(file_name)
    print(messege)

if __name__=='__main__':
    while True:
        command = listen_command()
        do_this_command(command)