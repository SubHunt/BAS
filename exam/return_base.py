import threading
import time

from pymavlink import mavutil

from drone_monitor import DroneState, monitor_loop
from flight_control import set_mode_guided


def connect(connection_string: str = "tcp:127.0.0.1:14550") -> mavutil.mavlink_connection:
    """
    Подключение к SITL/дрону ArduPilot.
    В Mission Planner можно настроить выдачу MAVLink по TCP на этот адрес и порт
    """
    master = mavutil.mavlink_connection(connection_string)

    # Ждём первое HEARTBEAT от автопилота
    result = master.wait_heartbeat(timeout=1)

    if result is None:  # None будет в случае таймаута
        return None

    print(f"Подключено к системе {master.target_system}, компонент {master.target_component}")
    return master


def goto_local_ned(master, x=0, y=0, z=-10, coordinate_frame=mavutil.mavlink.MAV_FRAME_LOCAL_NED):
    """
    Полёт в точку (x, y, z) в системе LOCAL_NED (X — север, Y — восток, Z — вниз).
    Дрон уже должен быть ARM и в GUIDED.
    """
    coordinate_frame = mavutil.mavlink.MAV_FRAME_LOCAL_NED  # или MAV_FRAME_LOCAL_OFFSET_NED / BODY_OFFSET_NED

    type_mask = 0b0000111111111000  # 4088: используем ТОЛЬКО позицию x,y,z [web:5][web:23]

    master.mav.set_position_target_local_ned_send(
        0,                          # time_boot_ms (не важно)
        master.target_system,       # target_system
        master.target_component,    # target_component
        coordinate_frame,
        type_mask,
        x, y, z,                    # позиция
        0, 0, 0,                    # скорости игнорируются маской
        0, 0, 0,                    # ускорения игнорируются маской
        0, 0                        # yaw / yaw_rate игнорируются маской
    )

if __name__ == "__main__":
    master = connect(connection_string="tcp:127.0.0.1:14550")

    state = DroneState()  # датакласс состояний дрона, будет обновляться

    stop_flag = {"stop": False}

    # В отдельном потоке запускаем цикл мониторинга
    monitor_thread = threading.Thread(
        target=monitor_loop,
        args=(master, state, lambda: stop_flag["stop"]),
        daemon=False,  # чтобы поток останавливался, если остановилась основная программа (например при ошибке)
    )

    monitor_thread.start()

    set_mode_guided(master)

    time.sleep(1)
    print("Старт перемещения")
    goto_local_ned(master, x=5, y=2, z=-7)
    for _ in range(10):
        print(state.lat_deg, state.lon_deg)
        time.sleep(1)

    stop_flag["stop"] = True
    monitor_thread.join(timeout=2.0)

