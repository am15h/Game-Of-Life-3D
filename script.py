import bpy
from array import *
import colorsys
from math import sqrt, pi, sin, ceil
from random import TWOPI

# Number of cubes.
count = 10

# Size of grid.
extents = 8.0

# Spacing between cubes.
padding = 0.05

# Size of each cube.
sz = (extents / count) - padding

# To convert abstract grid position within loop to real-world coordinate.
iprc = 0.0
jprc = 0.0
kprc = 0.0
countf = 1.0 / (count - 1)
diff = extents * 2

# Position of each cube.
z = 0.0
y = 0.0
x = 0.0

# Center of grid.
centerz = 0.0
centery = 0.0
centerx = 0.0

# For animation, track current frame, specify desired number of key frames.
currframe = 0
fcount = 10
invfcount = 1.0 / (fcount - 1)

# If the default frame range is 0, then default to 1 .. 150.
frange = bpy.context.scene.frame_end - bpy.context.scene.frame_start
if frange == 0:
    bpy.context.scene.frame_end = 150
    bpy.context.scene.frame_start = 0
    frange = 150

# Number of keyframes per frame.
fincr = ceil(frange * invfcount)



T = [[0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,1,0,0,0,0,0], 
     [0,0,0,1,1,1,0,0,0,0], 
     [0,0,0,0,1,0,0,0,0,0], 
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,1,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0]]

C = [[0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,1,0,0,0,0,0], 
     [0,0,0,1,1,1,0,0,0,0], 
     [0,0,0,0,1,0,0,0,0,0], 
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,1,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0]]
     
# Loop through grid z axis.
print('new')
for i in range(0, 14, 1):
    
    for x in range(0, count, 1):
        for y in range(0, count, 1):        
            T[x][y] = C[x][y]
    
    # Convert from index to percent in range 0 .. 1,
    # then convert from prc to real world coordinate.
    # Equivalent to map(val, lb0, ub0, lb1, ub1).
    iprc = i * countf
    z = -extents + iprc * diff
    print('at', i ,'T ' ,T)
    print('at', i ,'C ' ,C)
    # Loop through grid y axis.
    for j in range(0, count, 1):
        jprc = j * countf
        y = -extents + jprc * diff

        # Loop through grid x axis.
        for k in range(0, count):
            kprc = k * countf
            x = -extents + kprc * diff
            
            neisum = 0
            
            if k-1>=0 and j-1>=0 and k+1<count and j+1<count :
                neisum = T[j-1][k-1] + T[j-1][k] + T[j-1][k+1] + T[j][k-1] + T[j][k+1] + T[j+1][k-1] + T[j+1][k] + T[j+1][k+1] 
                print(T[j-1][k] , T[j][k-1] ,T[j][k+1] ,T[j+1][k])
            elif j==0 and k==0:   
                neisum = T[j+1][k] + T[j][k+1] + T[j+1][k+1]
            elif j==count-1 and k==count-1:    
                neisum = T[j-1][k] + T[j][k-1] + T[j-1][k-1]
            elif j==0 and k==count-1:    
                neisum = T[j+1][k] + T[j][k-1] + T[j+1][k-1]
            elif j==count-1 and k==0:    
                neisum = T[j-1][k] + T[j][k+1] + T[j-1][k+1]    
            elif j==0 and k-1>=0 and k+1<count:
                neisum = T[j][k-1] + T[j][k+1] + T[j+1][k-1] + T[j+1][k] + T[j+1][k+1]    
            elif j==count-1 and k-1>=0 and k+1<count:
                neisum = T[j][k-1] + T[j][k+1] + T[j-1][k-1] + T[j-1][k] + T[j-1][k+1]    
            elif k==0 and j-1>=0 and j+1<count:
                neisum = T[j-1][k] + T[j-1][k+1] + T[j][k+1] +  T[j+1][k] + T[j+1][k+1]
            elif k==count-1 and j-1>=0 and j+1<count:
                neisum = T[j-1][k-1] + T[j-1][k] + T[j][k-1] + T[j+1][k-1] + T[j+1][k] 
                 
            print('(',j,',',k,')',neisum)            
            if T[j][k]==1 : 
                
                if neisum<2 or neisum>3:
                    C[j][k] = 0
                            
                # Add grid world position to cube local position.
                bpy.ops.mesh.primitive_cube_add(location=(centerx + x, centery + y, centerz + z), radius=sz)

                # Cache the current object being worked on.
                current = bpy.context.object

                # Equivalent to Java's String.format. Placeholders
                # between curly braces will be replaced by value of k, j, i.
                current.name = 'Cube ({0}, {1}, {2})'.format(k, j, i)
                current.data.name = 'Mesh ({0}, {1}, {2})'.format(k, j, i)

                # Create a material.
                mat = bpy.data.materials.new(name='Material ({0}, {1}, {2})'.format(k, j, i))

                # Assign a diffuse color to the material.
                mat.diffuse_color = (kprc, jprc, iprc)
                current.data.materials.append(mat)
                
                # Track the current key frame.
                currframe = bpy.context.scene.frame_start
                for f in range(0, fcount, 1):
                        
                    # Set the scene to the current frame.
                    bpy.context.scene.frame_set(currframe)
                    
                    current.keyframe_insert(data_path='scale', index=2)
                    
                    # Advance by the keyframe increment to the next keyframe.
                    currframe += fincr        
                                        
            else:
               if neisum==3:
                    C[j][k] = 1 
            
   


# Add a sun lamp above the grid.
bpy.ops.object.lamp_add(type='SUN', radius=1.0, location=(0.0, 0.0, extents * 0.667))

# Add an isometric camera above the grid.
# Rotate 45 degrees on the x-axis, 180 - 45 (135) degrees on the z-axis.
bpy.ops.object.camera_add(location=(extents * 1.414, extents * 1.414, extents * 2.121), rotation=(0.785398, 0.0, 2.35619))
bpy.context.object.data.type = 'ORTHO'
bpy.context.object.data.ortho_scale = extents * 7.0