import sys, pygame
from pygame.locals import *
import os, math, random
import speech_recognition as sr



class introScreen:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Voco') #Title


        #program color panel
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (200,0,0)
        self.light_red = (255,0,0)
        self.YELLOW = (200,200,0)
        self.light_yellow = (255,255,0)
        self.GREEN = (34,177,76)
        self.light_green = (22,222,105)
        self.BLUE = (67,94,132)
        self.light_blue = (114,203,255)
        self.COFFEE = (127,96,57)
        self.light_coffee = (229,173,103)
        self.CYAN = (54,104,127)
        self.light_cyan = (129,208,255)
        self.WINE = (127,0,0)
        self.light_wine = (229,0,0)

        #speech recognition text
        self.recogText = ""
        self.gestTXT = ""
        self.isSpeaking = False
        self.isEndSpeech = False
        self.isGesturing = False
        self.inEndGesturing = False


        #program font panel
        self.font = pygame.font.SysFont("Impact", 20)
        self.smallfont = pygame.font.SysFont("Impact", 25)
        self.medfont = pygame.font.SysFont("Impact", 50)
        self.largefont = pygame.font.SysFont("Impact", 85)

        #program mouse control panel
        self.QUIT = False
        self.mousebutton = None
        self.mousedown = False
        self.mouse_buttons = ["Left Button","Middle Button","Right Button","Wheel Up","Wheel Down"]

        #clock declaration
        self.clock = pygame.time.Clock()

        #initialize system
        self.initialize()


       
    def initialize(self):

        #Setup the pygame screen
        self.screen_width = 1000
        self.screen_height = 700
        self.screen_size = (self.screen_width, self.screen_height)    
        self.screen = pygame.display.set_mode(self.screen_size)

        #setup a generic drawing surface/canvas
        self.canvas = pygame.Surface((self.screen_width, self.screen_height))


        # Load all the images for buttons

        # self.bg = pygame.image.load("image/CMU-Tartan-Digital.png")
        self.bg = pygame.image.load("image/bg_gaussian.png")
        # self.logo = pygame.image.load("image/logo_v2.png")
        self.new_bg = pygame.image.load("image/new_bg.png")
        self.listenicon = pygame.image.load("image/listenicon.png")
        self.listenicon_small = pygame.image.load("image/listenicon_small.png")
        self.speakicon = pygame.image.load("image/speakicon.png")
        self.speakicon_small = pygame.image.load("image/speakicon_small.png")
        self.helpicon = pygame.image.load("image/help.png")
        self.backicon = pygame.image.load("image/back.png")
        self.speechicon = pygame.image.load("image/speech.png")
        self.stopicon = pygame.image.load("image/pause.png")
        self.instruction = pygame.image.load("image/Instruction.png")
        self.gesture = pygame.image.load("image/myo_gestures/double-tap.png")
        # self.tartanhacksicon = pygame.image.load("image/white-tartanhacks.png")
        # self.vocologo = pygame.image.load("image/VocoLogo.png")


        # Make all the buttons
        self.listenbutton = pygame.transform.scale(self.listenicon, (180,180))
        self.listenbutton_small = pygame.transform.scale(self.listenicon_small, (94,94))
        self.speakbutton = pygame.transform.scale(self.speakicon, (157, 157))
        self.speakbutton_small = pygame.transform.scale(self.speakicon_small, (82, 82))
        self.helpbutton = pygame.transform.scale(self.helpicon, (100, 100))
        self.back_button = pygame.transform.scale(self.backicon,(80,80))





    def record_audio(self):
        
        # Record Audio
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if(self.isSpeaking == True):
                print("Say something!")
                audio = r.listen(source)
            else:
                r.stop()

        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`

            self.recogText = r.recognize_google(audio)
            print("You said: " + self.recogText)
        except sr.UnknownValueError:
            print("Could not understand audio")
            self.recogText = "Could not understand audio"
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            self.recogText = "Could not request results from Google Speech Recognition service; {0}".format(e)



    #mouse handler takes care of all the mouse events 
    def mouse_handler(self,event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mousedown = True
            self.mousebutton = event.button  
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mousedown = False
            self.mousebutton = event.button

        self.mouseX, self.mouseY = pygame.mouse.get_pos()
 
        self.show_mousestate()

    #shows the position of the mouse and it's press state
    def show_mousestate(self):
        """Show the mouse position and button press on the screen"""
        if self.mousebutton and self.mousedown:
            info = "Mouse: "+str(self.mouse_buttons[self.mousebutton-1])
        else:
            info = "Mouse: "
        info += "X= "+str(self.mouseX)+" Y: "+str(self.mouseY)

        #NB: for now we clear the canvas with black
        self.canvas.fill(self.BLACK)

        #load font and blit to canvas
        font = pygame.font.Font(None, 20)        
        textimg = font.render(info, 1, self.WHITE)
        self.canvas.blit(textimg, (10, 10))


    # draw general stuff the doesn't need to repaint 
    def draw(self):
        """We use a generic surface / Canvas onto which we draw anything
           Then we blit this canvas onto the display screen"""
        self.screen.blit(self.new_bg, (0, 0))

        self.button("Listen", 320,590,85,85, self.COFFEE, self.light_coffee, action="listen")
        self.button("Speak", 670,590,85,85, self.CYAN, self.light_cyan, action="speak")
        self.button("help", 900,580,53,53, self.COFFEE, self.light_coffee, action="help")


        #display on the screen
        self.screen.blit(self.listenbutton, (230, 500))
        self.screen.blit(self.speakbutton, (591, 511))
        self.screen.blit(self.helpbutton, (850, 530))
    #customized button class (the main splashscreen and levelSelect all share 
    # one button class to maximize code reuse)
    def button(self, text, x, y, width, height, inactive_color, active_color, action = None):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if(abs(cur[0]-x)<width and abs(cur[1]-y)<height):
            
            pygame.draw.circle(self.screen, active_color, (x,y), width)
            if click[0] == 1 and action != None:
                if action == "quit":
                    pygame.quit()
                    quit()

                if action == "listen":
                    self.listenScreen()
                    
                    print("This is Listen Mode")

                if action == "speak":
                    self.speakScreen()
                    
                    print("This is Speak Mode")

                if action == "help":
                    self.helpScreen()
                    
                    print("This is help Mode")

                if action == "backFromListen":
                    print("This is back")
                    myWelcomScreen = introScreen()
                    myWelcomScreen.run()

                if action == "backFromSpeak":
                    print("This is back")
                    myWelcomScreen = introScreen()
                    myWelcomScreen.run()

                if action == "startspeech":
                    print("Start of Recognition")
                    self.isSpeaking = True
                    self.record_audio()

                if action == "stopspeech":
                    print("End of the Recognition")
                    self.isSpeaking = False
                    self.isEndSpeech = True

                if action == "startGesture":
                    print("Start of the gesture")
                    # call the gesture recognition function

                if action == "endGesture":
                    print("End of the of gesture")


                
        else:
            # the button returns to the unselected state
            pygame.draw.circle(self.screen, inactive_color, (x,y), width)


    # helper function to format text objects 
    def text_objects(self, text, color,size = "small"):

        if size == "small":
            textSurface = self.smallfont.render(text, True, color)
        if size == "medium":
            textSurface = self.medfont.render(text, True, color)
        if size == "large":
            textSurface = self.largefont.render(text, True, color)

        return textSurface, textSurface.get_rect()

    # helper function to fomat button 
    def text_to_button(self, msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
        textSurf, textRect = self.text_objects(msg,color,size)
        textRect.center = (buttonx, buttony)
        self.screen.blit(textSurf, textRect)

    # helper function to format text
    def message_to_screen(self,msg,color, y_displace = 0, size = "small"):
        textSurf, textRect = self.text_objects(msg,color,size)
        textRect.center = (int(1300 / 2), int(700 / 2)+y_displace)
        self.screen.blit(textSurf, textRect)

    # Listen Mode is for hearing impaired individuals to read transcribed words 
    def listenScreen(self):
        gcont = True

        while gcont:
            for event in pygame.event.get():
                    #print(event)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()


            self.screen.blit(self.bg, (0,0))
            
            self.button("back", 75,588,46,46, self.WINE, self.light_wine, action="backFromListen")
            self.button("Speak", 73,490,46,46, self.CYAN, self.light_cyan, action="speak")      

            listenScreenText = self.largefont.render("Listen Mode",True, self.WHITE)
            self.screen.blit(listenScreenText, [300,50])

            self.button("Start1", 320,590,46,46, self.WINE, self.light_wine, action="startGesture")
            self.screen.blit(self.gesture,[282,550])

            self.button("End1", 670,590,46,46, self.CYAN, self.light_cyan, action="endGesture") 
            self.screen.blit(self.stopicon, [647, 565])

            self.screen.blit(self.back_button, (35, 548))
            self.screen.blit(self.speakbutton_small, (32, 448))
            

            if(self.isGesturing == False):
                starterText = self.smallfont.render("Please hit Record to start your sign language. Press stop when finished.", True, self.WHITE)
                self.screen.blit(starterText,[100,150]) 

            recognizingText = self.smallfont.render("", True, self.WHITE)
            if(self.isGesturing == True):
                recognizingText = self.smallfont.render("Recognizing your sign...", True, self.WHITE)
                self.screen.blit(recognizingText,[100,200]) 

            gestureText = self.medfont.render(self.gestTXT, True, self.WHITE)
            self.screen.blit(gestureText,[100,300]) 

            if(self.inEndGesturing == True):
                endText = self.smallfont.render("Pausing your gesture...", True, self.WHITE)
                self.screen.blit(recognizingText,[100,200]) 
            


            pygame.display.update()

            self.clock.tick(15)

    # Speaking Mode is for hearing impaired individuals to translate their sign language.
    def speakScreen(self):
        gcont = True

        while gcont:
            for event in pygame.event.get():
                    #print(event)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
            
            self.screen.blit(self.bg, (0,0))

            self.button("back", 75,588,46,46, self.WINE, self.light_wine, action="backFromSpeak")
            self.screen.blit(self.back_button, (35, 548))
            
            self.button("Listen", 75,490,46,46, self.COFFEE, self.light_coffee, action="listen")
            self.screen.blit(self.listenbutton_small, (28, 442))

            speakScreenText = self.largefont.render("Speech Mode",True, self.WHITE)
            self.screen.blit(speakScreenText, [300,50])
            
            self.button("Start", 320,590,46,46, self.WINE, self.light_wine, action="startspeech")
            self.screen.blit(self.speechicon,[297,565])
            self.button("End", 670,590,46,46, self.CYAN, self.light_cyan, action="endspeech") 
            self.screen.blit(self.stopicon, [647, 565])



            if(self.isSpeaking == False):
                starterText = self.smallfont.render("Please hit Record to start speech recognition. Press stop when finished.", True, self.WHITE)
                self.screen.blit(starterText,[100,150]) 

            recognizingText = self.smallfont.render("", True, self.WHITE)
            if(self.isSpeaking == True):
                recognizingText = self.smallfont.render("Recognizing your speech...", True, self.WHITE)
                self.screen.blit(recognizingText,[100,200]) 

            recognitionText = self.medfont.render(self.recogText, True, self.WHITE)
            self.screen.blit(recognitionText,[100,300]) 

            if(self.isEndSpeech == True):
                endText = self.smallfont.render("Pausing your speech...", True, self.WHITE)
                self.screen.blit(recognizingText,[100,200]) 
            
            pygame.display.update()

            self.clock.tick(15)

    # Help Mode is for instructions of how to use the program
    def helpScreen(self):
        gcont = True

        while gcont:
            for event in pygame.event.get():
                    #print(event)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

            self.screen.blit(self.instruction, [0,0])

            self.button("back", 75,588,46,46, self.WINE, self.light_wine, action="backFromSpeak")
            self.screen.blit(self.back_button, (35, 548))

            

            pygame.display.update()

            self.clock.tick(15)

    # This is the main run function of the splashscreen
    def run(self):
        """This method provides the main application loop.
           It continues to run until either the ESC key is pressed
           or the window is closed
        """
        while True:
            
            events = pygame.event.get()
            for e in events:
                #pass event onto mouse handler only if something happens
                self.mouse_handler(e)
                
                #Set quit state when window is closed
                if e.type == pygame.QUIT :
                    self.QUIT = True
                if e.type == KEYDOWN:
                    #Set quit state on Esc key press
                    if e.key == K_ESCAPE:
                        self.QUIT = True
                                    
            if self.QUIT:
                #Exit pygame gracefully
                pygame.quit()
                sys.exit(0)

            #Process any drawing that needs to be done
            self.draw()

            #flip the display
            pygame.display.flip()

if __name__ == "__main__":
    myWelcomScreen = introScreen()
    myWelcomScreen.run()

        