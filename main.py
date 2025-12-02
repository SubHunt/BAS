import time
from pymavlink import mavutil

TARGET_SYSTEM = 1  # ID дрона
TARGET_COMPONENT = 1  # ID автопилота
GUIDED_MODE = 4  # ID режима
TARGET_HIG = 3  # целевая высота
current_alt = 0  # высота для работы алгоритма

# Отправка команд


def connect_to_autopilot(connection_string):
    print(f"Подключаемся к автопилоту по адресу: {connection_string}...")
    master = mavutil.mavlink.connection(connection_string)
    master = wait_hearbeat()
    print("Соединение было установлено.")
    return master
# Подключение к дрону


def send_command(master, command, param1=0, param7=0):
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        command,
        0,
        param1,
        param7
    )
    return master.recv_match(type='COMMAND_ACK', blocking=True, timeout=5)


# Миссия
def simple_mission():
    # Подключение к симулятору
    print('Подключаемся к симулятору.')
    connection_string = 'udp: 127:0:0:1:14550'
    master = connect_to_autopilot(connection_string)
    # Переключаем режим
    print('Переключаем режим.')
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, GUIDED_MODE
    )
    # Арминг
    print('Армимся.')
    ack = send_command(
        master, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, param1=0)

    # Взлет
    print('Взлетаем.')
    ack = send_command(
        master, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, param7=TARGET_HIG)
    # Удержание высоты
    print('Пытаемся удержать высоту.')
    while current_alt < TARGET_HIG * 0.98:
        msg = master.recv_math(type='GLOBAL_POSITION_INT',
                               blocking=True, timeout=1)
        if msg:
            current_alt = msg.relative_alt / 1000
            print("Текущая высота:", current_alt)
        if time.time() - start_time > 30:
            print("Ошибка времени ожидания. Прерывание")
            break
    # Блок ожидания
    print("Ждем 5 секунд.")
    time.sleep(5)
    # Посадка
    print("Выполняется посадка")
    ack = send_command(
        master, mavutil.mavlink.MAV_CMD_NAV_LAND)
    # Дизарм
    print("Дизармимся.")
    send_command(
        master, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, param1=0)

    if __name__ == '__main__':
        simple_mission()
