#version 330 core

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
uniform mat4 p3d_ModelViewProjectionMatrix;

out vec2 texcoord0;

void main(){
	texcoord0 = p3d_MultiTexCoord0;
	gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}