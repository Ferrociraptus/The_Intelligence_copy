from threading import Thread
from time import sleep

import serial
import serial.tools.list_ports

from Gripper_suspension.Force_graph import ForceGraph
from Classes.Vector_class import Vector
from Gripper_suspension.KalmanFilter_class import KalmanFilter

functions_sequence = [[], [], []]


def synchronize_in_thread(function):
    global functions_sequence

    def wrapper(*args, **kwargs):
        functions_sequence[0].append(function)
        functions_sequence[1].append(args)
        functions_sequence[2].append(kwargs)
        return None

    return wrapper


class GripSuspension(Thread):

    def __init__(self, port: str = None, baudrate: int = None, **kwargs):
        Thread.__init__(self)
        self.run_available = False
        self.data_buffer_len = 5
        self.sleep_time = 0.1
        self.buffer = []
        self.graph = None

        self.plus_x_filter = KalmanFilter(1e-2, 0.05 ** 2)
        self.minus_x_filter = KalmanFilter(1e-2, 0.05 ** 2)
        self.plus_y_filter = KalmanFilter(1e-2, 0.05 ** 2)
        self.minus_y_filter = KalmanFilter(1e-2, 0.05 ** 2)

        self.plus_x_cof = 0
        self.minus_x_cof = 0
        self.plus_y_cof = 0
        self.minus_y_cof = 0

        if (port is not None) and (baudrate is not None):
            self.serial = serial.Serial(port, baudrate, timeout=0.2)
        else:
            self.serial = None
        if kwargs.get("data_buffer", False):
            self.data_buffer_len = kwargs["data_buffer"]
        if kwargs.get("sleep_time", False):
            self.sleep_time = kwargs["sleep_time"]
        if kwargs.get("graph", False):
            self.graph = ForceGraph()

        self.start()

    def run(self) -> None:
        global functions_sequence

        self.run_available = True

        while self.run_available:
            sleep(self.sleep_time)

            if len(functions_sequence[0]) > 0:
                function = functions_sequence[0].pop(0)
                arguments = functions_sequence[1].pop(0)
                key_word_arguments = functions_sequence[2].pop(0)
                function(*arguments, **key_word_arguments)

            if self.serial is not None:
                if not self.serial.is_open:
                    self.serial.open()

                while self.serial.in_waiting:
                    try:
                        data: bytes = self.serial.readline()

                        if type(data) == bytes:
                            data: str = data.decode('utf-8').strip()

                        if data != "":
                            data = data.replace('$', '')
                            data = data.replace(';', '')
                            data = data.strip()
                            parse = data.split()
                            parse = {"+x": self.plus_x_filter.latest_noisy_measurement(float(parse[0][2:]))
                                           - self.plus_x_cof,
                                     "-x": self.minus_x_filter.latest_noisy_measurement(float(parse[1][2:]))
                                           - self.minus_x_cof,
                                     "+y": self.plus_y_filter.latest_noisy_measurement(float(parse[2][2:]))
                                           - self.plus_y_cof,
                                     "-y": self.minus_y_filter.latest_noisy_measurement(float(parse[3][2:]))
                                           - self.minus_y_cof}
                            vec1 = Vector((0, 0, 0), (-parse['-x'], 0, parse['-x']))
                            vec2 = Vector((0, 0, 0), (parse['+x'], 0, parse['+x']))
                            vec3 = Vector((0, 0, 0), (0, -parse['-y'], parse['-y']))
                            vec4 = Vector((0, 0, 0), (0, parse['+y'], parse['+y']))

                            sum_vec = vec1 + vec2 + vec3 + vec4
                            sum_vec.set_length(abs(parse['-x']) + abs(parse['+x'])
                                               + abs(parse['-y']) + abs(parse['+y']))

                            if len(self.buffer) >= self.data_buffer_len:
                                self.buffer.append((sum_vec, parse))
                                self.buffer.pop(0)
                            else:
                                self.buffer.append((sum_vec, parse))

                            if self.graph is not None:
                                self.graph.add_to_buffer((sum_vec, parse))
                    except:
                        pass

    @synchronize_in_thread
    def connect(self, port: str, baudrate: int):
        try:
            self.serial = serial.Serial(port, baudrate, timeout=0.2)
        except serial.SerialException:
            print("Can not connect to serial port.")
            print("Available ports:")
            for port in list(d.device for d in serial.tools.list_ports.comports()):
                print(port)

    @synchronize_in_thread
    def disconnect(self):
        if self.serial is not None:
            self.serial.close()
            self.serial = None

    @synchronize_in_thread
    def send_to_serial(self, information: str):
        if self.serial is not None:
            if not self.serial.is_open:
                self.serial.open()
            self.serial.write((information + "\n").encode("utf-8"))
            self.serial.reset_input_buffer()
        else:
            Exception("Error sending to Serial.")

    def terminate_thread(self):
        self.disconnect()
        if self.graph is not None:
            self.graph.terminate_thread()
        self.run_available = False
        self.graph.join()
        self.join()

    def latest_val(self):
        return self.buffer[-1]

    def set_zero(self):
        val = self.latest_val()
        self.plus_x_cof = -val[1]['+x']
        self.minus_x_cof = -val[1]['-x']
        self.plus_y_cof = -val[1]['+y']
        self.minus_y_cof = -val[1]['-y']

    def no_zero(self):
        self.plus_x_cof = 0
        self.minus_x_cof = 0
        self.plus_y_cof = 0
        self.minus_y_cof = 0
