#version 330 core

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;
in vec2 texcoord0;

void main(){
	fragColor = texture(tex0, texcoord0);
}