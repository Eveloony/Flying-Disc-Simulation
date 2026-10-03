Web VPython 3.2

frisbee = cylinder(pos=vector(1, 1.3, 0), axis=vector(0,0.032,0), radius=0.135, color=color.cyan, make_trail=False, retain=400)
spin_marker = sphere(
    radius=0.015,
    color=color.red
)

scene.append_to_caption("\n")

#COLOR-------------------------------

def change_color(evt):
    if evt.selected == "White":
        frisbee.color = color.white
    elif evt.selected == "Cyan":
        frisbee.color = color.cyan
    elif evt.selected == "Blue":
        frisbee.color = color.blue
    elif evt.selected == "Green":
        frisbee.color = color.green
    elif evt.selected == "Yellow":
        frisbee.color = color.yellow
    elif evt.selected == "Orange":
        frisbee.color = color.orange
    elif evt.selected == "Red":
        frisbee.color = color.red
    elif evt.selected == "Pink":
        frisbee.color = vector(1, 0.7, 0.8) 
    elif evt.selected == "Purple":
        frisbee.color = color.purple
    frisbee.trail_color = frisbee.color
    
    frisbee_velocity_curve.color = frisbee.color
    height_vs_time_curve.color = frisbee.color
    distance_vs_time_curve.color = frisbee.color
    acceleration_vs_time_curve.color = frisbee.color
    lift_force_vs_time_curve.color = frisbee.color
    drag_force_vs_time_curve.color = frisbee.color

wtext(text="Color ")
color_menu = menu(choices=["Cyan","White","Blue", "Green", "Yellow", "Orange", "Red", "Pink", "Purple"], bind=change_color)

scene.append_to_caption("\n\n")

#ANGLE OF ATTACK--------------------------------------------------------

wtext(text="Angle of attack ")
angle_text = wtext(text="0")

angle_of_attack = 0

def angle_change(s):
    global angle_of_attack 
    global theta
    global omega
    global spin_angle
    
    angle_text.text = str(int(s.value))
    
    angle_of_attack = (int(s.value)/180)*pi
    
    bank_angle = 25 * (pi / 180)
    base_axis = vector(0, 0.032, 0)
    frisbee.axis = base_axis.rotate(angle=angle_of_attack, axis=vector(0,0,1)).rotate(angle=bank_angle, axis=vector(1,0,0))
    
    theta = vector(angle_of_attack,0,0)
    
    u = norm(frisbee.axis)
    v = cross(u, vector(0,0,1))
    if mag(v) < 0.001:
        v = vector(1,0,0)
    v = norm(v)
    
    w = norm(cross(u,v))
    
    spin_marker.pos = frisbee.pos + frisbee.radius*(
        cos(spin_angle)*v +
        sin(spin_angle)*w
    )

angle_slider = slider(min=0, max=90, value=0, bind=angle_change)

scene.append_to_caption("\n\n")

#FORCE-----------------------------------------------------------------

wtext(text="Force ")
force_text = wtext(text="0 N")

force_exerted = 0

def force_change(s):
    global force_exerted
    force_text.text = str(int(s.value)) + " N"
    force_exerted = int(s.value)

force_ext_slider = slider(min=0, max=20, value=0, bind=force_change)

scene.append_to_caption("\n\n")

#TORQUE------------------------------------------------------------------

wtext(text="Torque ")

spin_text = wtext(text="0 N·m")

def spin_change(s):
    global applied_torque
    applied_torque = int(s.value)
    spin_text.text = str(round(s.value,2)) + " N·m"

torque_slider = slider(
    min=0,
    max=1,
    value=0,
    bind=spin_change
)

scene.append_to_caption("\n\n")

#HEIGHT-----------------------------------------------------------------

wtext(text="Height ")
height_text = wtext(text="1.3 m")

def height_change(s):
    height_text.text = str(s.value) + " m"
    frisbee.pos.y = s.value
    arm1.axis.y = s.value - 1.25
    
    u = norm(frisbee.axis)
    v = cross(u, vector(0,0,1))
    if mag(v) < 0.001:
        v = vector(1,0,0)
    v = norm(v)
    
    w = norm(cross(u,v))
    
    spin_marker.pos = frisbee.pos + frisbee.radius*(
        cos(spin_angle)*v +
        sin(spin_angle)*w
    )


