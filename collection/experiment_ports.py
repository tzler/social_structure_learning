"""Functions to find and open hardware using relevant ports."""

import sys
import glob
import serial


def list_ports():
    """List all ports connected via USB."""

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def select_port(name):
    """Select port from available USB connections"""

    # get available ports
    ports = list_ports()
    # select from list
    for iPort in ports:
        if iPort.find(name) > 0:
            port = iPort

    return port


class SD9:
    """Signals SD9 to administer shock."""

    def __init__(self):
        """Initiate connection to SD9."""
        # specificy port and extract location
        name = 'usbmodem'
        port = select_port(name)
        print port
        # specificy communication rate and establish connection
        bRate = 57600
        SD9_port = serial.Serial(port, baudrate=bRate)
        # close possibly open ports to avoid errors
        SD9_port.close()
        SD9_port.open()
        # preserve connection
        self.SD9 = SD9_port

    def shock(self):
        """Administer shock."""
        self.SD9.write(b"t\r")

    def close(self):
        """Close Port."""
        self.SD9.close()


class biopac:
    """Signals stimulus information to biopack."""

    def __init__(self):
        """Establish connection with biopac."""
        # specify por and extract location
        name = 'BBTKUSBTTL'
        port = select_port(name)
        # specify communication rate and open connection
        bRate = 115200
        self.biopac = serial.Serial(port, baudrate=bRate)

    def initiate(self):
        """Trigger biopack to initialize, set all channels to zero."""
        self.biopac.write('0')
        self.biopac.write('255')
        self.biopac.write('00')
        self.biopac.write('88')

    def begin(self):
        """Signal begining of experiment."""
        self.biopac.write('00')

    def end_stim(self):
        """Set all channels to zero."""
        self.biopac.write('00')

    def US(self):
        """Send stimulus marker for US to channel 3."""
        self.biopac.write('55')

    def CS(self, cs_type):
        """Send signal for CS (+) 0 -> 1 or (-) 0 -> 2)."""
        self.biopac.write('%s' % (cs_type + 1) * 2)
        # '* 2' just repeats the string

    def end(self):
        """Signal end of experiment to biopac."""
        self.biopac.write('88')
