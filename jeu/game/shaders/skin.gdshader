shader_type canvas_item;
// Remplace les 3 couleurs de l'écharpe (r, R, o de la palette) par celles du skin.
uniform vec3 src0 = vec3(0.478, 0.122, 0.239);
uniform vec3 src1 = vec3(0.769, 0.220, 0.310);
uniform vec3 src2 = vec3(1.0, 0.478, 0.349);
uniform vec3 dst0 = vec3(0.478, 0.122, 0.239);
uniform vec3 dst1 = vec3(0.769, 0.220, 0.310);
uniform vec3 dst2 = vec3(1.0, 0.478, 0.349);
uniform float flash : hint_range(0.0, 1.0) = 0.0;
void fragment() {
	vec4 col = texture(TEXTURE, UV);
	vec3 c = col.rgb;
	if (distance(c, src0) < 0.03) c = dst0;
	else if (distance(c, src1) < 0.03) c = dst1;
	else if (distance(c, src2) < 0.03) c = dst2;
	c = mix(c, vec3(1.0), flash);
	COLOR = vec4(c, col.a);
}
