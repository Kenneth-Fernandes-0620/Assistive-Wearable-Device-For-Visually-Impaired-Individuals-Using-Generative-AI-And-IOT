"""
GPS Interfacing with Raspberry Pi using Pyhton
http://www.electronicwings.com
"""

from collections import namedtuple

was_gps_loaded = False
Coordinate = namedtuple("Coordinate", ["latitude", "longitude"])


def load_gps():
    try:
        import serial  # import serial pacakge
        from time import sleep
        import webbrowser  # import package for opening link in browser
        import sys  # import system package

        def GPS_Info():
            global NMEA_buff
            global lat_in_degrees
            global long_in_degrees
            nmea_time = []
            nmea_latitude = []
            nmea_longitude = []
            nmea_time = NMEA_buff[0]  # extract time from GPGGA string
            nmea_latitude = NMEA_buff[1]  # extract latitude from GPGGA string
            nmea_longitude = NMEA_buff[3]  # extract longitude from GPGGA string

            print("NMEA Time: ", nmea_time, "\n")
            print(
                "NMEA Latitude:", nmea_latitude, "NMEA Longitude:", nmea_longitude, "\n"
            )

            lat = float(nmea_latitude)  # convert string into float for calculation
            longi = float(nmea_longitude)  # convertr string into float for calculation

            lat_in_degrees = convert_to_degrees(
                lat
            )  # get latitude in degree decimal format
            long_in_degrees = convert_to_degrees(
                longi
            )  # get longitude in degree decimal format

        # convert raw NMEA string into degree decimal format
        def convert_to_degrees(raw_value):
            decimal_value = raw_value / 100.00
            degrees = int(decimal_value)
            mm_mmmm = (decimal_value - int(decimal_value)) / 0.6
            position = degrees + mm_mmmm
            position = "%.4f" % (position)
            return position

        gpgga_info = "$GPGGA,"
        ser = serial.Serial("/dev/ttyS0")  # Open port with baud rate
        GPGGA_buffer = 0
        NMEA_buff = 0
        lat_in_degrees = 0
        long_in_degrees = 0

        try:

            received_data = (str)(ser.readline())  # read NMEA string received
            GPGGA_data_available = received_data.find(
                gpgga_info
            )  # check for NMEA GPGGA string
            if GPGGA_data_available > 0:
                GPGGA_buffer = received_data.split("$GPGGA,", 1)[
                    1
                ]  # store data coming after "$GPGGA," string
                NMEA_buff = GPGGA_buffer.split(
                    ","
                )  # store comma separated data in buffer
                GPS_Info()  # get time, latitude, longitude

        except KeyboardInterrupt:
            return map_link
    except:
        was_gps_loaded = False
        pass


def get_gps():
    if not was_gps_loaded:
        return f"12°56'03.2\"N 77°36'21.1\"E"
    return f"12°56'03.2\"N 77°36'21.1\"E"


def dms_to_dd(dms_str):
    # Split the latitude and longitude
    lat_str, lon_str = dms_str.split()

    # Convert latitude
    lat_deg = int(lat_str[0:2])
    lat_min = int(lat_str[3:5])
    lat_sec = float(lat_str[6:-2])
    lat_dir = lat_str[-1]

    # Convert longitude
    lon_deg = int(lon_str[0:2])
    lon_min = int(lon_str[3:5])
    lon_sec = float(lon_str[6:-2])
    lon_dir = lon_str[-1]

    # Convert to decimal degrees
    lat_dd = lat_deg + (lat_min / 60) + (lat_sec / 3600)
    lon_dd = lon_deg + (lon_min / 60) + (lon_sec / 3600)

    # Apply direction
    if lat_dir == "S":
        lat_dd = -lat_dd
    if lon_dir == "W":
        lon_dd = -lon_dd

    return f"{round(lat_dd,6)},{round(lon_dd,6)}"


if __name__ == "__main__":
    load_gps()
    print(get_gps())
