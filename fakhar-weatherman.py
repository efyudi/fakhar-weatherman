import sys
import os
import getopt
from colorama import Fore

monthDictionary = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May",
                   6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

whatToFindDictionary = {0: "Highest Temperature", 1: "Mean Temperature",
                        2: "Lowest Temperature", 3: "Highest Humidity", 4: "Mean Humidity", 5: "Lowest Humidity"}


class WeatherReadings:
    # this will require 16 more variables.
    def __init__(self, day, month, year, max_temp, mean_temp, min_temp, max_humidity, mean_humidity, min_humidity):
        self.attributes = []
        self.day = day
        self.month = month
        self.year = year
        # Trying to experiment with different approaches and what works best
        # Will use a loop here for appending all 23 values
        self.attributes.append(max_temp)
        self.attributes.append(mean_temp)
        self.attributes.append(min_temp)
        self.attributes.append(max_humidity)
        self.attributes.append(mean_humidity)
        self.attributes.append(min_humidity)
        # Manually setting all the values
        self.max_temp = max_temp
        self.mean_temp = mean_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity

    def print_details(self):
        print("Date : " + self.day + "-" + self.month + "-" + self.year)
        # print("Max Temp : " + self.max_temp + " :: Mean Temp : " +
        #      self.mean_temp + " :: Min Temp : " + self.min_temp)
        # print("Max Humidity : " + self.max_humidity + " :: Mean Humidity : " +
        #      self.mean_humidity + " :: Min Humidity : " + self.min_humidity)
        # print("Max Temp : " + self.attributes[0] + " :: Mean Temp : " +
        #      self.attributes[1] + " :: Min Temp : " + self.attributes[2])
        # print("Max Humidity : " + self.attributes[3] + " :: Mean Humidity : " +
        #      self.attributes[4] + " :: Min Humidity : " + self.attributes[5])


class ParseFiles:
    @staticmethod
    def parse_file(file):
        weather_readings = []
        with open(file, 'r') as fileToRead:
            fileToRead.readline()  # Reading the titles
            for line in fileToRead:
                # Separating Details by comma
                separated_details = line.split(',')
                # Splitting the date for better Search
                year, month, day = separated_details[0].split('-')
                # Adding new date Weather to the List
                weather_readings.append(WeatherReadings(day, month, year, separated_details[1], separated_details[2],
                                                        separated_details[3], separated_details[7],
                                                        separated_details[8], separated_details[9]))
                # weather_readings.append(WeatherReadings(
                #    day, month, year, separated_details[1:]))
        return weather_readings


class MakeWeatherReport:
    @staticmethod
    def generate_mean_report(readings):
        for key, value in readings.items():
            # print("\033[0;37;40m "+key+" : ", end="")  # Manual Command to print colored Text
            # Module imported for color text
            print(Fore.WHITE + key + " : ", end="")
            for _ in range(0, value):  # Printing +, value number of times
                print(
                    Fore.RED + "+", end="") if "Highest" in key else print(Fore.LIGHTBLUE_EX + "+", end="")
            # Print the value in Magenta Color
            print(Fore.LIGHTMAGENTA_EX + " " + str(value))

    @staticmethod
    def generate_monthly_report(readings_max, readings_min):
        """ Function to Generate Monthly Report"""
        for entry in range(1, len(readings_max)):
            if readings_max[entry] == "":
                continue
            else:
                print(Fore.WHITE + str(entry) + " : ", end="")
                for _ in range(0, int(readings_max[entry])):
                    print(Fore.RED + "+", end="")
                print(Fore.LIGHTMAGENTA_EX + " " +
                      str(readings_max[entry]) + "C")

                print(Fore.WHITE + str(entry) + " : ", end="")
                for _ in range(0, int(readings_min[entry])):
                    print(Fore.LIGHTBLUE_EX + "+", end="")
                print(Fore.LIGHTMAGENTA_EX + " " +
                      str(readings_min[entry]) + "C\n", end="\n")

    @staticmethod
    def generate_monthly_inline_report(readings_max, readings_min):
        """ Function to Generate Monthly Report but in a single line (BONUS)"""
        for entry in range(1, len(readings_max)):
            if readings_max[entry] == "":
                continue
            else:
                print(Fore.WHITE + str(entry) + " : ", end="")
                for _ in range(0, int(readings_min[entry])):
                    print(Fore.LIGHTBLUE_EX + "+", end="")

                for _ in range(0, int(readings_max[entry])):
                    print(Fore.RED + "+", end="")
                print(Fore.LIGHTMAGENTA_EX + " " +
                      str(readings_min[entry]) + "C - " + str(readings_max[entry] + "C"))


