import os
import sys
import numpy as np
import pygame
import moderngl
import imageio

from scene_generator import SceneGenerator
from scene_fader import SceneFader
from audio_utils import detect_kick
from shader_utils import load_shader
from moviepy import VideoFileClip, AudioFileClip

WIDTH, HEIGHT = 1280, 720
FPS = 30

def ask_input():
    audio_path = input("🎵 Enter path to your input audio file (.wav or .mp3): ").strip()
    while not os.path.exists(audio_path):
        print("⚠️ File not found, try again.")
        audio_path = input("🎵 Enter path to your input audio file (.wav or .mp3): ").strip()

    shader_choice = input("🌀 Choose shader style (fractal_blob / tunnel_wave / grid_glitch / storm_warp): ").strip()
    prompts = input("🖼️ Enter comma-separated AI prompts for scenes (ex: 'psychedelic mushrooms, cosmic desert'): ").strip()

    prompts = [p.strip() for p in prompts.split(",")]
    return audio_path, shader_choice, prompts

def main():
    audio_path, shader_choice, prompts = ask_input()

    # 1. Generate scenes
    scene_gen = SceneGenerator(prompts)
    scene_paths = scene_gen.generate()

    # 2. Setup graphics
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
    ctx = moderngl.create_context()
    ctx.viewport = (0, 0, WIDTH, HEIGHT)

    vertex_shader, fragment_shader = load_shader(shader_choice)
    prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    vertices = np.array([
        -1, -1,  0, 0,
         1, -1,  1, 0,
        -1,  1,  0, 1,
        -1,  1,  0, 1,
         1, -1,  1, 0,
         1,  1,  1, 1
    ], dtype='f4')
    vbo = ctx.buffer(vertices.tobytes())
    vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_uv')

    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    audio_data = pygame.mixer.Sound(audio_path).get_raw()
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    audio_pos = 0
    chunk_size = 1024

    fader = SceneFader(ctx, scene_paths)

    time_val = 0.0
    clock = pygame.time.Clock()
    frames = []

    while pygame.mixer.music.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if audio_pos + chunk_size < len(audio_array):
            chunk = audio_array[audio_pos:audio_pos+chunk_size]
            fft = np.abs(np.fft.fft(chunk)[:chunk_size // 2])
            bass = np.mean(fft[0:20]) / 5000.0
            kick = 1.0 if detect_kick(fft) else 0.0
            audio_pos += chunk_size
        else:
            bass, kick = 0.0, 0.0

        fader.update(clock.get_time() / 1000.0)

        if 'iTime' in prog:
            prog['iTime'].value = time_val
        if 'iResolution' in prog:
            prog['iResolution'].value = (WIDTH, HEIGHT)
        if 'iBass' in prog:
            prog['iBass'].value = bass
        if 'kick' in prog:
            prog['kick'].value = kick
        if 'mix_factor' in prog:
            fader.bind(prog)

        ctx.clear()
        vao.render()

        frame = pygame.image.tostring(screen, "RGB")
        frames.append(frame)

        pygame.display.flip()
        time_val += clock.get_time() / 1000.0
        clock.tick(FPS)

    # Save video
    writer = imageio.get_writer('output_video.mp4', fps=FPS)
    for frame in frames:
        img = np.frombuffer(frame, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
        writer.append_data(img)
    writer.close()

    video_clip = VideoFileClip("output_video.mp4")
    audio_clip = AudioFileClip(audio_path)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile("final_output.mp4", codec='libx264')

    pygame.quit()
    print("✅ Final output saved: final_output.mp4")

if __name__ == "__main__":
    main()