height_slider = slider(min=0, max=2, value=1.3, bind=height_change)

scene.append_to_caption("\n\n")

#DENSITY-------------------------------------------------------------------

wtext(text="Density ")

frisbee_density = 1000
air_density = 1.2

def density_change(evt):
    global frisbee_density
    
    if(evt.selected == "Plastic"):
        frisbee_density = 1000
    elif(evt.selected == "Steel"):
        frisbee_density = 7850
    elif(evt.selected == "Tin"):
        frisbee_density = 2700

density_menu = menu(choices=["Plastic","Steel","Tin"], bind=density_change)

scene.append_to_caption("\n\n")

#THROW-------------------------------------------------------------------------

frisbee.velocity = vector(0,0,0)
is_thrown = False

def toggle(b):
    global is_thrown, omega, frisbee

    current_mass = frisbee_density * (0.175e-3)
    u = norm(frisbee.axis)

    throw_accel = force_exerted * vector(cos(angle_of_attack), sin(angle_of_attack), 0) / current_mass
    frisbee.velocity = throw_accel * 0.25

    alpha_spin = applied_torque / Iy
    initial_spin = max(5.0, alpha_spin * 0.25)
    omega = u * initial_spin

    frisbee.acceleration = vector(0,0,0)
    is_thrown = True

    b.disabled = True
    b.text = 'Thrown!'

    angle_slider.disabled = True
    density_menu.disabled = True
    height_slider.disabled = True
    force_ext_slider.disabled = True
    torque_slider.disabled = True

    frisbee.make_trail = True

throw_button = button(text='Throw!', bind=toggle)

#RESET--------------------------------------------------------------------------
def reset(b):
    global is_thrown, angle_text, height_text, force_text
    global theta, omega, spin_angle, applied_torque
    global angle_of_attack, frisbee_density, dragging
    global lift_force, drag_force, gravity, alpha
    global precession_rate, precession_angle
    global mass, Ix, Iy, Iz
    global force_exerted, bank_angle
    global curr_time
    global wind_theta1, wind_theta2, wind_mag, following

    angle_of_attack = 0
    frisbee_density = 1000
    force_exerted = 0
    dragging = False
    precession_rate = 0
    precession_angle = 0
    bank_angle = 0.262
    
    frisbee.color = color.cyan
    color_menu.selected = 'Cyan'

    mass = frisbee_density * (0.175e-3)
    Ix = 0.25 * mass * (0.135**2)
    Iy = 0.50 * mass * (0.135**2)
    Iz = Ix

    theta = vector(0,0,0)
    omega = vector(0,0,0)
    alpha = vector(0,0,0)
    spin_angle = 0
    applied_torque = 0

    lift_force = vector(0,0,0)
    drag_force = vector(0,0,0)
    gravity = vector(0,0,0)

    is_thrown = False
    frisbee.velocity = vector(0,0,0)
    frisbee.acceleration = vector(0,0,0)
    frisbee.pos = vector(1,1.3,0)
    frisbee.axis = vector(0,0.032,0)
    frisbee.clear_trail()

    spin_marker.pos = frisbee.pos + frisbee.radius*vector(1,0,0)

    wind_arrow.axis = vector(1.5,0,0)
    wind_tip.pos = wind_arrow.pos + wind_arrow.axis

    crosswind_slider_lr.value = 0
    crosswind_slider_ud.value = 0
    crosswind_slider_mag.value = 3
    crosswind_text_lr.text = "0 degrees"
    crosswind_text_ud.text = "0 degrees"
    crosswind_text_mag.text = "3 m/s"
    wind_theta1 = 0
    wind_theta2 = 0
    wind_mag = 3

    throw_button.disabled = False
    throw_button.text = "Throw!"

    angle_slider.disabled = False
    angle_slider.value = 0
    angle_text.text = "0"

    density_menu.disabled = False

    height_slider.disabled = False
    height_slider.value = 1.3
    height_text.text = "1.3 m"

    force_ext_slider.disabled = False
    force_ext_slider.value = 0
    force_text.text = "0 N"

    torque_slider.disabled = False
    torque_slider.value = 0
    spin_text.text = "0 N·m"
    
    frisbee.make_trail = False
    
    curr_time = 0
    
    frisbee_velocity_curve.delete()
    height_vs_time_curve.delete()
    distance_vs_time_curve.delete()
    acceleration_vs_time_curve.delete()
