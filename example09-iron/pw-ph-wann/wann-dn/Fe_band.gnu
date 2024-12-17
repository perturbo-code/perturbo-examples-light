set style data dots
set nokey
set xrange [0:15.00387]
set yrange [  3.43504 : 45.30501]
set arrow from  2.18927,   3.43504 to  2.18927,  45.30501 nohead
set arrow from  4.08523,   3.43504 to  4.08523,  45.30501 nohead
set arrow from  5.17987,   3.43504 to  5.17987,  45.30501 nohead
set arrow from  6.72791,   3.43504 to  6.72791,  45.30501 nohead
set arrow from  8.91718,   3.43504 to  8.91718,  45.30501 nohead
set arrow from 10.46523,   3.43504 to 10.46523,  45.30501 nohead
set arrow from 12.01327,   3.43504 to 12.01327,  45.30501 nohead
set arrow from 13.90924,   3.43504 to 13.90924,  45.30501 nohead
set xtics ("G"  0.00000,"H"  2.18927,"P"  4.08523,"N"  5.17987,"G"  6.72791,"H"  8.91718,"N" 10.46523,"G" 12.01327,"P" 13.90924,"N" 15.00387)
 plot "Fe_band.dat"
