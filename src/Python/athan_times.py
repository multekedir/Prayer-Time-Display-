from prayer_api import prayer_api
from datetime import date, datetime

"""
This class sets the longitude and latitude to get the Athan time.
It also calculates the time left for the next prayer.

Author: Multezem Kedir
Date: 1/4/2017
Version: 2.0
"""


class athan_times:
    __prayTimes = None

    def __init__(self):
        self.__time_left = 0000
        self.__prayTimes = prayer_api('ISNA')
        self.__next_prayer = "Fajr"

    def get_prayertime(self, prayer, format='24h', ):
        """
        get the time of Athan from the prayer_api.py file.
        Location is set to Eugene,OR. Can be changed by
        adjusting the long, lat and elevation.
        :param prayer: enter a prayer from one the list [fajr, sunrise, dhuhr, asr, maghrib, isha]
        :param format: adjust time format in '12h' or '24h'
        :return: Time of prayer
        """

        times = self.__prayTimes.getTimes(date.today(), (44.0497300, -123.1210060, 131.04), -8, 0, format)
        return times[prayer]

    def get_timeremaining(self):
        """
        calculates how many hours or min left to prayer by sorting
        the prayer times and the current time. We find the location
        of the current time and see what prayer is next.

        :return: time remaining  in '00:00' format
        """
        hour = int(datetime.now().strftime('%H%M'))  # get current hour in '0000' format

        # ==========================get prayer times=====================================
        fajr_time = int(self.get_prayertime('fajr').replace(':', ''))
        sunrise_time = int(self.get_prayertime('sunrise').replace(':', ''))
        dhuhr_time = int(self.get_prayertime('dhuhr').replace(':', ''))
        asr_time = int(self.get_prayertime('asr').replace(':', ''))
        maghrib_time = int(self.get_prayertime('maghrib').replace(':', ''))
        isha_time = int(self.get_prayertime('isha').replace(':', ''))

        # =========================================================================================
        #  sort the current time and the prayer times
        time_index = sorted([hour, fajr_time, sunrise_time, dhuhr_time, asr_time, maghrib_time, isha_time]).index(hour)
        self.prayer_list = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
        prayer_index = [hour, fajr_time, sunrise_time, dhuhr_time, asr_time, maghrib_time, isha_time]
        print(sorted(prayer_index))
        print(hour)
        print('time index', time_index)
        # ==========================================================================================
        #  depending on the location of the current hour calculate the time left
        if time_index == 0:
            self.__time_left = fajr_time - hour
            self.__next_prayer = "Fajr"
        elif time_index == 1:
            self.__time_left = sunrise_time - hour
            self.__next_prayer = "Dhuhr"
        if time_index == 2:
            self.__time_left = dhuhr_time - hour
            self.__next_prayer = "Asr"
        elif time_index == 3:
            self.__time_left = asr_time - hour
            self.__next_prayer = "Maghrib"
        elif time_index == 4:
            self.__time_left = maghrib_time - hour
            self.__next_prayer = "Isha"
        elif time_index == 5:
            self.__time_left = isha_time - hour
            self.__next_prayer = "Fajr"
        elif time_index == 6:
            self.__time_left = ((2400 - isha_time) + fajr_time)

        # ===================================================================
        #  add trailing  zero and finally return
        self.__time_left = str(self.__time_left)

        if len(self.__time_left) == 4:
            if int(self.__time_left[2:]) > 60:
                min = int(self.__time_left[2:]) - 60
                hr = int(self.__time_left[:2]) + 1
                return str(hr) + 'Hr,' + str(min) + 'Min' + ' Until ' + self.__next_prayer
            else:
                return self.__time_left[:2] + 'Hr,'  + str(self.__time_left)[2:] +'Min' + ' Until ' + self.__next_prayer
        elif len(self.__time_left) == 3:
            if int(self.__time_left[1:]) > 60:
                min = int(self.__time_left[1:]) - 60
                hr = int(self.__time_left[:1]) + 1
                return str(hr) + 'Hr,'  + str(min)+'Min' + ' Until ' + self.__next_prayer
            else:
                return self.__time_left[:1] + 'Hr,'  + self.__time_left[1:]+'Min'+ ' Until ' + self.__next_prayer
        elif len(self.__time_left) == 2:
            return self.__time_left + 'Min' + ' Until ' + self.__next_prayer
        elif len(self.__time_left) == 1:
            if int(self.__time_left) == 0:
                return str(' Time for ' + self.prayer_list[time_index])
            else:
                return self.__time_left + 'Min'+ ' Until ' + self.__next_prayer
