from athan_times import athan_times

"""
This class calculates Iqama time according user input from the java program.
This class reads iqama.txt from that was saved from the java program.

Author: Multezem Kedir
Date: 1/4/2017
Version: 2.0
"""


class iqama_time:
    # ======================================================================================================================
    def __init__(self):
        # get Athan time from api
        self.__athan = athan_times()
        # file to read is iqama_time.txt
        self.__file_name = 'iqama.txt'
        # a list to store file data
        self.__file_data = []
        # read file
        self.__read_file()
        self.__time = ""

    def __read_file(self):
        """ Read file and store each line in a list"""
        with open(self.__file_name, "r") as f:
            for i in range(6):
                # append data to a list and remove the new line char
                self.__file_data.append(f.readline().strip('\n').lower())

        # close file
        f.close()

    # ======================================================================================================================
    def __cal_iqama_time(self, hour, difference):
        """
        Gets prayer time and split the string and add
        the min to the prayer time.
        If hour 11:50am and difference is 20 -> 12:10pm
        :param hour: 11:50pm
        :param difference: 20
        :return: time in 12hr formats
        """
        self.period = hour[-2:]  # get the am and pm
        self.hour, self.min = hour.strip('am,pm').split(':')  # get the time
        self.iqama_min = int(self.min) + difference
        if self.iqama_min >= 60:  # check if it is more than 59 min
            self.iqama_min -= 60
            if len(str(self.iqama_min)) == 1:
                self.iqama_min = '0' + str(self.iqama_min)
            self.iqama_hour = int(self.hour) + 1
            if hour == '11':
                if self.period == "am":
                    self.period = 'pm'

                elif self.period == 'pm':
                    self.period = 'am'
            return str(self.iqama_hour) + ":" + str(self.iqama_min) + self.period
        return str(self.hour) + ":" + str(self.iqama_min) + self.period

    # ===================================================================================================================
    def __get_index(self, prayer):
        """
        enter a prayer get the index of the prayer
        from the list data_file.
        {fajr, dhuhr, asr, maghrib, isha, jumah}
        :type prayer: str
        :param prayer:
        :return: int
        """
        prayer = prayer.lower()
        self.__index = None
        if prayer == "fajr":
            self.__index = 0
        elif prayer == "dhuhr":
            self.__index = 1
        elif prayer == "asr":
            self.__index = 2
        elif prayer == "maghrib":
            self.__index = 3
        elif prayer == "isha":
            self.__index = 4
        elif prayer == "jumah":
            self.__index = 5
        return int(self.__index)

    # ======================================================================================================================
    def get_iqama(self, prayer):
        """
        Check id input is a static or an addition.
        user input can start with '+' or a static time '5:25 PM'
        calls prayer_api.py
        :return: static time ('4:30 PM') or adds the time from Athan api
        """

        self.__time = self.__file_data[self.__get_index(prayer)]
        if self.__time.startswith('+'):
            self.__time = self.__time.strip('+')
            try:
                self.__time = int(self.__time)
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")
            self.__time = self.__cal_iqama_time(self.__athan.get_prayertime(prayer, '12h'), self.__time)
            return self.__time
        if "pm" or "am" and ":" in self.__time and len(self.__time) > 6:
            return self.__time
        else:
            return "ERROR"
