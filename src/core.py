class Core:
    # Static variable declaration
    MAX_DAILY_AMOUNT:float = 3.0
    MAX_HOUR_AMOUNT:float = 1.0
    def __init__(self):
        self.__baseline: float = 0.01         # Baseline injection rate [0.01,0.1]
        self.__bolus: float = 0.2            # Bolus injection amount [0.2,0.5]
        self.__dailyAmount: float = 0.0
        self.__hourAmount: float = 0.0
        self.__baselineStatus: bool = False
        self.__minuteRecord: list[float] = [] # Record the amount injected every minute (Size 60 * 24)

    def set_baseline(self, baseline: float):
        if(baseline < 0.01 or baseline > 0.1):
            return "Baseline injection rate must be between 0.01 and 0.1"
        self.__baseline = baseline
        return "Success Set Baseline to " + str(baseline)

    def set_bolus(self, bolus: float):
        if(bolus < 0.2 or bolus > 0.5):
            return "Bolus injection amount must be between 0.2 and 0.5"
        self.__bolus = bolus
        return "Success Set Bolus to " + str(bolus)
    
    def baselineOn(self):
        self.__baselineStatus = True
    
    def baselineOff(self):
        self.__baselineStatus = False
    
    def validate(self,amount: float)->bool:
        # Check hour limit
        if(self.__hourAmount + amount > Core.MAX_HOUR_AMOUNT):
            return False
        # Check day limit
        if(self.__dailyAmount + amount > Core.MAX_DAILY_AMOUNT):
            return False
        return True

    def updateByMinute(self):
        # Reduce the hour and daily amount
        if(len(self.__minuteRecord) >= 60):
            amount=self.__minuteRecord.pop(0)
            self.__hourAmount -= amount
            if(len(self.__minuteRecord) >= 1440):
                self.__dailyAmount -= amount
        
        # Update Baseline
        if(self.__baselineStatus == True):
            if(self.validate(self.__baseline)):
                self.__minuteRecord.append(self.__baseline)
                self.__hourAmount += self.__baseline
                self.__dailyAmount += self.__baseline
        else: 
            self.__minuteRecord.append(0.0)

    def requestBolus(self):
        if(self.validate(self.__bolus)):
            self.__hourAmount += self.__bolus
            self.__dailyAmount += self.__bolus
            self.__minuteRecord[len(self.__minuteRecord)-1] += self.__bolus
            return True
        return False
        
        


        
        
        

