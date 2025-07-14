
import turtle
import time                                     #library for time 

sIO_FILE = "C:\emu8086\emu8086.io"

#length of robotic arms 
arm1_l = 80
arm2_l = 80
arm3_l = 60
arm4_l = 40
gr_size = 10        #how long is the grip

#define the onclick object
item = [False,0,0]

# Each tuple in list arms describes the color, the length and the angle range of the arm
arm1 = ["grey", arm1_l, -60,60]
arm2 = ["blue", arm2_l, -45, 45]
arm3 = ["red", arm3_l,  -125, 125, arm4_l]
grip = ["blue", 30, -60, 60]

#starting robotic arm position
new_angle1 = cur_angle1 = 0
new_angle2 = cur_angle2 = -45
new_angle3 = cur_angle3 = 90
new_length4 = cur_length4 = int(arm3_l + (arm4_l/2))
new_grip_angle = cur_grip_angle = 30
new_grip_status = cur_grip_status = 1
terminate = False


t1 = turtle.Turtle()
t2 = turtle.Turtle()
    
#
def show_parameter_names():
    x0=-70
    y0=-115
    step = 15
    t1.clear()
    t1.ht()
    t1.color('blue')
    
    t1.penup()
    t1.goto(x0, y0)
    t1.pendown()
    t1.write("Angle 1:    ", font=("Courier", 10, "bold") )
    
    t1.penup()
    t1.goto(x0, y0-step)
    t1.pendown()
    t1.write("Angle 2:    " , font=("Courier", 10, "bold"))
    
    t1.penup()
    t1.goto(x0, y0-2*step)
    t1.pendown()
    t1.write("Angle 3:    " , font=("Courier", 10, "bold"))
    
    t1.penup()
    t1.goto(x0, y0-3*step)
    t1.pendown()
    t1.write("Length 4:   " , font=("Courier", 10, "bold"))
    
    t1.penup()
    t1.goto(x0, y0-4*step)
    t1.pendown()
    t1.write("Grip angle: " , font=("Courier", 10, "bold"))
    
    t1.penup()
    t1.goto(x0, y0-5*step)
    t1.pendown()
    t1.write("Grip status:" , font=("Courier", 10, "bold"))
   
def show_parameter_values():
    
    x0=30
    y0=-115
    step = 15

    t2.clear()
    t2.ht()
    t2.color('blue')
    t2.penup()
    t2.goto(x0, y0)
    t2.pendown()
    t2.write( '%4s' %(cur_angle1), font=("Courier", 10, "bold"))
    
    t2.penup()
    t2.goto(x0, y0-step)
    t2.pendown()
    t2.write( '%4s' %(cur_angle2), font=("Courier", 10, "bold"))
    
    t2.penup()
    t2.goto(x0, y0-2*step)
    t2.pendown()
    t2.write('%4s' %(cur_angle3), font=("Courier", 10, "bold"))
    
    t2.penup()
    t2.goto(x0, y0-3*step)
    t2.pendown() 
    t2.write('%4s' %(cur_length4), font=("Courier", 10, "bold"))
    
    t2.penup()
    t2.goto(x0, y0-4*step)
    t2.pendown()
    t2.write('%4s' %(cur_grip_angle), font=("Courier", 10, "bold"))
    
    t2.penup()
    t2.goto(x0, y0-5*step)
    t2.pendown() 
    t2.write('%4s' %(cur_grip_status), font=("Courier", 10, "bold"))

def WRITE_IO_BYTE( lPORT_NUM, mybyte):
    f = open(sIO_FILE, "r+b")                
    f.seek(lPORT_NUM)                       
    f.write(mybyte)
    f.close()

def READ_IO_BYTE( lPORT_NUM):
    mybyte = chr(0)
    f = open(sIO_FILE, "rb")
    f.seek(lPORT_NUM)               #goes to the position of where we want to read 
    mybyte = f.read(1)
    f.close() 
    return mybyte

def READ_IO_PARAMETERS( lPORT_NUM):
    f = open(sIO_FILE, "rb")
    f.seek(lPORT_NUM)
    myparams = f.read(7)
    f.close() 
    #print(myparams)
    return myparams


