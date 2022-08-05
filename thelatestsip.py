# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 19:41:17 2021

@author: David Ilogho
"""

from sl3 import *


def sutron_day_calc(julian_day, year):
    """
    Sutron day counts the number of days from 12/31/1984 till date. uses modulo 4096
    :param julian_day: Julian day (between 1 to 365 or 366(ly))
    :param year: Year (yyyy)
    :return: Sutron day
    """

    year -= 1985  # subtract 1984 + 1 from current year. Subtracting 1 because
    # this year is not over
    leap_year = year // 4
    return (365 * year + leap_year + julian_day) % 4096


class SecondarySensor:
    def __init__(self, meas_number):
        """
        This SecondarySensor class constructor uses the measurement number e.g M1 to retrieve relevant sensor
        attributes, then uses it to create and initialize the sensor object
        :param meas_number: Measurement number e.g M1, M2
        """

        self.meas_number = meas_number
        self.label = command_line("!" + meas_number + " LABEL\r").strip()
        self.right_digits = int(command_line("!" + meas_number + " RIGHT DIGITS\r").strip())
        self.value = -99999.0

    def get_encoded_data(self):
        """
        This method returns the encoded data of the object when called
        :return: Encoded data
        """
        if self.value == -99999.0:
            if self.label in ("MWWL", "COND"):
                return "???"
            if self.label in ("MWSTD", "AT", "WT", "CTWT"):
                return "??"
            if self.label in ("MWOUT"):
                return "?"
            if self.label in ("BARO"):
                return "@@@"
            if self.label in ("SNS"):
                return "@@"
            if self.label in ("BAT"):
                return "_?"

        value = int(self.value * 10 ** self.right_digits)
        if self.label in ("MWOUT"):
            return pseudo_encoder(value, 1, True)
        if self.label in ("BARO", "BAT", "MWSTD", "WD", "WG", "WS"):
            if self.label in ("BARO"):
                value -= 8000
            return pseudo_encoder(value, 2, True)
        if self.label in ("SNS", "AT", "WT"):
            return pseudo_encoder(value, 2)
        return pseudo_encoder(value, 3)

    def update_secondary_data(self):
        """
        This method is used to update the secondary data object with the most recent
        sensor data
        :return: Most recent sensor data value
        """
        log = command_line("!LOG 0.010 " + self.meas_number + " NY NH\r").strip()
        if log.count(self.label) > 0:
            self.value = round(float(log.split("\r\n")[-1].split(",")[3]), self.right_digits)
            return self.value
        self.value = -99999.0
        return self.value


class PrimarySensor(SecondarySensor):
    def __init__(self, meas_number):
        """
        This PrimarySensor class constructor inherits the SecondarySensor class attributes
        and methods. It also includes date and time attributes and additional methods for
        date and time conversions
        :param meas_number: Measurement number e.g M1
        """
        super().__init__(meas_number)
        self.redundant_value = -99999.0
        self.year = utime.localtime()[0]
        self.month = utime.localtime()[1]
        self.day = utime.localtime()[2]
        self.hour = utime.localtime()[3]
        self.minute = utime.localtime()[4]
        self.second = utime.localtime()[5]
        self.julian_day = utime.localtime()[7]
        self.sutron_day = sutron_day_calc(self.julian_day, self.year)

    def get_encoded_hour(self):
        """
        This method encodes hour
        :return: returns encoded data
        """
        return pseudo_encoder(self.hour, 1)

    def get_encoded_minute(self):
        """
        This method encodes minute
        :return: returns encoded data
        """
        return pseudo_encoder(self.minute, 1, True)

    def get_encoded_redundant_data(self):
        """
        This method encodes redundant data
        :return: returns encoded data
        """
        if self.redundant_value == -99999.0:
            return "@@@"
        value = int(self.redundant_value * 10 ** self.right_digits)
        return pseudo_encoder(value, 3)

    def get_encoded_sutron_day(self):
        """
        This method encodes sutron day
        :return: returns encoded data
        """
        return pseudo_encoder(self.sutron_day, 2, True)

    def update_primary_data(self):
        """
        This method is used to update the primary data object with the most recent
        sensor data, date and time
        :return: Most recent sensor data value, date and time
        """
        log = command_line("!LOG 0.015 " + self.meas_number + " NY NH\r").strip()
        if log.count(self.label) > 0:
            new_log = log.split("\r\n")[-1].split(",")
            self.value = round(float(new_log[3]), self.right_digits)
            if log.count(self.label) > 1:
                self.redundant_value = round(float(log.split("\r\n")[-2].split(",")[3]), self.right_digits)
            else:
                self.redundant_value = -99999.0
            if self.label == "MWWL":
                time_diff = 180
            elif self.label == "AQT":
                time_diff = 90
            else:
                time_diff = 0
            pri_date = utime.localtime(utime.mktime(get_log_date(new_log)) - time_diff)
            self.year = pri_date[0]
            self.month = pri_date[1]
            self.day = pri_date[2]
            self.hour = pri_date[3]
            self.minute = pri_date[4]
            self.second = pri_date[5]
            self.julian_day = pri_date[7]
            self.sutron_day = sutron_day_calc(self.julian_day, self.year)
            return self.value, self.redundant_value
        self.value = self.redundant_value = -99999.0
        return self.value, self.redundant_value


class TsunamiData(SecondarySensor):
    def __init__(self, meas_number):
        """
        This TsunamiData class constructor inherits certain PrimarySensor class attributes
        and methods. It also includes attributes and methods that are tsunami related
        :param meas_number: Measurement number e.g M1
        """
        super().__init__(meas_number)
        self.value2 = self.value3 = self.value4 = self.value5 = self.value6 = self.value
        self.hour = utime.localtime()[3]
        self.minute = utime.localtime()[4]

    def get_encoded_tsunami(self):
        """
        This method encodes tsunami data
        :return: returns encoded data
        """
        if -99999.0 in (self.value, self.value2, self.value3, self.value4, self.value5, self.value6):
            return "?", "?", "@", "@@", "@@", "@@", "@@", "@@", "@@"
        value = round(self.value * 10 ** self.right_digits)
        value2 = round(self.value2 * 10 ** self.right_digits)
        value3 = round(self.value3 * 10 ** self.right_digits)
        value4 = round(self.value4 * 10 ** self.right_digits)
        value5 = round(self.value5 * 10 ** self.right_digits)
        value6 = round(self.value6 * 10 ** self.right_digits)
        tsunami_offset = min(value, value2, value3, value4, value5, value6) // 250
        value = pseudo_encoder(value % 250 + (value // 250 - tsunami_offset) * 250, 2, True)
        value2 = pseudo_encoder(value2 % 250 + (value2 // 250 - tsunami_offset) * 250, 2, True)
        value3 = pseudo_encoder(value3 % 250 + (value3 // 250 - tsunami_offset) * 250, 2, True)
        value4 = pseudo_encoder(value4 % 250 + (value4 // 250 - tsunami_offset) * 250, 2, True)
        value5 = pseudo_encoder(value5 % 250 + (value5 // 250 - tsunami_offset) * 250, 2, True)
        value6 = pseudo_encoder(value6 % 250 + (value6 // 250 - tsunami_offset) * 250, 2, True)
        tsunami_hour = pseudo_encoder(self.hour, 1)
        tsunami_minute = pseudo_encoder(self.minute, 1, True)
        tsunami_offset = pseudo_encoder(tsunami_offset, 1, True)
        return tsunami_hour, tsunami_minute, tsunami_offset, value, value2, value3, value4, value5, value6

    def update_tsunami_data(self):
        """
        This method is used to update the tsunami data object with the most recent
        tsunami sensor data, date and time
        :return: Most recent tsunami sensor data value, date and time
        """
        log = command_line("!LOG 0.006 " + self.meas_number + " NY NH\r").strip()
        if log.count(self.label) > 5:
            tsunami_log = log.split("\r\n")[-1].split(",")
            self.hour = int((tsunami_log[1])[0:2])
            self.minute = int((tsunami_log[1])[3:5])
            self.value = round(float(tsunami_log[3]), self.right_digits)
            self.value2 = round(float(log.split("\r\n")[-2].split(",")[3]), self.right_digits)
            self.value3 = round(float(log.split("\r\n")[-3].split(",")[3]), self.right_digits)
            self.value4 = round(float(log.split("\r\n")[-4].split(",")[3]), self.right_digits)
            self.value5 = round(float(log.split("\r\n")[-5].split(",")[3]), self.right_digits)
            self.value6 = round(float(log.split("\r\n")[-6].split(",")[3]), self.right_digits)
            return self.value, self.value2, self.value3, self.value4, self.value5, self.value6
        self.value = self.value2 = self.value3 = self.value4 = self.value5 = self.value6 = -99999.0
        return self.value, self.value2, self.value3, self.value4, self.value5, self.value6


def format_date_time(date_time):
    """
    This function changes the time and date format in a tuple to this -> (YYYY/MM/DD, HH:MM:SS)
    :return: Date and time
    """
    start_date = "{:04d}/{:02d}/{:02d}".format(date_time[0], date_time[1], date_time[2])
    start_time = "{:02d}:{:02d}:{:02d}".format(date_time[3], date_time[4], date_time[5])
    return start_date, start_time


def sl3_datetime():
    """
    This function returns the current date and time of the Satlink 3 in a tuple of strings in this format
    (YYYY/MM/DD, HH:MM:SS)
    :return: Date and time
    """

    sl3_date_time = utime.localtime()[0:6]
    sl3_date = "{:04d}/{:02d}/{:02d}".format(sl3_date_time[0], sl3_date_time[1], sl3_date_time[2])
    sl3_time = "{:02d}:{:02d}:{:02d}".format(sl3_date_time[3], sl3_date_time[4], sl3_date_time[5])
    return sl3_date, sl3_time


def ports_tag_message_append(flag, val, f):
    f.write(flag)
    f.write("{:>11.1f}\r\n".format(val) if val != -99999.0 else "  Data Flagged as bad or missing\r\n")


def ports_tag_message_formatter():
    """
    This function formats the data to a file for PORTS Tag transmission
    """
    aqt = []
    mwwl1 = []
    mwwl2 = []
    wind1 = []
    wind2 = []
    station_id = command_line("!STATION NAME\r").strip()
    pri_year = str("{:04d}".format(add_sns[0].year))
    pri_month = str("{:02d}".format(add_sns[0].month))
    pri_day = str("{:02d}".format(add_sns[0].day))
    pri_date = ("{0}/{1}/{2}".format(pri_month, pri_day, pri_year))
    pri_hour = str("{:02d}".format(add_sns[0].hour))
    pri_minute = str("{:02d}".format(add_sns[0].minute))
    pri_second = str("{:02d}".format(add_sns[0].second))
    f = open("p", "w")
    f.write("NOS {0} {1} {2}:{3}:{4}\r\n".format(station_id, pri_date, pri_hour, pri_minute, pri_second))
    for a_s in add_sns:
        if a_s.label in ("AQT", "AQTSTD", "AQTOUT", "AQT1", "AQT2"):
            aqt.append(a_s.value)
            if len(aqt) == 5 and -99999.0 not in aqt[:3]:
                f.write("A1 1")
                f.write("{0}{1}{2}{3}{4}\r\n".format("{:>11.3f}".format(aqt[0]), "{:>9.3f}".format(aqt[1]),
                                                     "{:>10.0f}".format(aqt[2]), "{:>10.1f}".format(aqt[3]),
                                                     "{:>10.1f}".format(aqt[4])))
            else:
                f.write("A1 1  Data flagged as bad or missing\r\n")

        if a_s.label in ("WS", "WD", "WG"):
            wind1.append(a_s.value)
            if len(wind1) == 3 and -99999.0 not in wind1:
                f.write("C1 3")
                f.write("{0}{1}{2}\r\n".format("{:>11.1f}".format(wind1[0]),
                                               "{:>9.0f}".format(wind1[1]),
                                               "{:>10.1f}".format(wind1)))
            else:
                f.write("C1 3  Data flagged as bad or missing\r\n")
        elif a_s.label == "AT":
            ports_tag_message_append("D1 4", a_s.value, f)
        elif a_s.label == "WT":
            ports_tag_message_append("E1 5", a_s.value, f)
        elif a_s.label == "BARO":
            ports_tag_message_append("F1 6", a_s.value, f)

    f.write("L1 <")
    f.write("{:>11.1f}\r\n".format(bat.value) if bat.value != -99999.0 else "  Data flagged as bad or missing\r\n")
    f.write("DAT")
    f.write("{:>10.3f}".format(dat.value) + "\r\n" if dat.value != -99999.0 else " data not available\r\n")
    f.write("SNS")
    f.write("{:>10.3f}".format(sns.value) + "\r\n" if sns.value != -99999.0 else " data not available\r\n")
    temps = (twl.value, twl.value2, twl.value3, twl.value4, twl.value5, twl.value6)
    for temp in temps:
        f.write("U1")
        f.write("{:>11.3f}".format(temp) + "\r\n" if temp != -99999.0 else " data not available\r\n")
    f.write("\r\nREPORT COMPLETE\r\n")
    f.close()


message_ready = True


def status_message(msg):
    """
    This function updates the status file with status messages
    only when activated
    """
    global message_ready
    gp1_value = float(command_line("!gp1 value\r"))
    if gp1_value >= 1:
        count = 0
        while True:
            if message_ready:
                message_ready = False
                sl3_date, sl3_time = sl3_datetime()
                with open("/sd/status_log/status" + sl3_datetime()[0].replace("/", ".") + ".txt", "a") as f:
                    f.write("{0} {1}: {2}\r\n".format(sl3_date, sl3_time, msg))
                message_ready = True
                print(msg)
                return
            elif not message_ready:
                count += 1
                if count == 15:
                    print(msg)
                    return
                utime.sleep(0.025)
    else:
        print(msg)
        return


command_line("!file mkdir /sd/status_log/\r")
status_message("Initializing data...")

add_sns = []
cnt_meas = 1
while True:
    if command_line("!M" + str(cnt_meas) + " active\r").strip() == "Off":
        cnt_meas -= 1
        break
    elif command_line("!M" + str(cnt_meas) + " active\r").strip() == "On":
        if cnt_meas == 1:
            add_sns.append(PrimarySensor("M" + str(cnt_meas)))
        else:
            if command_line("!M" + str(cnt_meas) + " LABEL\r").strip() == "TWL":
                add_sns.append(TsunamiData("M" + str(cnt_meas)))
            else:
                add_sns.append(SecondarySensor("M" + str(cnt_meas)))
        cnt_meas += 1

ports_tag_message_formatter()
status_message("Initialization complete!")


def initialize_config():
    global add_sns, cnt_meas
    command_line("!file mkdir /sd/status_log/\r")
    add_sns = []
    cnt_meas = 1
    while True:
        if command_line("!M" + str(cnt_meas) + " active\r").strip() == "Off":
            cnt_meas -= 1
            break
        elif command_line("!M" + str(cnt_meas) + " active\r").strip() == "On":
            if cnt_meas == 1:
                add_sns.append(PrimarySensor("M" + str(cnt_meas)))
            else:
                if command_line("!M" + str(cnt_meas) + " LABEL\r").strip() == "TWL":
                    add_sns.append(TsunamiData("M" + str(cnt_meas)))
                else:
                    add_sns.append(SecondarySensor("M" + str(cnt_meas)))
            cnt_meas += 1

    ports_tag_message_formatter()
    status_message("Initialization complete!")


def decimal_to_binary(decimal_number):
    """
    This function coverts decimal to 18 bits binary number
    :param decimal_number: Decimal number
    :return: 18 bits binary number
    """
    bi_num = bin(abs(decimal_number)).replace("0b", "")
    bi_len = len(bi_num)
    bi_app = "0" * 18
    bi_app = bi_app[0:18 - bi_len]
    return bi_app + bi_num


def file_deleter(file_dir):
    """
    This function takes the path of the folder to be checked and deletes the files in that folder that are over
    3 years old
    :param file_dir: File directory to be deleted
    :return: Deletes files that are over 3 years from current date
    """
    count = 0
    while count < 10:
        try:
            file_sample = command_line("!file dir /sd/" + file_dir + "\r").strip().split("\r\n")[0]
            file_name = file_sample.split()[3]
            file_date = file_sample.split("status")[1].split(".")[0:3]
            file_date = list(map(int, file_date))
            file_date.extend([0, 0, 0])
            file_date = tuple(file_date)
            sl3_date = utime.localtime()[0:6]
            file_time_sec = utime.mktime(file_date)
            sl3_time_sec = utime.mktime(sl3_date)
            file_diff_day = round((sl3_time_sec - file_time_sec) / 86400)
            file_diff_year = "{:.3f}".format(file_diff_day / 360)
        except IndexError as e:
            status_message(str(e))
            break
        except OSError as e:
            status_message(str(e))
            break
        else:
            if file_diff_day > 1095:
                response = command_line("!FILE DEL /SD/" + file_dir + "/" + file_name + "\r").strip()
                msg = "{0}. It was {1} year(s) old which exceeds 3 years".format(response, file_diff_year)
                status_message(msg)
            else:
                msg = "The oldest file {0} is appx {1} years old. Files 3 years and older are deleted".format(
                    file_name, file_diff_year)
                status_message(msg)
                break
        count += 1


def get_log_date(log):
    """
    This function retrieves the date and time from a log string from a sensor
    :param log: Log
    :return: log_year, log_month, log_day, log_hour, log_minute, log_second
    """
    log_year = int(log[0][6:10])
    log_month = int((log[0])[0:2])
    log_day = int((log[0])[3:5])
    log_hour = int((log[1])[0:2])
    log_minute = int((log[1])[3:5])
    log_second = int((log[1])[6:8])
    return log_year, log_month, log_day, log_hour, log_minute, log_second


def goes_message_formatter():
    """
    This function formats the encoded data and prepares it for GOES transmission
    :return: GOES message
    """
    wind_bird = ""
    station_id = command_line("!STATION NAME\r").strip()
    tsunami = twl.get_encoded_tsunami()
    tx_battery = float(command_line("!BATT\r").strip())
    if tx_battery < 9.5:
        tx_battery = 9.5
    tx_battery = round((tx_battery - 9.5) * 10)
    if tx_battery > 63:
        tx_battery = 63
    tx_battery = pseudo_encoder(tx_battery, 1, True)
    tx_message = "P{0}{1}{2}@@{3}0{4}{5}8{6}{7}{8}#{9}<{10} {11}T{12}{13}{14}{15}{16}{17}{18}{19}{20}".format(
        station_id, dat.get_encoded_data(), sns.get_encoded_data(), pri.get_encoded_minute(),
        pri.get_encoded_sutron_day(), pri.get_encoded_hour(), pri.get_encoded_data(), mwstd.get_encoded_data(),
        mwout.get_encoded_data(), pri.get_encoded_redundant_data(), bat.get_encoded_data(), tx_battery,
        tsunami[0], tsunami[1], tsunami[2], tsunami[3], tsunami[4], tsunami[5], tsunami[6], tsunami[7], tsunami[8])
    for a_s in add_sns:
        if a_s.label == "WS":
            wind_bird += a_s.get_encoded_data()
        elif a_s.label == "WD":
            wind_bird += a_s.get_encoded_data()
        elif a_s.label == "WG":
            wind_bird += a_s.get_encoded_data()
            index = tx_message.find('<')
            if len(wind_bird) == 6:
                tx_message = tx_message[:index] + "3" + wind_bird + tx_message[index:]
            else:
                tx_message = tx_message[:index] + "3" + "??????" + tx_message[index:]
        elif a_s.label == "AT":
            index = tx_message.find('<')
            tx_message = tx_message[:index] + "4" + a_s.get_encoded_data() + tx_message[index:]
        elif a_s.label == "WT":
            index = tx_message.find('<')
            tx_message = tx_message[:index] + "5" + a_s.get_encoded_data() + tx_message[index:]
        elif a_s.label == "BARO":
            index = tx_message.find('<')
            tx_message = tx_message[:index] + "6" + a_s.get_encoded_data() + tx_message[index:]

    return tx_message


def pseudo_encoder(int_val, byt, pos=False):
    """
    Pseudobinary encoder function converts binary number from -131072 to 131071
    :param int_val: Decimal number
    :param byt: Number of bytes (1,2 or 3)
    :param pos: Positive only is True
    :return: Pseudobinary b format
    """
    int_val = int(str(int_val).replace(".", ""))
    iv = 0
    if int_val < 0 and pos:
        return "`@@"[:byt]
    if int_val < 0 and not pos:
        if byt == 1 and int_val < -31:
            return "`"
        if byt == 2 and int_val < -2047:
            return "`@"
        if byt == 3 and int_val < -131071:
            return "`@@"
        # Call decimal_to_binary Function
        bi_num = decimal_to_binary(int_val)
        bi_str = ""
        for bit in bi_num:
            if bit == "1":
                bi_str += "0"
            else:
                bi_str += "1"
        iv = int(bi_str, 2) + 1
    if int_val >= 0:
        if not pos:
            if byt == 1 and int_val > 30:
                return "_"
            if byt == 2 and int_val > 2046:
                return "_?"
            if byt == 3 and int_val > 131070:
                return "_??"
        elif pos:
            if byt == 1 and int_val > 62:
                return "?"
            if byt == 2 and int_val > 4094:
                return "??"
            if byt == 3 and int_val > 262142:
                return "???"
        iv = int_val
    bi_array = [iv >> 12, (iv >> 6) & 63, iv & 63]
    for i in range(3):
        if bi_array[i] != int(63):
            bi_array[i] += 64
    if byt == 1:
        return chr(bi_array[2])
    if byt == 2:
        return chr(bi_array[1]) + chr(bi_array[2])
    if byt == 3:
        return chr(bi_array[0]) + chr(bi_array[1]) + chr(bi_array[2])


@TASK
def delete_old_files():
    """
    This task checks the status_log folders and deletes the files that are over 3 years old.
    It utilizes the file_deleter() function
    """
    status_message("Checking for old files to delete...")
    file_deleter("status_log")


@TASK
def initialize_configuration():
    """
    This task initializes the configuration
    """
    initialize_config()


@TASK
def update_data():
    """
    This task updates the sensor objects
    """
    status_message("Updating all data...")
    for i in range(cnt_meas):
        if i == 0:
            add_sns[i].update_primary_data()
        else:
            if add_sns[i].label == "TWL":
                add_sns[i].update_tsunami_data()
            else:
                add_sns[i].update_secondary_data()
    ports_tag_message_formatter()
    status_message("Updates successful!")


@TXFORMAT
def goes_message(standard):
    """
    This transmission function returns the GOES message for transmission
    """
    status_message("Transmitting GOES message...")
    _ = standard  # neatly discards the input from sensor because it's not needed
    good_goes_message = goes_message_formatter()
    status_message("GOES transmission successful!")
    return good_goes_message
