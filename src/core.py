from decimal import Decimal, getcontext

# Set the precision to 2 decimal places
getcontext().prec = 2  

class Core:
    # Static variable declaration
    MAX_DAILY_AMOUNT = Decimal('3.0')
    MAX_HOUR_AMOUNT = Decimal('1.0')

    def __init__(self):
        self.__baseline = Decimal('0.01')  # Baseline injection rate [0.01,0.1]
        self.__bolus = Decimal('0.2')  # Bolus injection amount [0.2,0.5]
        self.__dailyAmount = Decimal('0.0')
        self.__hourAmount = Decimal('0.0')
        self.__baselineStatus = False
        self.__minuteRecord = []  # Record the amount injected every minute (Size 60 * 24)

    def set_baseline(self, baseline: float) -> str:
        baseline = Decimal(str(baseline))
        if baseline < Decimal('0.01') or baseline > Decimal('0.1'):
            return "Baseline injection rate must be between 0.01 and 0.1"
        self.__baseline = baseline
        return "Success Set Baseline to " + str(baseline)

    def set_bolus(self, bolus: float) -> str:
        bolus = Decimal(str(bolus))
        if bolus < Decimal('0.2') or bolus > Decimal('0.5'):
            return "Bolus injection amount must be between 0.2 and 0.5"
        self.__bolus = bolus
        return "Success Set Bolus to " + str(bolus)
    
    def baseline_on(self):
        self.__baselineStatus = True
    
    def baseline_off(self):
        self.__baselineStatus = False
    
    def validate(self, amount: Decimal) -> bool:
        # Check hour limit
        if (self.__hourAmount + amount > Core.MAX_HOUR_AMOUNT):
            return False
        # Check day limit    
        if (self.__dailyAmount + amount > Core.MAX_DAILY_AMOUNT):
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
                self.__minuteRecord.append(Decimal('0.0'))
        else:
            self.__minuteRecord.append(Decimal('0.0'))

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
            'Hourly Amount': self.__hourAmount,
            'Daily Amount': self.__dailyAmount,
            'Baseline Status': self.__baselineStatus,
            #'Minute Record': self.__minuteRecord[-10:]
        }