#    angular_position_vs_time_curve.delete()
#    angular_vel_vs_time_curve.delete()
    lift_force_vs_time_curve.delete()
    drag_force_vs_time_curve.delete()
    
    scene.camera.pos = vector(-5, 2, 0)
    scene.camera.axis = vector(1, -0.2, 0)
    
    following = False
    scene.camera.follow(None)
    following_frisbee_button.text = 'Follow Frisbee'
    
    arm1.pos = vector(0.55,1.25,0)
    arm1.axis = vector(0.35,0.05,0)

    

reset_button = button(text='Reset!', bind=reset)

#BACKGROUND---------------------------------------------------------------------

autoscale = False
scene.camera.pos = vector(-5, 2, 0)
scene.camera.axis = vector(1, -0.2, 0)
bg = sphere(pos=vec(0,0,0), 
    radius=50,   
    texture= 'https://i.imgur.com/gHTRddo.jpeg')
    
floor = box(pos=vector(0, 0, 0), size = vector(100, 0.1, 100), texture='https://i.imgur.com/HosF5Up.jpeg')


#preset views ----------------------------------------------------

def side_view(b):
    scene.camera.follow(None)
    scene.camera.pos = vector(3, 1, 8)
    scene.camera.axis = vector(0, 0, -1)

def thrower_view(b):
    scene.camera.follow(None)
    scene.camera.pos = vector(-2, 2, 0)
    scene.camera.axis = vector(1, -0.2, 0)

def birds_eye(b):
    scene.camera.follow(None)
    scene.camera.pos = vector(3, 7, 0)
    scene.camera.axis = vector(0, -1, 0)

following = False

def follow_frisbee(b):
    global following
    following = not following
    
    if(following):
        scene.camera.follow(frisbee)
        following_frisbee_button.text = 'Unfollow Frisbee'
    else:
        scene.camera.follow(None)
        following_frisbee_button.text = 'Follow Frisbee'

scene.append_to_caption("\n\n")
button(text='Side View', bind=side_view)
button(text="Thrower's View", bind=thrower_view)
button(text="Bird's Eye", bind=birds_eye)
following_frisbee_button = button(text="Follow Frisbee", bind=follow_frisbee)
scene.append_to_caption("\n\n")


#stuff for wind arrows -----------------------------

wtext(text="Wind Magnitude ")

wind_arrow = arrow(
    pos=vector(0,2,0),
    axis=vector(1.5,0,0),
    color=color.yellow,
    shaftwidth=0.05
)

wind_tip = sphere(
    pos=wind_arrow.pos + wind_arrow.axis,
    radius=0.05,
    color=color.red
)

dragging = False

def down():
    global dragging
    if scene.mouse.pick == wind_tip:
        dragging = True

def up():
    global dragging
    dragging = False

scene.bind("mousedown", down)
scene.bind("mouseup", up)

wind_theta1 = 0
wind_theta2 = 0
wind_mag = 3

wtext(text="Wind (L/R) ")
crosswind_text_lr = wtext(text="0 degrees")

def crosswind_change_lr(s):
    global wind_theta1, wind_theta2, wind_mag
    wind_theta1 = (s.value / 180) * pi 
    crosswind_text_lr.text = str(round(s.value,1)) + " degrees"

    v = vector(1,0,0)
    v = v.rotate(angle=wind_theta2, axis=vector(0,0,1))
    v = v.rotate(angle=wind_theta1, axis=vector(0,-1,0))

    wind_arrow.axis = wind_mag * v/2
    wind_tip.pos = wind_arrow.pos + wind_arrow.axis

crosswind_slider_lr = slider(min=-180, max=180, value=0, bind=crosswind_change_lr)

