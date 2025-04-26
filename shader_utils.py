def load_shader(shader_name):
    with open(f"shaders/common.vert") as f:
        vertex = f.read()
    with open(f"shaders/{shader_name}.frag") as f:
        fragment = f.read()
    return vertex, fragment