import OpenGL.GLUT as GLUT
import OpenGL.GL as GL
import OpenGL.GL.shaders as GL_shaders
import OpenGL.GL.EXT.texture_compression_s3tc as GL_s3tc
import PIL.Image as PIL_Image
import numpy as np
import ctypes as c # These seem very cool!

class Window():
    def __init__(self, name, width, height):
        self.width = width
        self.height = height
        self.name = name
        
        # Create window:
        GLUT.glutInit()
        GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA | GLUT.GLUT_DOUBLE | GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(self.width, self.height)
        
    def run(self):
        # Create window:
        self.win = GLUT.glutCreateWindow(self.name)
        
        # Setup stuff for testing this time:
        self.mySetup()
        
        # Create update mechanism:
        GLUT.glutTimerFunc(30, self.update, 30)
        
        # Create redraw mechanism:
        GLUT.glutDisplayFunc(self.draw)
        GLUT.glutMainLoop()
        
    def mySetup(self):
        self.shader = self.loadShader("vertexshader.glsl", "fragmentshader.glsl")
        #Define geometry:
        self.vertex_data = np.array([
            [-1.0,-1.0, 0.0,  -1.0, 0.0, 0.0],
            [ 1.0,-1.0, 0.0,   0.0,-1.0, 0.0],
            [ 1.0, 1.0, 0.0,   1.0, 0.0, 0.0],
            [-1.0, 1.0, 0.0,   0.0, 1.0, 0.0],
            ], dtype=np.float32)
        
        self.index_data = np.array([
            [0, 1, 3],
            [1, 2, 3]
            ], dtype=np.uint32)
          
        GL.glEnable(GL.GL_CULL_FACE) # This isn't enabled by default
        GL.glFrontFace(GL.GL_CCW) # Standard, right hand rule
        GL.glCullFace(GL.GL_BACK)
            
        self.vbo = GL.glGenBuffers(1)
        self.ibo = GL.glGenBuffers(1)
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo) # Select self.vbo
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vertex_data, GL.GL_STATIC_DRAW) # Assign data to selected buffer
        
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ibo) # Select self.ibo
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.index_data, GL.GL_STATIC_DRAW) # Assign data to selected buffer
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0) # Deselect buffers
    
    def render(self):
        try:
            GL_shaders.glUseProgram(self.shader)
            try:
                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
                
                GL.glVertexAttribPointer( # Vertex data
                    0,                  # Attribute 0 in this attribute array
                    3,                  # This attribute uses 3 elements
                    GL.GL_FLOAT,        # These values are of type "GL_FLOAT"
                    False,              # Normalize values? No!
                    self.vertex_data.shape[1]*c.sizeof(c.c_float), # bits per row, 4 bits for floats, 6 elements in one row (doubles are 8)
                    c.c_void_p(0))               # Where in each row does attribute start?
                GL.glEnableVertexAttribArray(0)
                
                GL.glVertexAttribPointer( # Extra vertex data
                    1,
                    3,
                    GL.GL_FLOAT,
                    False,
                    self.vertex_data.shape[1]*c.sizeof(c.c_float),
                    c.c_void_p(3*4))
                GL.glEnableVertexAttribArray(1)
                
                GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ibo)
                GL.glDrawElements(
                    GL.GL_TRIANGLES,
                    self.index_data.size,
                    GL.GL_UNSIGNED_INT, c.c_void_p(0))
            finally:
                GL.glDisableVertexAttribArray(0)
                GL.glDisableVertexAttribArray(1)
                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        finally:
            GL_shaders.glUseProgram(0)
            
    def update(self, t):
        # Schedule next update:
        GLUT.glutTimerFunc(t, self.update, t)
        # Run "GLUT.glutDisplayFunc(self.draw)":
        GLUT.glutPostRedisplay()
        
    def draw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT) # Clear window
        # Draw commands go here:
        self.render()
        
        GLUT.glutSwapBuffers() # Apply update to window
        
    def loadShader(self, vs, fs):
        # Load vertex shader file and compile:
        with open(vs, 'r') as vs_file:
            VERTEX_SHADER = GL_shaders.compileShader(
                vs_file.read(),
                GL.GL_VERTEX_SHADER)
        del vs_file # Delete file object, good programming practice
        # Load fragment shader file and compile:
        with open(fs, 'r') as fs_file:
            FRAGMENT_SHADER = GL_shaders.compileShader(
                fs_file.read(),
                GL.GL_FRAGMENT_SHADER)
        del fs_file # Delete file object, good programming practice
        # Compile and return shader program:
        return GL_shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)
    
if __name__ == "__main__":
    w = Window("OpenGL", 640, 480)
    w.run()