wtext(text="\nWind (Up/Down) ")
crosswind_text_ud = wtext(text="0 degrees")

def crosswind_change_ud(s):
    global wind_theta1, wind_theta2, wind_mag
    wind_theta2 = (s.value / 180) * pi 
    crosswind_text_ud.text = str(round(s.value,1)) + " degrees"

    v = vector(1,0,0)
    v = v.rotate(angle=wind_theta2, axis=vector(0,0,1))
    v = v.rotate(angle=wind_theta1, axis=vector(0,-1,0))

    wind_arrow.axis = wind_mag * v /2
    wind_tip.pos = wind_arrow.pos + wind_arrow.axis

crosswind_slider_ud = slider(min=-180, max=180, value=0, bind=crosswind_change_ud)


wtext(text="\nWind Strength ")
crosswind_text_mag = wtext(text="3 m/s")

def crosswind_change_mag(s):
    global wind_theta1, wind_theta2, wind_mag
    wind_mag = s.value
    crosswind_text_mag.text = str(round(s.value,1)) + " m/s"

    v = vector(1,0,0)
    v = v.rotate(angle=wind_theta2, axis=vector(0,0,1))
    v = v.rotate(angle=wind_theta1, axis=vector(0,-1,0))

    wind_arrow.axis = wind_mag * v / 2
    wind_tip.pos = wind_arrow.pos + wind_arrow.axis

crosswind_slider_mag = slider(min=0, max=18, value=3, bind=crosswind_change_mag)


#stuff for ms. sharaf ------------------------------------------

head = sphere(
    pos=vector(0.55,1.5,0),
    radius=0.08,
    color=color.yellow
)

left_eye = sphere(
    pos = head.pos + vector(0.06, 0.02, 0.03), 
    radius = 0.015, 
    color = color.blue
)

right_eye = sphere(
    pos = head.pos + vector(0.06, 0.02, -0.03), 
    radius = 0.015, 
    color = color.blue
)

mouth = cylinder(
    pos = head.pos + vector(0.07, -0.02, -0.03), 
    axis = vector(0.005, 0.01, 0.06), 
    radius = 0.006, 
    color = color.black
)

glass_color = color.black
frame_thickness = 0.003
lens_radius = 0.022

left_lens = ring(
    pos = head.pos + vector(0.077, 0.02, 0.03),
    axis = vector(1, 0, 0),
    radius = lens_radius,
    thickness = frame_thickness,
    color = glass_color
)

right_lens = ring(
    pos = head.pos + vector(0.077, 0.02, -0.03),
    axis = vector(1, 0, 0), 
    radius = lens_radius,
    thickness = frame_thickness,
    color = glass_color
)

bridge = cylinder(
    pos = head.pos + vector(0.079, 0.02, -0.012),
    axis = vector(0, 0, 0.024),
    radius = frame_thickness,
    color = glass_color
)

hair_color = color.yellow
hair_thickness = 0.002
hair_length = 0.04

hair_left = cylinder(
    pos = head.pos + vector(0, 0.075, 0.02),
    axis = vector(0, hair_length, 0.02),
    radius = hair_thickness,
    color = hair_color
)

hair_center = cylinder(
    pos = head.pos + vector(0, 0.08, 0),
    axis = vector(0, hair_length, 0),
    radius = hair_thickness,
    color = hair_color
)

hair_right = cylinder(
    pos = head.pos + vector(0, 0.075, -0.02),
    axis = vector(0, hair_length, -0.02),
    radius = hair_thickness,
    color = hair_color
)

body = cylinder(
    pos=vector(0.55,1.38,0),
    axis=vector(0,-1.05,0),
    radius=0.05,
    color=color.blue
)

arm1 = cylinder(
    pos=vector(0.55,1.25,0),
    axis=vector(0.35,0.05,0),
    radius=0.02,
    color=color.orange
)

arm2 = cylinder(
    pos=vector(0.55,1.25,0),
    axis=vector(-0.2,-0.05,0),
    radius=0.02,
    color=color.orange
)

leg1 = cylinder(
    pos=vector(0.55,0.33,0),
    axis=vector(0.08,-0.35,0),
    radius=0.025,
    color=color.orange
)

