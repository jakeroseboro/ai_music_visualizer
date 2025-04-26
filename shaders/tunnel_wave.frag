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

    float angle = atan(uv.y, uv.x);
    float radius = length(uv);

    float waves = sin(10.0 * angle + iTime * 2.0 + sin(radius * 20.0 - iTime * 5.0)) * 0.5 + 0.5;
    float tunnel = smoothstep(0.2, 0.0, radius + iBass * 0.5);

    vec3 color = mix(vec3(0.05, 0.05, 0.15), vec3(0.3, 0.5, 1.0), waves) * tunnel;

    fragColor = vec4(color, 1.0);
}
