import dateutil
from datetime import datetime

class Connection:
    '''Connection class
       A class that holds information about the transport means (e.g. the trains) and the times of a connection
    '''
    def __init__(self, destination_x, destination_y, departure, arrival, transport_means):
        '''
        Connection constructor
        :param destination_x: the latitude of the destination
        :param destination_y: the longitude of the destination
        :param departure: a string containing the datetime for the departure
        :param arrival: a string containing the datetime for the arrival
        :param transport_means: a list of the transport means of the connection (e.g. ['IC 5'])
        '''

        if (isinstance(destination_x,float) and isinstance(destination_y,float) and
            isinstance(departure,str) and isinstance(arrival,str) and
            isinstance(transport_means,list)):
            self.destination_x = destination_x
            self.destination_y = destination_y
            self.transport_means = transport_means

            self.departure_time = dateutil.parser.parse(departure.split('+')[0])
            self.arrival_time = dateutil.parser.parse(arrival.split('+')[0])
        else:
            raise AttributeError

    def __str__(self):
        return "{}: {}->{}".format(self.transport_means, self.departure_time, self.arrival_time)

    def get_unix_departure_time(self):
        '''
        Method get_Unix_departure_time
        Returns the local time of departure as a Unix timestamp
        '''
        return int((self.departure_time - datetime(1970,1,1)).total_seconds())

    def get_unix_arrival_time(self):
        '''
        Method get_Unix_arrival_time
        Returns the local time of arrival as a Unix timestamp
        '''
        return int((self.arrival_time - datetime(1970,1,1)).total_seconds())