leg2 = cylinder(
    pos=vector(0.55,0.33,0),
    axis=vector(-0.08,-0.35,0),
    radius=0.025,
    color=color.orange
)

frisbee.velocity = vector(0,0,0)
frisbee.acceleration = vector(0, 0, 0)

applied_torque = 0

mass = frisbee_density*(0.175e-3)
Ix = 0.25*mass*(0.135**2)
Iy = 0.50*mass*(0.135**2)
Iz = Ix

theta = vector(angle_of_attack,0,0)
omega = vector(0,0,0)
spin_angle=0
#torque = vector(0,0,applied_torque)
#alpha = vector(0,0,torque.z/Iz)

#angular_momentum = (Iy * mag(omega)) * norm(frisbee.axis)

dt = 1/60


#print(angle_of_attack)

lift_force = vector(0,0,0)
drag_force = vector(0,0,0)
gravity = vector(0,0,0)
bank_angle=0.262

u = norm(frisbee.axis)
v = cross(u, vector(0,0,1))
if mag(v) < 0.001:
    v = vector(1,0,0)
v = norm(v)

w = norm(cross(u,v))

spin_marker.pos = frisbee.pos + frisbee.radius*v

precession_rate = 0
precession_angle = 0
curr_time = 0

#scene.camera.follow(frisbee)

height_vs_time_graph = graph(width=400, height=300, align='left', title='Height vs Time', xtitle='time (s)', ytitle='Height (m)', xmin=0, ymin=0)
height_vs_time_curve = gcurve(color=frisbee.color)

distance_vs_time_graph = graph(width=400, height=300, align='left', title='Distance vs Time', xtitle='time (s)', ytitle='Distance (m)', xmin=0, ymin=0)
distance_vs_time_curve = gcurve(color=frisbee.color)

frisbee_velocity_graph = graph(width=400, height=300, align='left', title='Velocity over Time', xtitle='time (s)', ytitle='Frisbee Velocity (m/s)', xmin=0, ymin=0)
frisbee_velocity_curve = gcurve(color=frisbee.color)

acceleration_vs_time_graph = graph(width=400, height=300, align='left', title='Acceleration vs Time', xtitle='time (s)', ytitle='Acceleration (m/s^2)', xmin=0, ymin=0)
acceleration_vs_time_curve = gcurve(color=frisbee.color)

#angular_position_vs_time_graph = graph(title='Angular Position vs Time', xtitle='time (s)', ytitle='Angular Position (rad)', xmin=0, ymin=0)
#angular_position_vs_time_curve = gcurve(color=frisbee.color)
#
#angular_vel_vs_time_graph = graph(title='Angular Velocity vs Time', xtitle='time (s)', ytitle='Angular Velocity (rad/s)', xmin=0, ymin=0)
#angular_vel_vs_time_curve = gcurve(color=frisbee.color)
#
#angular_momentum_vs_time_graph = graph(title='Angular Momentum vs Time', xtitle='time (s)', ytitle='Angular Momentum (kg • m^2/s)', xmin=0, ymin=0)
#angular_momentum_vs_time_curve = gcurve(color=frisbee.color)

lift_force_vs_time_graph = graph(width=400, height=300, align='left', title='Lift Force vs Time', xtitle='time (s)', ytitle='Lift Force (N)', xmin=0, ymin=-2)
lift_force_vs_time_curve = gcurve(color=frisbee.color)

drag_force_vs_time_graph = graph(width=400, height=300, align='left', title='Drag Force vs Time', xtitle='time (s)', ytitle='Drag Force (N)', xmin=0, ymin=0)
drag_force_vs_time_curve = gcurve(color=frisbee.color)

