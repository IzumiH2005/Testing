shader_type canvas_item;
// Transforme un sprite en « écho » : la valeur est remappée sur la rampe cyan de la palette.
uniform float alpha : hint_range(0.0, 1.0) = 0.6;
uniform float flash : hint_range(0.0, 1.0) = 0.0;
const vec3 C_Q = vec3(0.055, 0.290, 0.361);
const vec3 C_T = vec3(0.102, 0.541, 0.620);
const vec3 C_C = vec3(0.247, 0.816, 0.831);
const vec3 C_E = vec3(0.659, 1.0, 0.941);
void fragment() {
	vec4 col = texture(TEXTURE, UV);
	float l = dot(col.rgb, vec3(0.299, 0.587, 0.114));
	vec3 o = l < 0.16 ? C_Q : (l < 0.38 ? C_T : (l < 0.62 ? C_C : C_E));
	o = mix(o, vec3(1.0), flash);
	COLOR = vec4(o, col.a * alpha);
}
