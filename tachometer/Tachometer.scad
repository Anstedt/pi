include <roundedcube.scad>
// Box length, width, height
o_L = 54.5;
o_W = 24;
o_H = 22;

// PICO length, width, height
i_L = 54.5;
i_W = 22;
i_H = 20;

// How far apart the mount holes
m_D = 11;

// Sensor Height, measured from table top to middle of sensor
s_H = 16;

w_W = 1; // Wall width

// Subtract from first item
difference()
{
// translate([0, 0, 0])
// External cube
roundedcube([o_L, o_H, o_W]);
// cube([o_L, o_H, o_W]);
translate([w_W, w_W, w_W])
    cube([i_L, i_H, i_W]);
// x=move along lenght
// y=move across height
// z=move across width
// The +1 is off inner floor 
translate([0, i_W/2, s_H+w_W])
    rotate(a=[0,90,0])
        cylinder(d=4, h=4);
// X controls distance from front
// Y controls distance appart
// Z left alone to put hole in bottom
// Distance appart is 6 based on measurement
translate([3, (i_W/2)-(m_D/2), 0])
    cylinder(d=2, h=5);
translate([3, (i_W/2)+(m_D/2), 0])
    cylinder(d=2, h=5);
}


// translate([47,6,20])
//    rotate(a=[0,90,0])
//        cylinder(d=4, h=4);

