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
    def get_baseline(self) -> float:
        return self.__baseline
    def get_bolus(self) -> float:
        return self.__bolus
    def get_daily_amount(self) -> float:
        return self.__dailyAmount
    def get_hour_amount(self) -> float:
        return self.__hourAmount
    def get_baseline_status(self) -> bool:
        return self.__baselineStatus
    def set_baseline(self, baseline: float) -> str:
        if(baseline < 0.01 or baseline > 0.1):
            return "Baseline injection rate must be between 0.01 and 0.1"
        self.__baseline = baseline
        return "Success Set Baseline to " + str(baseline)

    def set_bolus(self, bolus: float) -> str:
        if(bolus < 0.2 or bolus > 0.5):
            return "Bolus injection amount must be between 0.2 and 0.5"
        self.__bolus = bolus
        return "Success Set Bolus to " + str(bolus)
    
    def baseline_on(self):
        self.__baselineStatus = True
    
    def baseline_off(self):
        self.__baselineStatus = False
    
    def validate(self,amount: float)->bool:
        # Check hour limit
        if(self.__hourAmount + amount > Core.MAX_HOUR_AMOUNT):
            return False
        # Check day limit
        if(self.__dailyAmount + amount > Core.MAX_DAILY_AMOUNT):
            return False
        return True

    def update_by_minute(self):
        if len(self.__minuteRecord) >= 60:
            amount = self.__minuteRecord.pop(0)
            self.__hourAmount -= amount
            if len(self.__minuteRecord) >= 1440:
                self.__dailyAmount -= amount
        
        if self.__baselineStatus:
            if self.validate(self.__baseline):
                self.__minuteRecord.append(self.__baseline)
                self.__hourAmount += self.__baseline
                self.__dailyAmount += self.__baseline
            else:
                self.__minuteRecord.append(0.0)
        else:
            self.__minuteRecord.append(0.0)

    def request_bolus(self) -> bool:
        if self.validate(self.__bolus):
            self.__hourAmount += self.__bolus
            self.__dailyAmount += self.__bolus
            if len(self.__minuteRecord) == 0:
                self.__minuteRecord.append(self.__bolus)
            else:
                self.__minuteRecord[-1] += self.__bolus
            return True
        return False
    def status(self):
        return {
            'Baseline Rate': self.__baseline,
            'Bolus Amount': self.__bolus,
            'Daily Amount': self.__dailyAmount,
            'Hourly Amount': self.__hourAmount,
            'Baseline Status': self.__baselineStatus,
            'Minute Record': self.__minuteRecord[-10:]
        }
        


        
        
        

