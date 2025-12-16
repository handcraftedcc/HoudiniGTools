import hou
def createGtoolAttribs(geo): #Depreceated - handled in HDA instead
    geo.addAttrib(hou.attribType.Point, "Gtype", "", transform_as_normal=False, create_local_variable=False) #Indicates Gcode type (G0, G1, Custom etc)
    geo.addAttrib(hou.attribType.Point, "CustomGcode", "", transform_as_normal=False, create_local_variable=False)  #For custom code sections
    geo.addArrayAttrib(type, "XYZset", hou.attribData.Int, tuple_size=3) #Indicates which elements should be written to the gcode file, since all points will have XYZ coordinates
    geo.addArrayAttrib(type, "F", hou.attribData.Int, tuple_size=3) #Feedrate for G1,G2,G3 etc commands - should be ignored if 0 or negative
    geo.addAttrib(hou.attribType.Point, "IJK", hou.vector((0,0,0)), transform_as_normal=False, create_local_variable=False) #Arc parameters
    geo.addAttrib(hou.attribType.Point, "E", 0, transform_as_normal=False, create_local_variable=False) #Output pin number with M67
    geo.addAttrib(hou.attribType.Point, "L", 0, transform_as_normal=False, create_local_variable=False) #Parameter for G10
    geo.addAttrib(hou.attribType.Point, "P", 0.0, transform_as_normal=False, create_local_variable=False) #Dwell time with G4 & Used to indicate coordinate system with G10
    geo.addAttrib(hou.attribType.Point, "T", 0, transform_as_normal=False, create_local_variable=False) #Used to indicate analog level with M67
    geo.addAttrib(hou.attribType.Point, "Q", 0, transform_as_normal=False, create_local_variable=False) #This is used with the M6 command. It is used to change the current tool number. With FluidNC it can also be used to change the spindle if multiple spindles are used.

#--- Helper functions
def is_bit_set(mask, n):
    return (mask & (1 << n)) != 0

def addMessage(point,gcode,message,mode):
    gcode += f"(MSG {message}) "
    if mode=="geo":
        point.setAttribValue("G_Message", message)
    return gcode,point
        

def addComment(point,gcode,comment,mode):
    gcode += f"; {comment} "
    if mode=="geo":
        point.setAttribValue("G_Comment", comment)
    return gcode,point

#--- Gcode builders
def buildTypeCustom(geo,pos,customGcode,message,comment,mode):
    gcode = customGcode
    if mode=="geo":
        point = geo.createPoint()
        point.setPosition(pos)
        point.setAttribValue("G_CustomGcode", gcode)
        point.setAttribValue("G_Gtype", "Custom")

    gcode,point = addComment(point,gcode,comment,mode)
    gcode,point = addMessage(point,gcode,message,mode)

    return geo,gcode,pos
    
def buildTypeG0(geo,pos,XYZ,toggleXYZ,distancemode,message,comment,mode): #Rapid move

    toggleX = is_bit_set(toggleXYZ,0)
    toggleY = is_bit_set(toggleXYZ,1)
    toggleZ = is_bit_set(toggleXYZ,2)

    startpos = pos.copy()

    if distancemode!="G90":
        gcode = distancemode + "\n"
    else:
        gcode = ""
    gcode += "G0 "
   
    if toggleX:
        if distancemode=="G90":
            pos[0] = XYZ[0]
        else:
            pos[0] += XYZ[0]
        gcode+=f"X {XYZ[0]}"
    if toggleY:
        if distancemode=="G90":
            pos[1] = XYZ[1]
        else:
            pos[1] += XYZ[1]
        gcode+=f"Y {XYZ[1]}"
    if toggleZ:
        if distancemode=="G90":
            pos[2] = XYZ[2]
        else:
            pos[2] += XYZ[2]
        gcode+=f"Z {XYZ[2]}"

    if mode=="geo":
        if distancemode!="G90":
            distancemodepoint = geo.createPoint()
            distancemodepoint.setPosition(startpos)
            distancemodepoint.setAttribValue("G_Gtype", distancemode)
        point = geo.createPoint()
        point.setPosition(pos)
        point.setAttribValue("G_Gtype", "G0")
        if distancemode!="G90":
            distancemodepointout = geo.createPoint()
            distancemodepointout.setPosition(pos)
            distancemodepointout.setAttribValue("G_Gtype", "G90") #Reset to G90

    gcode,point = addComment(point,gcode,comment,mode)
    gcode,point = addMessage(point,gcode,message,mode)

    return geo,gcode,pos

