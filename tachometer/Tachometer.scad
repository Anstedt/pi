include <roundedcube.scad>
// Box length, height, width
o_L = 55.5;
o_H = 26;
o_W = 24;

// PICO length, width, height
i_L = 55.5;
i_H = 24;
i_W = 22;

// Display Dimension
d_L = 25;
d_H = 3;
d_W = 9;

// Display Offsets
do_L = 14.5;
do_H = 0;
do_W = (o_W/2) - (d_W/2);

// How far apart the mount holes
m_D = 11;

// Sensor Height, measured from table top to middle of sensor
s_H = 17;

w_W = 1; // Wall width

// Bottom mounts
m_L = 38; // Length
m_H = 5;  // Clears OLED
m_W = 2;  // Width

// Upper side mounts
u_L = 5; // Length
u_H = 2; // Clear PICO
u_W = 2; // Width

// Subtract from first item
difference()
{
// External cube
roundedcube([o_L, o_W, o_H]);
// Inner Cube to hollow out outer cube
translate([w_W, w_W, w_W])
    cube([i_L, i_W, i_H]);
// x=move along lenght
// y=move across height
// z=move across width
// The +1 is off inner floor
// Sesnsor hole
translate([0, (i_W/2)+1, s_H+w_W])
    rotate(a=[0,90,0])
        cylinder(d=5, h=4);
// X controls distance from front
// Y controls distance appart
// Z left alone to put hole in bottom
// Distance appart is 6 based on measurement
// Small mount holes
translate([o_L-3, ((i_W/2)+w_W) - (m_D/2), 0])
    cylinder(d=2, h=5);
translate([o_L-3, ((i_W/2)+w_W) + (m_D/2), 0])
    cylinder(d=2, h=5);
// OLED display opening
translate([do_L, do_W, do_H])
    cube([d_L, d_W, d_H]); 
}
// Side mounts
translate([w_W, w_W, w_W])
    cube([m_L, m_W, m_H]);
    
translate([w_W, i_W-w_W, w_W])
    cube([m_L, m_W, m_H]);

// Upper side mounts
translate([w_W, w_W, m_H + 2.2])
    cube([u_L, u_W, u_H]);

translate([w_W, i_W-w_W, m_H + 2.2])
    cube([u_L, u_W, u_H]);
    
    
 // Hole mountes
difference()
{
translate([o_L-3, ((i_W/2)+w_W) - (m_D/2), 1])
    cylinder(d=4, h=m_H);
translate([o_L-3, ((i_W/2)+w_W) - (m_D/2), 0])
    cylinder(d=2, h=m_H+1);
}

difference()
{
translate([o_L-3, ((i_W/2)+w_W) + (m_D/2), 1])
    cylinder(d=4, h=m_H);
translate([o_L-3, ((i_W/2)+w_W) + (m_D/2), 0])
    cylinder(d=2, h=m_H+1);
}