#Print updated posiiton 
def update_position():
    if cur_angle1 < 0: temp = cur_angle1 + 256
    else: temp = cur_angle1
    WRITE_IO_BYTE(11,(temp).to_bytes(1, "little"))
    
    if cur_angle2 < 0: temp = cur_angle2 + 256
    else: temp = cur_angle2
    WRITE_IO_BYTE(12,(temp).to_bytes(1, "little"))
    
    if cur_angle3 < 0: temp = cur_angle3 + 256
    else: temp = cur_angle3
    WRITE_IO_BYTE(13,(temp).to_bytes(1, "little"))
   
    WRITE_IO_BYTE(14,(cur_length4).to_bytes(1, "little"))

    if cur_grip_angle < 0: temp = cur_grip_angle + 256
    else: temp = cur_grip_angle
    WRITE_IO_BYTE(15,(temp).to_bytes(1, "little"))
    
    WRITE_IO_BYTE(16,(cur_grip_status).to_bytes(1, "little"))


# Read desired position. Parameters are truncated if out of robotic arm bounds
def read_new_position():
    global new_angle1, new_angle2, new_angle3, new_length4, new_grip_angle, new_grip_status 

    temp = READ_IO_PARAMETERS(11)
    new_angle1 = (temp[0])
    new_angle2 = (temp[1])
    new_angle3 = (temp[2])
    new_length4 = (temp[3])
    new_grip_angle = (temp[4])
    new_grip_status = (temp[5])

    #print(temp[0], temp[1],temp[2],temp[3],temp[4],temp[5])

    #print(new_angle1, new_angle2, new_angle3, new_length4, new_grip_angle, new_grip_status)

    # convert parameters to signed intergers
    if new_angle1 >128: new_angle1 = new_angle1-256
    if new_angle2 >128: new_angle2 = new_angle2-256
    if new_angle3 >128: new_angle3 = new_angle3-256
    if new_grip_angle >128: new_grip_angle = new_grip_angle-256

    #truncate parameters to arm bounds 
    if (new_angle1 < arm1[2]):  new_angle1 = arm1[2]
    elif(new_angle1 > arm1[3]): new_angle1 = arm1[3]

    if (new_angle2 < arm2[2]):   new_angle2 = arm2[2]
    elif(new_angle2 > arm2[3]):  new_angle2 = arm2[3]

    if (new_angle3 < arm3[2]):   new_angle3 = arm3[2]
    elif(new_angle3 > arm3[3]):  new_angle3 = arm3[3]

    if (new_length4 < arm3[1]):   new_length4 = arm3[1]
    elif(new_length4 > (arm3[1]+arm3[4])):  new_length4 = (arm3[1]+arm3[4])

    if (new_grip_angle < grip[2]):    new_grip_angle = grip[2]
    elif(new_grip_angle > grip[3]):   new_grip_angle = grip[3]

    if (new_grip_status != 0): new_grip_status = 1
    #print(new_angle1, new_angle2, new_angle3, new_length4, new_grip_angle, new_grip_status)

    


#create  an orthogonal staring at x0, y0 
def make_box(color, x0, y0 ,width, height, fill) :
    #Draw the base of the robotic arm (grey orthogonal(100X200))
    t = turtle.Turtle()
    t.hideturtle()
    t.pensize(5)
    t.penup()
    t.goto(x0, y0)
    t.color(color)
    t.pendown()
    t.fillcolor(color)
    if (fill == 1): t.begin_fill()
  
    # drawing first side
    t.forward(width) # Forward turtle by width units
    t.right(90) # Turn turtle by 90 degree
 
    # drawing second side
    t.forward(height) # Forward turtle by height units
    t.right(90) # Turn turtle by 90 degree
 
    # drawing third side
    t.forward(width) # Forward turtle by width units
    t.right(90) # Turn turtle by 90 degree
 
    # drawing fourth side
    t.forward(height) # Forward turtle by height units
    t.right(90) # Turn turtle by 90 degree

    if (fill==1): t.end_fill()


def draw_grip(status,  grip_angle, pen):

    #truncate grip_angle
    if grip_angle < grip[2] : grip_angle = grip[2]
    elif grip_angle > grip[3] : grip_angle = grip[3]

    pen.pensize(4)
    if status==0:  # grip open
        pen.penup()
        pen.color(grip[0])
        pen.rt(grip_angle+90)
        pen.pendown()
        pen.fd(20)
        pen.left(90)
        pen.fd(grip[1])
        pen.back(grip[1])
        pen.lt(90)
        pen.fd(40)
        pen.rt(90)
        pen.fd(grip[1])
    else:        #grip closed
        pen.penup()
        pen.color(grip[0])
        pen.rt(grip_angle+90)
        pen.pendown()
        pen.fd(20)
        pen.left(120)
        pen.fd(grip[1])
        pen.back(grip[1])
        pen.lt(60)
        pen.fd(40)
        pen.rt(120)
        pen.fd(grip[1])


