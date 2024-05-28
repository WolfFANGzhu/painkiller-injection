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
        self.__baselineStatus = 'off'  # Baseline Status: off, on, pause
        self.__minuteRecord = []  # Record the amount injected every minute (Size 60 * 24)
        self.__time = 0

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
        self.__baselineStatus = 'on'
    
    def baseline_off(self):
        self.__baselineStatus = 'off'
    
    def validate(self, amount: Decimal) -> bool:
        # Check hour limit
        if (self.__hourAmount + amount > Core.MAX_HOUR_AMOUNT):
            return False
        # Check day limit    
        if (self.__dailyAmount + amount > Core.MAX_DAILY_AMOUNT):
            return False
        return True

    def update_by_minute(self):
        # If minuteRecord exceeds 1440, remove the oldest record
        if len(self.__minuteRecord) >= 1440:
            self.__minuteRecord.pop(0)
        
        if self.__baselineStatus == 'on':
            if self.validate(self.__baseline):
                self.__minuteRecord.append(self.__baseline)
            else:
                self.__minuteRecord.append(Decimal('0.0'))
                self.__baselineStatus = 'pause'
        elif self.__baselineStatus == 'pause':
            if self.validate(self.__baseline):
                self.__minuteRecord.append(self.__baseline)
                self.__baselineStatus = 'on'  # Set status back to 'on' if validation succeeds
            else:
                self.__minuteRecord.append(Decimal('0.0'))
        else:
            self.__minuteRecord.append(Decimal('0.0'))

        # Calculate the hourly and daily amounts
        self.__hourAmount = sum(self.__minuteRecord[-60:])
        self.__dailyAmount = sum(self.__minuteRecord)
        self.__time += 1

    def request_bolus(self) -> bool:
        if self.validate(self.__bolus):
            if len(self.__minuteRecord) == 0:
                self.__minuteRecord.append(self.__bolus)
            else:
                self.__minuteRecord[-1] += self.__bolus
            # Recalculate hour and daily amounts after bolus request
            self.__hourAmount = sum(self.__minuteRecord[-60:])
            self.__dailyAmount = sum(self.__minuteRecord)
            return True
        return False

    def reset(self):
        self.__baseline = Decimal('0.01')
        self.__bolus = Decimal('0.2')
        self.__dailyAmount = Decimal('0.0')
        self.__hourAmount = Decimal('0.0')
        self.__baselineStatus = 'off'
        self.__minuteRecord = []
        self.__time = 0

    def status(self):
        return {
            'Time': self.__time,
            'Baseline Rate': self.__baseline,
            'Bolus Amount': self.__bolus,
            'Hourly Amount': self.__hourAmount,
            'Daily Amount': self.__dailyAmount,
            'Baseline Status': self.__baselineStatus,
        }
