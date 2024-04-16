import serial
import crc8
import logging
import time

#REV 11/1 PROTOCOL update (PAR su 4 Byte vs 2 prec) OK su .ino  Ardu_slave5.ino
#MA su Ardu ! BAUD max 9600 pare ! da capire eprche'
#Refer to https://crccalc.com/
#TODO
# merge in cli_master6.py as a proper class, manage errors comms


CLI_REV = "0.8"

##defaults
RETRIES_NUM = 3
SERIAL_TIMEOUT = 2
# BAUD        = 19200
BAUD = 9600

DEFAULT_COM = "COM6"  # com_port = '/dev/ttyUSB0'    linux or mac
## RES_ID = CMD_ID + 0x80     #!MAKE SUME max CMDs < 128 = 0x80 !
SER_TIMEOUT_DUR = 1
SER_DELAY0 = 0.2

CMD_RANDOM = 0x04
CMD_ADC = 0x02
CMD_GET_FWVERSION = 0x03
CMD_HELLO = 0x09
CMD_GET_TARGET_TYPE = 0x05
CMD_READ_HR = 0x12
CMD_WRITE_HR = 0x13
CMD_ASCII_CONSOLE = "a"


# Function to create a command packet
def create_command_packet(cmd_id, cmd_parameter):
    # Convert cmd_id to integer if it's a string
    if isinstance(cmd_id, str):
        cmd_id = int(cmd_id, 16)

    print(f"{cmd_parameter=}  {type(cmd_parameter)=}")

    # Check if cmd_parameter is a bytes object
    if isinstance(cmd_parameter, bytes):
        cmd_parameter_int = int.from_bytes(cmd_parameter, 'little')
    else:
        cmd_parameter_int = int(cmd_parameter)

    # Check if cmd_parameter is within the 4-byte range
    if not (0 <= cmd_parameter_int <= 0xFFFFFFFF):
        print(' ValueError("cmd_parameter out of 4-byte range)')

    # Convert parameters into bytes
    cmd_id_bytes = cmd_id.to_bytes(1, 'little')
    # cmd_parameter_bytes = cmd_parameter.to_bytes(4, 'little')
    # cmd_parameter_bytes = cmd_parameter #OK as default

    # Assuming cmd_parameter is a string representing an integer
    if isinstance(cmd_parameter, str):
        cmd_parameter_int = int(cmd_parameter)  # Convert string to integer
        cmd_parameter_bytes = cmd_parameter_int.to_bytes(1, byteorder='little')  # Convert integer to bytes
    else:
        cmd_parameter_bytes = cmd_parameter

    # Calculate CRC8
    hash_obj = crc8.crc8()
    hash_obj.update(cmd_id_bytes + cmd_parameter_bytes)
    crc8_byte = hash_obj.digest()

    # Return the command packet
    return cmd_id_bytes + cmd_parameter_bytes + crc8_byte


def parse_response_packet(packet, expected_resid) -> (str, str):
    # Convert each byte in the packet to hex and join them into a string
    print(f" {type(packet)=}")
    packet_hex = ' '.join(f'{byte:02x}' for byte in packet)

    print(f"Rx packet= 0x{packet_hex}  len= {len(packet)}")
    if len(packet) != 6:
        print(f"Invalid response length  len= {len(packet)}")
        return "-1", "-1"

    res_id = packet[0]
    if not isinstance(res_id, int):
        print(f" Error res_id is not an integer {type(res_id)=}")
        raise ValueError("res_id is not an integer")

    if expected_resid != res_id:
        print(f"RES_ID ERROR: {expected_resid=} got {res_id=}!")
        return "-1", "-1"
    else:
        print("RES_ID is correct")

    response = int.from_bytes(packet[1:5], 'little')
    if not isinstance(response, int):
        print(f" Error response is not an integer {type(response)=}")
        raise ValueError("response is not an integer")

    crc8_received = packet[5]

    # Verify CRC8
    crc8_calculated = 0
    try:
        hash_obj = crc8.crc8()
        hash_obj.update(packet[:5])
        crc8_calculated = hash_obj.digest()[0]
    except Exception as e:
        print(f"error in crc8 calc {e}")

    if crc8_received != crc8_calculated:
        # print(f'ValueError("CRC8 mismatch")! {crc8_received=} {crc8_calculated=} but ignored!')
        print(
            f'CRC8 mismatch: crc8_received=0x{crc8_received:02x} crc8_calculated=0x{crc8_calculated:02x} but ignored!')
    else:
        print("CRC OK")

    # print(f" Returning: res_id=0x{res_id:02x} response=0x{response:08x}")
    return f'{res_id:02x}', f'{response:08x}'


