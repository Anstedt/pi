include <roundedcube.scad>
// Box length, height, width
o_L = 55.5;
o_H = 26;
o_W = 24;

// PICO length, width, height
i_L = 55.5;
i_H = 24;
i_W = 22;

// Posts
p_O = 16; // Posts outer edge

// USB connector
usb_O = 6.5; // USB offset from bottom
usb_H = 4;   // USB connector height
usb_W = 10;  // Horizontal opening

difference()
{
roundedcube([2, o_W, o_H]);

translate([0, o_W/2 - usb_W/2, usb_O])
    roundedcube([2, usb_W, usb_H], false, 0.9, "x");
}

difference()
{
// Inner ridge surface, subtract -0.2 for tolerance fit
translate([2, 1+0.1, 1+0.1])
    roundedcube([5, i_W-0.14, i_H-0.14], false, 0.5, "xmax");
// Remove center of inner ridge
translate([2, 3, 3])
    cube([5, i_W-4, i_H-4]);
// Remove sides for board room
translate([2, 1, 4])
    cube([5, i_W, 8]);
// Remove room for posts
translate([2, 4, 1])
    cube([5, p_O, 8]);
}

