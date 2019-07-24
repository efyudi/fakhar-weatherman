import csv
import sys
import os
import getopt
from colorama import Fore
monthDictionary = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May",
                   6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

whatToFindDictionary = {1: "Highest Temperature", 2: "Mean Temperature",
                        3: "Lowest Temperature", 4: "Dew PointC", 5: "MeanDew PointC",
                        6: "Min DewpointC", 7: "Max Humidity", 8: "Mean Humidity", 9: "Min Humidity",
                        10: "Max Sea Level PressurehPa", 11: "Mean Sea Level PressurehPa",
                        12: "Min Sea Level PressurehPa",
                        13: "Max VisibilityKm", 14: "Mean VisibilityKm", 15: "Min VisibilitykM",
                        16: "Max Wind SpeedKm/h", 17: "Mean Wind SpeedKm/h",
                        18: " Max Gust SpeedKm/h", 19: "Precipitationmm", 20: "", 21: "CloudCover", 22: "Events",
                        23: "WindDirDegrees"}

unitsDictionary = {1: "C", 2: "C", 3: "C", 4: "C", 5: "C", 6: "C", 7: "%", 8: "%", 9: "%", 10: "Pa", 11: "Pa", 12: "Pa",
                   13: "Km", 14: "Km", 15: "kM", 16: "Km/h", 17: "Km/h", 18: "Km/h", 19: "mm", 20: "", 21: "", 22: "",
                   23: "Deg"}


class WeatherReadings:

    def __init__(self, day, month, year, separated_readings):
        self.attributes = []
        self.day = day
        self.month = month
        self.year = year
        for i in range(0, len(separated_readings)):
            self.attributes.append(separated_readings[i])

    def print_details(self):
        print("Date : " + self.day + "-" + self.month + "-" + self.year)
        for i in range(1, len(self.attributes)):
            print(whatToFindDictionary[i] + " : " + self.attributes[i])


class ParseFiles:
    @staticmethod
    def parse_file(file):
        """ Function to Parse the files.
        It finds the files, parses the data, stores in a list, and returns the list object """
        weather_readings = []

        with open(file, 'rt')as f:
            data = csv.reader(f)
            next(data)
            for row in data:
                year, month, day = row[0].split('-')
                weather_readings.append(WeatherReadings(
                    day, month, year, row[0:]))
        return weather_readings


class MakeWeatherReport:
    @staticmethod
    def generate_mean_report(readings):
        """ Function to generate report for mean operation -a """
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
        """ Function to Print calculated readings (Debugging Purposes) """
        day = weather_readings[recorded_month][entry_in_file].day
        month = int(weather_readings[recorded_month][entry_in_file].month)
        print("{} : {}{} on {} {}".format(whatToFindDictionary[index], str(
            value), unitsDictionary[index], monthDictionary[month], day))

    @staticmethod
    def check_max(old_max, value):
        """ Find Max """
        return value if value > old_max else old_max

    @staticmethod
    def check_min(old_min, value):
        """ Find Min """
        return value if value < old_min else old_min

    def calculate_highest_reading(self, weather_readings, index):
        """ Function will find MAX of what is specified, based on the index passed """
        find_max = -sys.maxsize
        highest_recorded_month = 0
        entry_in_file_max = 0
        ''' month here is, number of the MONTH FILE. ex : files read are 2. 0 = AUG, 1 = OCT.
         so I decode it later using the month variable '''
        for month in range(0, len(
                weather_readings)):
            for entry in range(0, len(weather_readings[month])):
                # if empty, skips
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
                # if empty, Skips
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
                                      lowest_recorded_month, entry_in_file_min, find_min, index)

        # LINES OF CODE TO MAKE REPORT OF HIGHEST/ AVERAGE TEMPERATURE/HUMIDITY
        # readings = {"Lowest ": find_min,
        #            " on ": weather_readings[lowest_recorded_month][entry_in_file_min], "index": index}
        # MakeWeatherReport.generate_mean_report(MakeWeatherReport, readings)

    @staticmethod
    def make_report(weather_readings):
        """Make a Report for Highest and Lowest Temp of a given month"""
        report_dictionary_highest = {}
        report_dictionary_lowest = {}
        for reading in range(0, len(weather_readings[0])):
            report_dictionary_highest.update(
                {int(weather_readings[0][reading].day): weather_readings[0][reading].attributes[1]})
            report_dictionary_lowest.update(
                {int(weather_readings[0][reading].day): weather_readings[0][reading].attributes[3]})

        MakeWeatherReport.generate_monthly_report(
            report_dictionary_highest, report_dictionary_lowest)
        MakeWeatherReport.generate_monthly_inline_report(
            report_dictionary_highest, report_dictionary_lowest)

    @staticmethod
    def calculate_mean_humidity(weather_readings):
        """Calculates the mean Humidity """
        total_readings = 0
        value = 0
        for month in range(0, len(weather_readings)):
            for reading in range(0, len(weather_readings[month])):
                total_readings += 1
                value += int(weather_readings[month]
                             [reading].attributes[8]) if weather_readings[month][reading].attributes[8] else 0
        return value / int(total_readings)

    @staticmethod
    def calculate_mean_temperature(weather_readings):
        """Calculates the mean Temperature"""
        total_readings = 0
        max_value = 0
        min_value = 0
        for month in range(0, len(weather_readings)):
            for reading in range(0, len(weather_readings[month])):
                total_readings += 1
                max_value += int(weather_readings[month]
                                 [reading].attributes[1]) if weather_readings[month][reading].attributes[1] else 0
                min_value += int(weather_readings[month]
                                 [reading].attributes[3]) if weather_readings[month][reading].attributes[3] else 0
        return max_value / int(total_readings), min_value / int(total_readings)

    def calculate_avg(self, weather_readings):
        """Calculates the Average Temperatures and Humidity"""
        avgmax_temp, avgmin_temp = self.calculate_mean_temperature(
            weather_readings)
        mean_avg_humidity = self.calculate_mean_humidity(weather_readings)
        print("Average Highest Temperature : {}C".format(str(int(avgmax_temp))))
        print("Average Lowest Temperature : {}C".format(str(int(avgmin_temp))))
        print("Mean Average Humidity : {}%".format(str(int(mean_avg_humidity))))
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
    year = "".join("{}_{}".format(mentioned_date[0], monthDictionary[int(mentioned_date[1])])
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
                WeatherCalculations, weather_readings, 1)
            WeatherCalculations.calculate_lowest_reading(
                WeatherCalculations, weather_readings, 3)
            # Second Function call is for Humidity
            WeatherCalculations.calculate_highest_reading(
                WeatherCalculations, weather_readings, 7)
            WeatherCalculations.calculate_lowest_reading(
                WeatherCalculations, weather_readings, 9)
            print()
        elif option in '-a':
            WeatherCalculations.calculate_avg(
                WeatherCalculations, weather_readings)
            print()
        elif option in '-c':
            WeatherCalculations.make_report(weather_readings)


if __name__ == "__main__":
    main()