def draw_robotic_arm(ang1, ang2, ang3, a4_l, gr, grip_angle, pen):

    global cur_angle1, cur_angle2, cur_angle3, cur_length4, cur_grip_angle, cur_grip_status
    #draw first arm

    pen.pensize(20)    
    pen.penup()
    pen.goto(0, -90)
    pen.color(arm1[0])
    pen.setheading(90)
    pen.rt(ang1)
    pen.pendown()
    pen.fd(arm1[1])

    #draw second arm
    pen.pensize(16)
    pen.penup()
    pen.color(arm2[0])
    pen.rt(ang2)
    pen.pendown()
    pen.fd(arm2[1])


    #draw third arm
    
    pen.pensize(14)    
    pen.penup()
    pen.color(arm3[0])
    pen.rt(ang3)
    pen.pendown()
    pen.fd(arm3[1])

    pen.pensize(8)    
    pen.penup()
    pen.color("black")
    pen.backward((arm3_l+arm4_l)-a4_l)
    pen.pendown()
    pen.fd(arm4_l)

    draw_grip(gr, grip_angle, pen)

    cur_angle1 = ang1
    cur_angle2 = ang2
    cur_angle3 = ang3
    cur_length4 = a4_l
    cur_grip_angle = grip_angle
    cur_grip_status = gr

def write_item_to_port(x,y):
    x1 = (x).to_bytes(2,'little',signed = True)
    y1 = (y).to_bytes(2,'little',signed = True)
    WRITE_IO_BYTE(30,(x1[0]).to_bytes(1,'little'))
    WRITE_IO_BYTE(31,(x1[1]).to_bytes(1,'little'))
    WRITE_IO_BYTE(32,(y1[0]).to_bytes(1,'little'))
    WRITE_IO_BYTE(33,(y1[1]).to_bytes(1,'little'))


t3 = turtle.Turtle()
t3.hideturtle()

def place_object(x,y):
    global t3,item
    if (item[0] == True):
        t3.clear()

    item[0] = True
    item[1] = int(x)
    item[2] = int(y)
    t3.hideturtle()
    t3.penup()
    t3.goto(x,y)
    t3.rt(180)
    t3.begin_fill()
    t3.circle(4)
    t3.end_fill()
    t3.write(str(int(x)) + ',' + str(int(y)))
    write_item_to_port(item[1], item[2])


def clear_objects(x,y):
    global t3,item
    t3.clear()
    item[0] = False
    item[1] = 0
    item[2] = 0
###MAIN PROGRAMM###

#setup  window for robotic arm
wndw = turtle.Screen()                              #makes a screen from library turtle with name wndw
wndw.bgcolor("light green")                               #background color 
wndw.setup(width=600, height=400)                   #size of window 
wndw.title("Robotic Arm")                           #window name 
wndw.tracer(0)                                      #set the refresh time 


# draw the base of the robotic arm
make_box("dark gray", -80, -95, 160, 100, 1)


make_box("dark blue", -80, -95, 160, 100, 0)

# Create the drawing pen for the robotic arms
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)


#print("ARXIKA:")
#print(cur_angle1, cur_angle2, cur_angle3, cur_length4,  cur_grip_angle, cur_grip_status)

write_item_to_port(0,0)
user_exit = 0
WRITE_IO_BYTE(21,(0).to_bytes(1,"little"))

show_parameter_names()
show_parameter_values()

draw_robotic_arm(cur_angle1,cur_angle2,cur_angle3, cur_length4, cur_grip_status, cur_grip_angle, pen)
update_position()
wndw.update()
time.sleep(3)

show_parameter_names()
show_parameter_values()




while (user_exit == 0):
    read_new_position()
    
    if (cur_angle1 != new_angle1) or (cur_angle2 != new_angle2) or  (cur_angle3 != new_angle3) or (cur_length4 != new_length4) or (cur_grip_status != new_grip_status) or (cur_grip_angle != new_grip_angle):
        pen.clear()
        WRITE_IO_BYTE(20,(1).to_bytes(1, "little"))
        draw_robotic_arm(new_angle1,new_angle2, new_angle3, new_length4,new_grip_status, new_grip_angle, pen)
        update_position()
       
    
    show_parameter_values()
    wndw.update()
    WRITE_IO_BYTE(20,(0).to_bytes(1,"little")) 
    user_exit = int.from_bytes(READ_IO_BYTE(21), "little")

    wndw.onclick(place_object,1)
    wndw.onclick(clear_objects,3)
    
    time.sleep(0.1)
    t2.clear()
    


