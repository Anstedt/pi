include <roundedcube.scad>

// Subtract from first item
difference()
{
translate([-5,-5,0])
    roundedcube([40,22,25]);
    // cube([40,22,25]);
translate([-5,-4,1])
    // PICO length, height, width
    cube([40,20,23]);
cylinder(d=3, h=5);
}
