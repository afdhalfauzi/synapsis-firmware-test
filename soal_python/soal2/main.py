from ..function.scheduler import Scheduler
from . import weatherLogger

    
def main():
    scheduler = Scheduler(weatherLogger.samplingWeatherData)
    scheduler.start()

if __name__ == "__main__":
    main()