class WeatherCalculations:
    @staticmethod
    def print_calculated_reading(weather_readings, recorded_month, entry_in_file, value, index):
        """ Function to Print calculated readings (Debugging Purposes)"""
        day = weather_readings[recorded_month][entry_in_file].day
        month = int(weather_readings[recorded_month][entry_in_file].month)
        print(whatToFindDictionary[index] + " : " + str(value) + " on " +
              monthDictionary[month] + " " + day)

    @staticmethod
    def check_max(old_max, value):
        """ Find Max """
        old_max = value if value > old_max else old_max
        return old_max

    @staticmethod
    def check_min(old_min, value):
        """ Find Min """
        old_min = value if value < old_min else old_min
        return old_min

    def calculate_highest_reading(self, weather_readings, index):
        """ Function will find MAX of what is specified, based on the index passed """
        find_max = -sys.maxsize
        highest_recorded_month = 0
        entry_in_file_max = 0
        for month in range(0, len(weather_readings)):
            for entry in range(0, len(weather_readings[month])):
                if weather_readings[month][entry].attributes[index] == "":
                    continue
                else:
                    returned_max = self.check_max(find_max, int(
                        weather_readings[month][entry].attributes[index]))
                    # Calculate Highest Temperature/ Humidity (BASED ON INDEX PASSED)
                    if returned_max > find_max:
                        find_max = returned_max
                        highest_recorded_month = month
                        entry_in_file_max = entry
        # Display Details of the day with HIGHEST of Specified Details
        self.print_calculated_reading(
            weather_readings, highest_recorded_month, entry_in_file_max, find_max, index)

        # LINES OF CODE TO MAKE REPORT OF HIGHEST/ AVERAGE TEMPERATURE/HUMIDITY
        # readings = {"Highest ": find_max,
        #            "on": weather_readings[highest_recorded_month][entry_in_file_max], "index": index}
        # MakeWeatherReport.generate_mean_report(MakeWeatherReport, readings)

    def calculate_lowest_reading(self, weather_readings, index):
        """ Function will find MIN of what is specified, based on the index passed """
        find_min = sys.maxsize
        lowest_recorded_month = 0
        entry_in_file_min = 0
        for month in range(0, len(weather_readings)):
            for entry in range(0, len(weather_readings[month])):
                if weather_readings[month][entry].attributes[index] == "":
                    continue
                else:
                    returned_min = self.check_min(find_min, int(
                        weather_readings[month][entry].attributes[index]))
                    # Calculate LOWEST Temperature/ Humidity (BASED ON INDEX PASSED)
                    if returned_min < find_min:
                        find_min = returned_min
                        lowest_recorded_month = month
                        entry_in_file_min = entry
        # Display Details of the day with LOWEST of Specified Details
        self.print_calculated_reading(weather_readings,
                                      lowest_recorded_month, entry_in_file_min, find_min, index + 2)

        # LINES OF CODE TO MAKE REPORT OF HIGHEST/ AVERAGE TEMPERATURE/HUMIDITY
        # readings = {"Lowest ": find_min,
        #            " on ": weather_readings[lowest_recorded_month][entry_in_file_min], "index": index+2}
        # MakeWeatherReport.generate_mean_report(MakeWeatherReport, readings)

    @staticmethod
    def make_report(weather_readings):
        report_dictionary_highest = {}
        report_dictionary_lowest = {}
        for reading in range(0, len(weather_readings[0])):
            report_dictionary_highest.update(
                {int(weather_readings[0][reading].day): weather_readings[0][reading].max_temp})
            report_dictionary_lowest.update(
                {int(weather_readings[0][reading].day): weather_readings[0][reading].min_temp})

        MakeWeatherReport.generate_monthly_report(
            report_dictionary_highest, report_dictionary_lowest)
        MakeWeatherReport.generate_monthly_inline_report(
            report_dictionary_highest, report_dictionary_lowest)

    @staticmethod
    def calculate_mean_humidity(weather_readings):
        total_readings = 0
        value = 0
        for month in range(0, len(weather_readings)):
            for reading in range(0, len(weather_readings[month])):
                total_readings += 1
                value += int(weather_readings[month]
                             [reading].mean_humidity) if weather_readings[month][reading].mean_humidity else 0
        return value / int(total_readings)

    @staticmethod
    def calculate_mean_temperature(weather_readings):
        total_readings = 0
        max_value = 0
        min_value = 0
        for month in range(0, len(weather_readings)):
            for reading in range(0, len(weather_readings[month])):
                total_readings += 1
                max_value += int(weather_readings[month]
                                 [reading].max_temp) if weather_readings[month][reading].max_temp else 0
                min_value += int(weather_readings[month]
                                 [reading].min_temp) if weather_readings[month][reading].min_temp else 0
        return max_value / int(total_readings), min_value / int(total_readings)

    def calculate_avg(self, weather_readings):
        avgmax_temp, avgmin_temp = self.calculate_mean_temperature(
            weather_readings)
        mean_avg_humidity = self.calculate_mean_humidity(weather_readings)
        print("Average Highest Temperature : ", int(avgmax_temp))
        print("Average Lowest Temperature : ", int(avgmin_temp))
        print("Mean Average Humidity : ", int(mean_avg_humidity))

        # LINES OF CODE TO MAKE REPORT OF AVERAGE TEMPERATURE/HUMIDITY
        # readings = {"Average Highest Temperature": int(avgmax_temp), "Average Lowest Temperature": int(
        #    avgmin_temp), "Mean Average Humidity": int(mean_avg_humidity)}
        # MakeWeatherReport.generate_mean_report(MakeWeatherReport, readings)
        # return int(avgmax_temp), int(avgmin_temp), int(mean_avg_humidity)


