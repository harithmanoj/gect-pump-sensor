
#	Cold Chain Management Desktop is free software : you can redistribute 
#   it and /or modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation, either version 3 of the 
#   License, or (at your option) any later version.

#	Cold Chain Management Desktop is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with Cold Chain Management Desktop. 
#   If not, see < https://www.gnu.org/licenses/>.

import serial
import serial.tools.list_ports

# Class to Manage Serial Communication
class SerialCommunication:

    # Return Port info with the argument in its description, 
    # "fail" if not found
    def acquirePortsWith(key):
        ports = SerialCommunication.acquirePorts()

        for p in ports:
            if key in p.description:
                return p
    
        return "fail"
    
    # Returns port info for all ports connected
    def acquirePorts():
        return list(serial.tools.list_ports.comports())
    
    # Initialise a stream with given port and in given baud rate
    def __init__(self, port, rate, timeout):

        self.portName = port[0]
        
        self.baudRate = rate

        self.stream = serial.Serial(
            port = self.portName,
            baudrate = self.baudRate,
            timeout = timeout )
    
    # write to created stream
    def write(self, message):
        return self.stream.write(message.encode())
    
    # read from created stream
    def read(self):
        return self.stream.read()

    def readline(self):
        return self.stream.readline()

    def waiting(self):
        return self.stream.in_waiting

    def checkStatus(self):
        self.stream.isOpen()