def buildTypeG1(geo,pos,XYZ,toggleXYZ,F,toggleF,distancemode,message,comment,mode): #Move at Feedrate
    toggleX = is_bit_set(toggleXYZ,0)
    toggleY = is_bit_set(toggleXYZ,1)
    toggleZ = is_bit_set(toggleXYZ,2)

    startpos = pos.copy()

    if distancemode!="G90":
        gcode = distancemode + "\n"
    else:
        gcode = ""
    gcode += "G1 "
   
    if toggleX:
        if distancemode=="G90":
            pos[0] = XYZ[0]
        else:
            pos[0] += XYZ[0]
        gcode+=f"X {XYZ[0]}"
    if toggleY:
        if distancemode=="G90":
            pos[1] = XYZ[1]
        else:
            pos[1] += XYZ[1]
        gcode+=f"Y {XYZ[1]}"
    if toggleZ:
        if distancemode=="G90":
            pos[2] = XYZ[2]
        else:
            pos[2] += XYZ[2]
        gcode+=f"Z {XYZ[2]}"
    if toggleF:
        gcode+=f"F {F}"

    if distancemode!="G90":
        gcode = "\n G90" #Reset to G90

    if mode=="geo":
        if distancemode!="G90":
            distancemodepoint = geo.createPoint()
            distancemodepoint.setPosition(startpos)
            distancemodepoint.setAttribValue("G_Gtype", distancemode)
        point = geo.createPoint()
        point.setPosition(pos)
        point.setAttribValue("G_Gtype", "G1")
        if toggleF:
            point.setAttribValue("G_F", F)
        if distancemode!="G90":
            distancemodepointout = geo.createPoint()
            distancemodepointout.setPosition(pos)
            distancemodepointout.setAttribValue("G_Gtype", "G90") #Reset to G90

    gcode,point = addComment(point,gcode,comment,mode)
    gcode,point = addMessage(point,gcode,message,mode)

    return geo,gcode,pos

def buildTypeG2G3(geo,pos,XYZ,toggleXYZ,IJK,toggleK,F,toggleF,message,comment,mode): #Arc move #NOT IMPLEMENTED JUST PLACEHOLDER CODE
    toggleX = is_bit_set(toggleXYZ,0)
    toggleY = is_bit_set(toggleXYZ,1)
    toggleZ = is_bit_set(toggleXYZ,2)

    gcode = "G0 "
   
    if toggleX:
        pos[0] = XYZ[0]
        gcode+=f"X {XYZ[0]}"
    if toggleY:
        pos[1] = XYZ[1]
        gcode+=f"Y {XYZ[1]}"
    if toggleZ:
        pos[2] = XYZ[2]
        gcode+=f"Z {XYZ[2]}"

    if toggleF:
        point.setAttribValue("G_F", F)

    if mode=="geo":
        point = geo.createPoint()
        point.setPosition(pos)
        point.setAttribValue("G_Gtype", "G0")

    return geo,gcode,pos

def buildTypeG4(geo,pos,P,message,comment,mode): #Dwell
    gcode = "G4 "
    gcode+=f"P {P}"

    if mode=="geo":
        point = geo.createPoint()
        point.setPosition(pos)
        point.setAttribValue("G_Gtype", "G4")
        point.setAttribValue("G_P", P)

    gcode,point = addComment(point,gcode,comment,mode)
    gcode,point = addMessage(point,gcode,message,mode)

    return geo,gcode,pos

def buildTypeG38(geo,pos,P,toggleP,G38mode,message,comment,mode): #Probe
    gcode=f"{G38mode} "
    if toggleP:
        gcode+=f"P {P}"

    if mode=="geo":
        point = geo.createPoint()
        point.setPosition(pos)
        point.setAttribValue("G_Gtype", G38mode)
        if toggleP:
            point.setAttribValue("G_P", P)

    gcode,point = addComment(point,gcode,comment,mode)
    gcode,point = addMessage(point,gcode,message,mode)
    
    return geo,gcode,pos

def buildTypeG53G59(geo,pos,coordsystem,message,comment,mode): #Select Coordinate System
    gcode = coordsystem

    if mode=="geo":
        point = geo.createPoint()
        point.setPosition(pos)
        point.setAttribValue("G_Gtype", coordsystem)

    gcode,point = addComment(point,gcode,comment,mode)
    gcode,point = addMessage(point,gcode,message,mode)

    return geo,gcode,pos

def buildTypeM0(geo,pos,message,comment,mode): #Pause
    gcode = "M0"

    if mode=="geo":
        point = geo.createPoint()
        point.setPosition(pos)
        point.setAttribValue("G_Gtype", "M0")

    gcode,point = addComment(point,gcode,comment,mode)
    gcode,point = addMessage(point,gcode,message,mode)

    return geo,gcode,pos

def buildTypeM3M5(geo,pos,command,message,comment,mode): #Pause
    gcode = command

    if mode=="geo":
        point = geo.createPoint()
        point.setPosition(pos)
        point.setAttribValue("G_Gtype", command)

    gcode,point = addComment(point,gcode,comment,mode)
    gcode,point = addMessage(point,gcode,message,mode)

    return geo,gcode,pos