def search_files(path, arguments):
    """ Read Files based on the year/month Mentioned """
    weather_readings = []
    # mentioned_date = arguments[0][0][1]
    mentioned_date = arguments.split(
        '/') if '/' in arguments else arguments  # Parsing MONTH AND YEAR if Provided
    # Joining the Year Mentioned in File Naming Format
    year = "".join(mentioned_date[0] + "_" + monthDictionary[int(mentioned_date[1])]
                   ) if isinstance(mentioned_date, list) else mentioned_date
    # List every file in the mentioned directory
    for file in os.listdir(path):
        if year in file:  # Listing Files which matches the NAME/ YEAR,MONTH
            weather_readings.append(
                ParseFiles.parse_file(file))

    return weather_readings
    # weather_readings[FILE][LINE/ENTRY]
    # print(weather_readings[1][0].month)


def main():
    path = sys.argv[1]  # File Path
    try:
        arguments, _ = getopt.getopt(
            sys.argv[2:], "c:a:e:")  # Parse the Arguments
    except:
        print("Usage : script.py ./path <operation> value")
        sys.exit(2)
    for option, value in arguments:
        weather_readings = search_files(path, value)
        if option in '-e':
            # First function call is for Temperature
            WeatherCalculations.calculate_highest_reading(
                WeatherCalculations, weather_readings, 0)
            WeatherCalculations.calculate_lowest_reading(
                WeatherCalculations, weather_readings, 0)
            # Second Function call is for Humidity
            WeatherCalculations.calculate_highest_reading(
                WeatherCalculations, weather_readings, 3)
            WeatherCalculations.calculate_lowest_reading(
                WeatherCalculations, weather_readings, 3)
            print()
        elif option in '-a':
            WeatherCalculations.calculate_avg(
                WeatherCalculations, weather_readings)
            print()
        elif option in '-c':
            WeatherCalculations.make_report(weather_readings)
            # with open(path, 'r') as file:
            #    for line in file:
            #        print(line, end="")

            # print(path)
            # print(arguments)


if __name__ == "__main__":
    main()
