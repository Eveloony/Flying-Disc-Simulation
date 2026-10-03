Cynthia Wen and Evelyn Liu
Period 4/5

We plan to code a physics simulation that demonstrates the aerodynamics of a frisbee flying in the air. The user will be able to customize the density of the frisbee, the initial torque applied to it, height at which it’s thrown, angle of attack, direction of the wind, and the color/design of the frisbee. The simulation will be 3d such that the user can adjust their view angle, with some preset viewing perspectives (side and front view) available

Based on user inputs, we can calculate an initial translational and rotational velocity for the frisbee. We will then calculate lift and drag forces using the formulas L=0.5*C_L*A*rho*V^2 and D=0.5*C_D*A*rho*V^2. We will use these forces to create changes in the frisbees rotational and translational movement over time, and display its flight path in 3d.