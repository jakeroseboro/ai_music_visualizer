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

    float warp = sin(5.0 * length(uv) - iTime * 2.0) * 0.3;
    uv += warp * normalize(uv) * (iBass * 0.5);

    vec3 color = vec3(0.2, 0.4, 0.8) * (1.0 - length(uv));

    fragColor = vec4(color, 1.0);
}
