from decimal import Decimal, getcontext
import matplotlib.pyplot as plt
import numpy as np
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
        self.__hourlyRecord = []  # Record the amount injected every hour 
        self.__dailyRecord = []  # Record the amount injected every day 
        self.__timeRecord = []  # Record the time in minutes

    def set_baseline(self, baseline: float) -> str:
        baseline = Decimal(str(baseline))
        if baseline < Decimal('0.01') or baseline > Decimal('0.1'):
            return "Baseline injection rate must be between 0.01 and 0.1 ml."
        self.__baseline = baseline
        return "Success set baseline to " + str(baseline) + " ml."

    def set_bolus(self, bolus: float) -> str:
        bolus = Decimal(str(bolus))
        if bolus < Decimal('0.2') or bolus > Decimal('0.5'):
            return "Bolus injection amount must be between 0.2 and 0.5 ml."
        self.__bolus = bolus
        return "Success set bolus to " + str(bolus) + " ml."
    
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
        else:
            self.__minuteRecord.append(Decimal('0.0'))

        if len(self.__hourlyRecord) >= 1440:
            self.__hourlyRecord.pop(0)
            self.__dailyRecord.pop(0)
            self.__timeRecord.pop(0)
        # Calculate the hourly and daily amounts
        self.__time += 1
        self.__hourAmount = sum(self.__minuteRecord[-60:])
        self.__dailyAmount = sum(self.__minuteRecord)

        self.__hourlyRecord.append(self.__hourAmount)
        self.__dailyRecord.append(self.__dailyAmount)
        self.__timeRecord.append(self.__time)
        

    def request_bolus(self) -> bool:
        if self.validate(self.__bolus):
            if len(self.__minuteRecord) == 0:
                self.__minuteRecord.append(self.__bolus)
            else:
                self.__minuteRecord[-1] += self.__bolus
            # Recalculate hour and daily amounts after bolus request
            self.__hourAmount = sum(self.__minuteRecord[-60:])
            self.__dailyAmount = sum(self.__minuteRecord)
            self.__hourlyRecord[-1] = self.__hourAmount
            self.__dailyRecord[-1] = self.__dailyAmount
            return True
        return False

    def reset(self):
        self.__baseline = Decimal('0.01')
        self.__bolus = Decimal('0.2')
        self.__dailyAmount = Decimal('0.0')
        self.__hourAmount = Decimal('0.0')
        self.__baselineStatus = 'off'
        self.__minuteRecord = []
        self.__hourlyRecord = []
        self.__dailyRecord = []
        self.__timeRecord = []
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

    def generate_combined_graph(self):
        plt.close('all')
        time_data = self.__timeRecord  # Last 60 minutes time data
        hourly_data = self.__hourlyRecord  # Last 60 minutes hourly data
        daily_data = self.__dailyRecord  # Last 60 minutes daily data

        fig, ax1 = plt.subplots()

        color = 'tab:blue'
        ax1.set_xlabel('Time (minutes)')
        ax1.set_ylabel('Hourly Amount (mL)', color=color)
        ax1.plot(time_data, hourly_data, color=color, label='Hourly Amount')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.legend(loc='upper left')

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:red'
        ax2.set_ylabel('Daily Amount (mL)', color=color)  # we already handled the x-label with ax1
        ax2.plot(time_data, daily_data, color=color, label='Daily Amount')
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.legend(loc='upper right')

        # Set x-axis limit
        ax1.set_xlim([0, 1440])
        ax2.set_xlim([0, 1440])

        # Set y-axis limit and ticks
        ax1.set_ylim([0, 3.5])
        ax2.set_ylim([0, 3.5])
        ax1.set_xticks(np.arange(0, 1441, 60))
        ax2.set_xticks(np.arange(0, 1441, 60))
        ax1.set_yticks(np.arange(0, 3.1, 0.1))
        ax2.set_yticks(np.arange(0, 3.1, 0.1))

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title('Hourly and Daily Amount Over Time')
        plt.close(fig)
        return fig
    
if __name__ == "__main__":
    core = Core()
    print(core.set_baseline(0.05))
    print(core.set_bolus(0.3))
    print(core.status())
    core.baseline_on()
    core.update_by_minute()
    core.update_by_minute()
    core.update_by_minute()
    core.update_by_minute()
    core.update_by_minute()
    print(core.status())
    core.request_bolus()
    core.update_by_minute()
    core.update_by_minute()
    core.update_by_minute()
    core.update_by_minute()
    core.update_by_minute()
    print(core.status())
    fig = core.generate_combined_graph()
    plt.show()
    core.reset()
    print(core.status())
    fig = core.generate_combined_graph()
    plt.show()