set term pngcairo
set out "diffusion.png"
set xlabel "t"
set ylabel "<(x(0)-x(t))^2>"
unset key

p "diffusion.dat"

