import gtts
from playsound import playsound


def playSpeech(text, language):  
    # make request to google to get synthesis
    #tts = gtts.gTTS("Hello world")

    # save the audio file
    #tts.save("hello.mp3")

    # play the audio file
    #playsound("hello.mp3")
    
    # in spanish
    tts = gtts.gTTS(text, lang=language)
    tts.save("sound.mp3")
    playsound("sound.mp3")