def read_full_packet(ser, expected_length) -> bytearray:
    # Initialize buffer with zeros
    buffer = bytearray(expected_length)

    start_time = time.time()
    index = 0  # To keep track of the next position to fill in the buffer

    while index < expected_length:
        if ser.in_waiting > 0:
            byte_read = ser.read(1)
            buffer[index] = byte_read[0]
            index += 1
            # print(f"rx: {buffer=} {len(buffer)=}")
        else:
            if time.time() - start_time > SERIAL_TIMEOUT:  # Timeout after 5 seconds
                ser.reset_input_buffer()
                raise TimeoutError("Timed out waiting for packet")

    ser.reset_input_buffer()
    return buffer


def send_cmd_read_hr1(ser):
    '''

    hard coded command to read holding register #1 for test

    '''

    # command_packet = create_command_packet(cmd_id, cmd_parameter)

    command_packet = b'\x12\x00\x00\x01\xf1'  # Richiesta valore registro modbus HR 1

    for r in range(RETRIES_NUM):
        print(f"retry # {r + 1}/{RETRIES_NUM}")
        # Send command
        print(f"Sending CMD: {command_packet=} ")
        ser.write(command_packet)
        try:
            # Read a full packet from the serial port
            response_packet = read_full_packet(ser, 6)
        except TimeoutError as e:
            print(f"Error timeout: {e}")
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

        # Process the packet
        try:
            res_id, response = parse_response_packet(response_packet, 0x12 + 0x80)
            print(f"Response ID: {res_id}, Response payload: {response}")
            if res_id != "-1":
                break
        except Exception as e:
            print(f"An error occurred in parse_response_packet(): {e}")


def send_cmd_read_hr65(ser):
    '''

        hard coded command to read holding register #65 =0x41 for test

        '''

    command_packet = b'\x12\x00\x00\x41\x36'  # Richiesta valore registro modbus HR 65
    response_packet = 0
    print(f"Sending CMD: {command_packet=} ")
    # print(f"   {cmd_id=}   0x{hex_cmdid} {cmd_parameter=} {hex_cmdpar=}")
    for r in range(RETRIES_NUM):
        print(f"retry # {r + 1}/{RETRIES_NUM}")
        # Send command
        ser.write(command_packet)
        try:
            # Read a full packet from the serial port
            response_packet = read_full_packet(ser, 6)
        except TimeoutError as e:
            print(f"Error timeout: {e}")
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

        # Process the packet
        try:
            res_id, response = parse_response_packet(response_packet, 0x12 + 0x80)
            print(f"Response ID: {res_id}, Response payload: {response}")
            if res_id != "-1":
                break
        except Exception as e:
            print(f"An error occurred in parse_response_packet(): {e}")


def decode_firmware_versionHEX(version_hex):
    '''

    :param version_hex: string of hexadecimal character
    :return:
    '''
    print(f" {version_hex=}")

    if len(version_hex) < 8:  # Each byte is represented by two hex characters
        print('In decode_firmware_versionHEX():  ValueError("Hex string is too short to contain a valid version.')
        return f"error"
    version_byte = bytes.fromhex(version_hex)
    major = version_byte[0]
    minor = version_byte[1]
    patch = version_byte[2]
    print(f"FW HEX Ver= {major}.{minor}.{patch}")
    return f"{major}.{minor}.{patch}"


