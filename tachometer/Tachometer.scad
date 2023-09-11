include <roundedcube.scad>
// Box length, width, height
o_L = 54.5;
o_W = 24;
o_H = 22;

// PICO length, width, height
i_L = 52.5;
i_W = 22;
i_H = 20;

// Subtract from first item
difference()
{
translate([-5,-5,0])
    // roundedcube([40,22,25]);
    // External cube
    roundedcube([o_L, o_H, o_W]);
    // cube([o_L, o_H, o_W]);
translate([-5,-4,1])
    cube([i_L, i_H, i_W]);
// x=move along lenght
// y=move across height
// z=move across width
// Close but needs better measurements
translate([47,6,20])
    rotate(a=[0,90,0])
        cylinder(d=4, h=4);
// X controls distance from front
// Y controls distance appart
// Z left alone to put hole in bottom
// Distance appart is 6 based on measurement
translate([-3,3,0])
    cylinder(d=2, h=5);
translate([-3,9,0])
    cylinder(d=2, h=5);
}

// translate([47,6,20])
//    rotate(a=[0,90,0])
//        cylinder(d=4, h=4);

