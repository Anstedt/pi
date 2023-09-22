HEIGHT = 13;
HOLE = 5;
TOP_R = 3;
BOT_R = 4;
BASE_H = 2;
BASE_D = 12;

$fn=45; // Smoothness but larger numbers render slower

difference()
{
    union()
    {
        cylinder(h=HEIGHT, r1=BOT_R, r2=TOP_R);
        cylinder(h=BASE_H, d=BASE_D);
    }
    cylinder(h=HEIGHT, d=HOLE);
}

