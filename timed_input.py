from threading import Thread

class TimedInput:
    def __init__(self, message, timeout):
        self.response=None
        thread=Thread(target=self.get_input, args=(message,))
        thread.start()
        # Wait for response
        thread.join(timeout)
        # Close input after timeout
        if self.response is None:
            print('Time\'s up. Initiating not dumping sequence.')
    
    def get_input(self, message):
        self.response=input(message)