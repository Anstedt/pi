include <roundedcube.scad>
// Box length, height, width
o_L = 54.5;
o_H = 24;
o_W = 24;

// PICO length, width, height
i_L = 54.5;
i_H = 22;
i_W = 22;

// Display Dimension
d_L = 25;
d_H = 3;
d_W = 11;

// Display Offsets
do_L = 14.5;
do_H = 0;
do_W = (o_W/2) - (d_W/2);

// How far apart the mount holes
m_D = 11;

// Sensor Height, measured from table top to middle of sensor
s_H = 18;

w_W = 1; // Wall width

// Subtract from first item
difference()
{
// translate([0, 0, 0])
// External cube
roundedcube([o_L, o_W, o_H]);
// cube([o_L, o_H, o_W]);
translate([w_W, w_W, w_W])
    cube([i_L, i_W, i_H]);
// x=move along lenght
// y=move across height
// z=move across width
// The +1 is off inner floor 
translate([0, (i_W/2)+1, s_H+w_W])
    rotate(a=[0,90,0])
        cylinder(d=5, h=4);
// X controls distance from front
// Y controls distance appart
// Z left alone to put hole in bottom
// Distance appart is 6 based on measurement
translate([o_L-2, (i_W/2)-(m_D/2) - w_W, 0])
    cylinder(d=2, h=5);
translate([o_L-2, (i_W/2)+(m_D/2), 0])
    cylinder(d=2, h=5);
translate([do_L, do_W, do_H])
    cube([d_L, d_W, d_H]); 
}


// translate([47,6,20])
//    rotate(a=[0,90,0])
//        cylinder(d=4, h=4);