while True:
    rate(60)
    
    if (dragging and (not is_thrown)):
        current_z = wind_tip.pos.z 
        wind_tip.pos = scene.mouse.pos
        wind_tip.pos.z = current_z  
        
        wind_arrow.axis = wind_tip.pos - wind_arrow.pos
        wind_text.text = str(round(mag(wind_arrow.axis),1)) + " N"

    if(is_thrown and frisbee.pos.y > 0):
        curr_time += dt
        
        # ----------------------------- GRAPHS ---------------------------------------
        
        height_vs_time_curve.plot(curr_time, frisbee.pos.y)
        distance_vs_time_curve.plot(curr_time, frisbee.pos.x-1)
        frisbee_velocity_curve.plot(curr_time, frisbee.velocity.mag)
        acceleration_vs_time_curve.plot(curr_time, frisbee.acceleration.mag)
#        angular_position_vs_time_curve.plot(curr_time, theta.mag)
#        angular_vel_vs_time_curve.plot(curr_time, omega.mag)
        
        # ------------------- RELATIVE VELOCITY & WIND -------------------
        wind_velocity = wind_arrow.axis
        relative_velocity = frisbee.velocity - wind_velocity
        
        u = norm(frisbee.axis)
        if mag(u) < 0.5: 
            u = vector(0,1,0)
            
        v_dir = vector(1, 0, 0)
        if mag(relative_velocity) > 0.001:
            v_dir = norm(relative_velocity)
            
        dot_val = dot(v_dir, u)
        dot_val = max(-1.0, min(1.0, dot_val))
        dynamic_aoa = -asin(dot_val)

        # ---------------------------------- LIFT AND DRAG -------------------------------------
        c_lift = min(1.5, 0.188 + 2.37 * dynamic_aoa)
        c_drag = 0.15 + 1.24 * (dynamic_aoa**2)
    
        m_lift_force = 0.5 * c_lift * (0.135**2) * pi * air_density * (relative_velocity.mag)**2
        lift_force = u * m_lift_force
        
        m_drag_force = 0.5 * c_drag * (0.135**2) * pi * air_density * (relative_velocity.mag)**2
        drag_force = -1 * v_dir * m_drag_force
        
        lift_force_vs_time_curve.plot(curr_time, m_lift_force)
        drag_force_vs_time_curve.plot(curr_time, m_drag_force)
        
        current_mass = frisbee_density * (0.175 * 10**(-3))
        gravity = (current_mass * 9.81) * vector(0, -1, 0)
        
        v = cross(u, vector(0,0,1))
        if mag(v) < 0.001:
            v = vector(1,0,0)
        v = norm(v)
        w = norm(cross(u,v))
        
        
        #----------------------------- CENTER OF PRESSURE ----------------------------------------
        cop_vector = v_dir - dot_val*u
        
        if mag(cop_vector) > 0.001:
            center_of_pressure = 0.25 * frisbee.radius * norm(cop_vector)
        else:
            center_of_pressure = vector(0,0,0)

        lift_torque = cross(center_of_pressure, lift_force)
        drag_torque = cross(center_of_pressure, drag_force)
        
        throw_force = vector(0,0,0)
        throw_torque = vector(0,0,0)
        
  
        frisbee.acceleration = (lift_force + drag_force + gravity + throw_force) / current_mass
        frisbee.velocity = frisbee.velocity + frisbee.acceleration * dt
        frisbee.pos = frisbee.pos + frisbee.velocity * dt
        
        spin_marker.pos = frisbee.pos + frisbee.radius*(cos(spin_angle)*v + sin(spin_angle)*w)
        
        net_torque = lift_torque + drag_torque + throw_torque
        
        # ------------------- MOMENTUM & SPIN -------------------
        current_spin_speed = mag(omega)
        
#        if current_spin_speed < 0.1: 
#            current_spin_speed = 30 

        L = Iy * current_spin_speed * u
        L += net_torque * dt
        
#        angular_momentum_vs_time_curve.plot(curr_time, L.mag)
        
        if mag(L) > 0.0001:
            new_spin_axis = norm(L)
        else:
            new_spin_axis = u

        frisbee.axis = new_spin_axis * 0.032
        omega = new_spin_axis * current_spin_speed
        theta += omega * dt
        
        spin_rate = mag(omega)
        spin_angle += spin_rate * dt

    elif(is_thrown):
        frisbee.velocity = vector(0,0,0)
        frisbee.acceleration = vector(0,0,0)
    
        if frisbee.pos.y < 0:
            frisbee.pos.y = 0
