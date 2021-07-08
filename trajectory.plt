set term pngcairo
set out "trajectory.png"
set xlabel "x"
set ylabel "y"
set zlabel "z"
unset key

splot "trajectory.dat" w l

