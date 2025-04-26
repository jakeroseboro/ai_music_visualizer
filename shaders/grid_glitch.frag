#version 330 core

in vec2 v_uv;
out vec4 fragColor;

uniform float iTime;
uniform vec2 iResolution;
uniform float iBass;

void main()
{
    vec2 uv = (v_uv - 0.5) * 2.0;
    uv.x *= iResolution.x / iResolution.y;

    vec2 grid = fract(uv * 10.0 + iTime * 0.5);
    float line = min(grid.x, grid.y);

    float glitch = step(0.02 + iBass * 0.3, line);

    vec3 color = mix(vec3(0.0, 0.0, 0.0), vec3(0.0, 0.8, 1.0), glitch);

    fragColor = vec4(color, 1.0);
}
