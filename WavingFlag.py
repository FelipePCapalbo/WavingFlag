import cv2
import numpy as np
import imageio

# Configurações da imagem
flag_img_path = "bandeira.png"  # imagem no mesmo diretório
frame_width, frame_height = 400, 227  # ajuste conforme o firmware permitir

# Parâmetros do GIF
frame_count = 15                # firmware aceita 15 frames
interval_time_ms = 80           # usará no programa depois (Interval time)
fps = 1000 / interval_time_ms
duration = frame_count / fps

# Carregar imagem
flag = cv2.imread(flag_img_path, cv2.IMREAD_UNCHANGED)
if flag is None:
    raise FileNotFoundError("Imagem da bandeira não encontrada no diretório!")

flag = cv2.resize(flag, (frame_width, frame_height))

# Parâmetros da onda
amplitude = 4                   # ajuste fino
wavelength = 100
wave_speed = 2 * np.pi / frame_count   # fecha ciclo em 15 frames

# Grids para remap
map_y, map_x = np.indices((frame_height, frame_width), dtype=np.float32)

# Lista de frames para o GIF
frames = []

for frame in range(frame_count):
    t = frame * wave_speed
    dx = amplitude * np.sin(2 * np.pi * map_y / wavelength + t)
    map_x_warped = map_x + dx

    waved_flag = cv2.remap(flag, map_x_warped, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    waved_flag_rgb = cv2.cvtColor(waved_flag, cv2.COLOR_BGR2RGB)
    frames.append(waved_flag_rgb)

# Exportar GIF perfeito com 15 frames
imageio.mimsave('bandeira.gif', frames, duration=interval_time_ms/1000)

print("✅ GIF de 15 frames gerado: bandeira.gif")