def gotoAsciiConsole(ser):
    cmd_id = CMD_ASCII_CONSOLE

    # ascii_value = ord('a')  #== CMD_ASCII_CONSOLE == 97 dec
    # hex_value = hex(ascii_value)  #= 0x61
    cmd_id = ord('a')
    cmd_parameter = b'\x61\x61\x61\x61'
    cmd_parameter_int = int.from_bytes(cmd_parameter, 'little')

    command_packet = create_command_packet(cmd_id, cmd_parameter)

    hex_cmdid = format(int(cmd_id), '04X')
    hex_cmdpar = format(cmd_parameter_int, '08X')
    print(f"Sending CMD: {command_packet=} ")
    print(f"   {cmd_id=}   0x{hex_cmdid} {cmd_parameter=} {hex_cmdpar=}")
    # Send command
    ser.write(command_packet)

    response_packet = 0
    try:
        # Read a full packet from the serial port
        response_packet = read_full_packet(ser, 6)
    except TimeoutError as e:
        print(f"Error timeout: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    # Process the packet (your parsing function here)
    try:
        expected_resid = cmd_id + 0x80
        res_id, response = parse_response_packet(response_packet, expected_resid)
        print(f"Response ID: {res_id}, Response payload: {response}")
    except Exception as e:
        print(f"An error occurred in parse_response_packet(): {e}")

    #TODO
    #handle an ascii console here


def decode_firmware_version(version_byte):
    if len(version_byte) < 4:
        raise ValueError("Byte data is too short to contain a valid version.")

    major = version_byte[0]
    minor = version_byte[1]
    patch = version_byte[2]
    print(f" Fe VEr= {major}.{minor}.{patch}")
    return f"{major}.{minor}.{patch}"


def main():
    # Serial port configuration
    port = DEFAULT_COM  # Change to your port
    baudrate = BAUD  # Change to your baud rate

    # Open serial port

    try:
        ser = serial.Serial(port, baudrate,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=SER_TIMEOUT_DUR)
    #except serial.SerialException as e:
    except Exception as e:
        logging.error(f"Serial port error: {e}")
        exit()

    ser.reset_input_buffer()

    while True:
        user_input = input("\n\rEnter command id in hex or 'q' to quit: ").strip()
        if user_input == "q":
            return
        if user_input == "a":
            gotoAsciiConsole(ser)
            return
        if user_input == "h":
            send_cmd_read_hr1(ser)
        elif user_input == "j":
            send_cmd_read_hr65(ser)
        else:
            # Create a command packet
            try:
                cmd_id = int(user_input, 16)
            except Exception as e:
                logging.error(f"User input error {e}  {user_input=}")
                return

            if cmd_id == CMD_READ_HR:
                par = int(input("\n\rEnter address of Modbus HR (in dec): ").strip())

                hex_bytes = par.to_bytes(4, byteorder='big')
                cmd_parameter = b'\x00\x00' + hex_bytes[-2:]
                print(f"user entered {par=}  {hex_bytes=} {cmd_parameter=}")
            else:
                cmd_parameter = b'\x02\x03\x04\x05'  # Example parameter

            manageCommand(ser, cmd_id, cmd_parameter)


def manageCommand(ser, cmd_id, cmd_parameter, DEBUG=True):
    #broken in many case of CMD 0x12 READ_HR with the user paramente FIXME
    if cmd_parameter.isdigit():
        #     cmd_parameter_bytes = cmd_parameter.to_bytes(4, byteorder='little')  # Convert integer to bytes
        cmd_parameter_int = int(cmd_parameter)
    else:
        cmd_parameter_int = int.from_bytes(cmd_parameter, 'little')

    #OK  cmd_parameter_int = int.from_bytes(cmd_parameter, 'little')
    command_packet = create_command_packet(cmd_id, cmd_parameter)

    hex_cmdid = format(int(cmd_id), '04X')
    hex_cmdpar = format(cmd_parameter_int, '08X')
    print(f"Sending CMD: {command_packet=} ")
    print(f"   {cmd_id=}   0x{hex_cmdid} {cmd_parameter=} {hex_cmdpar=}")
    expected_resid = cmd_id + 0x80
    res_id = "-1"
    response = 0
    for r in range(RETRIES_NUM):
        print(f"retry # {r + 1}/{RETRIES_NUM}")
        # Send command
        ser.write(command_packet)
        try:
            # Read a full packet from the serial port
            response_packet = read_full_packet(ser, 6)
        except TimeoutError as e:
            print(f"Error timeout: {e}")
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

        # Process the packet
        try:
            res_id, response = parse_response_packet(response_packet, expected_resid)
            print(f"Response ID: {res_id}, Response payload: {response}")
            if res_id != "-1":
                break
        except Exception as e:
            print(f"An error occurred in parse_response_packet(): {e}")

    print(f" {expected_resid=} {res_id=} {type(expected_resid)=}")

    if res_id == hex(expected_resid) and cmd_id == CMD_GET_FWVERSION:
        print(f"  FW Version=  {decode_firmware_versionHEX(response)}")

    return res_id, response


if __name__ == "__main__":
    main()
