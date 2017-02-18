set terminal postscript eps enhanced color size 8.6cm, 6cm dl 3\
font "Helvetica, 16pt"
set output 'persistence.eps'

unset key
unset bars
set xlabel 'Time ({/Symbol m}s)' enhanced
set ylabel 'Voltage (mV)' offset 2,0
set xrange [-2:7]

FILES = system("ls -1 sample_traces/*.dat")
plot for [data in FILES] data u ($1*1e6):($2*1e3) every 10 w lines lw .2 lc rgb "#11000000" notitle