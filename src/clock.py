class Clock:
    def __init__(self):
        self.hour = 0
        self.minute = 0

    def update(self):
        self.minute += 1
        if(self.minute == 60):
            self.minute = 0
            self.hour += 1
            if(self.hour == 24):
                self.hour = 0
    
    def getMinute(self)->int:
        return self.minute
    def getHour(self)->int:
        return self.hour
    