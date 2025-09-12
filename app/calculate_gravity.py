import time
from typing import final
import math

# time simulation
frame = 0
t0 = time.time()
fps = 30
max_fps = 50

# Gravity simulation
g = 9.81*3 # m/s²
p_vel = 0 # previous vel
vel = 0
p_frame_time = 0
start_pos = 1000 # meters
total_move = 0
object_drag = 0.001

while True:
    
    actual_time = time.time() - t0
    delta_time = actual_time-p_frame_time
    vel += delta_time * g - (object_drag*vel*vel)
    step_move = (vel + p_vel) / 2 * delta_time
    start_pos -= step_move
    total_move += step_move

    # Colision
    if total_move >= 5:
        total_move = 5
        vel = -vel*0.5#-vel*0.25

    p_vel = vel
    p_frame_time = actual_time
    print(f"{round(frame/max_fps*22, 1)}%" + "{top: " + f"{total_move*20}px" + "}")

    # print(f"""\n\n=== START ===
    # TIME: {actual_time}
    # Total Move: {total_move}
    # Vel: {vel}""")

    t_passed = time.time() - t0
    t_to_next_frame = (frame+1)/fps-(t_passed)
    if t_to_next_frame < 0:
        frame = math.floor(t_passed*fps)
        t_to_next_frame = max(0, (frame+1)/fps - (time.time() - t0))
        # print(f"=== TIME CONTROL === \nframe: {frame} \n{t_passed:.20f}")

    # print(t_to_next_frame)
    time.sleep(t_to_next_frame)

    if frame>max_fps:
        break