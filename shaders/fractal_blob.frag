#version 330 core

in vec2 v_uv;
out vec4 fragColor;

uniform float iTime;
uniform vec2 iResolution;
uniform float iBass;

float noise(vec2 p) {
    return fract(sin(dot(p, vec2(23.14069263277926, 2.665144142690225))) * 43758.5453);
}

float fbm(vec2 p) {
    float v = 0.0;
    float a = 0.5;
    vec2 shift = vec2(100);
    for (int i = 0; i < 4; ++i) {
        v += a * noise(p);
        p = p * 2.0 + shift;
        a *= 0.5;
    }
    return v;
}

void main() {
    vec2 uv = (v_uv - 0.5) * 2.0;
    uv.x *= iResolution.x / iResolution.y;

    float r = length(uv);
    float a = atan(uv.y, uv.x);

    float n = fbm(vec2(a * 1.0, r * 2.0 - iTime * 0.5));
    float blob = smoothstep(0.3 + iBass * 0.5, 0.1, r + n * 0.2);

    vec3 col = mix(vec3(0.1, 0.0, 0.2), vec3(0.8, 0.2, 1.0), blob);

    fragColor = vec4(col, 1.0);
}
