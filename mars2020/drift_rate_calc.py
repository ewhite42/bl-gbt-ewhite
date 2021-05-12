#drift_rate_calc.py

import pylab as plt

def main():

    c = 3.0*(10**8)
    f = 8.4*(10**9)
    v1820 = 1000*16.7140194
    v1825 = 1000*16.7120464
    v1830 = 1000*16.7102124
    v1855 = 1000*16.7031539
    
    #first use 18:20 UTC and 18:25 UTC as your points of interest:
    v_avg1 = (v1820+v1825)/2
    dur1 = 300
    v_dot1 = (v1825 - v1820)/dur1
    drift1 = -(c*v_dot1)*(f)/((c+v_avg1)**2)
    
    print("Drift rate between 18:20 and 18:25 UTC: {} Hz/s".format(drift1))
    
    #next use 18:25 UTC and 18:30 UTC as your points of interest:
    v_avg2 = (v1825+v1830)/2
    dur2 = 300
    v_dot2 = (v1830 - v1825)/dur2
    drift2 = -(c*v_dot2)*(f)/((c+v_avg2)**2)
    
    print("Drift rate between 18:25 and 18:30 UTC: {} Hz/s".format(drift2))
    
    #finally, use 18:25 UTC and 18:55 UTC as your points of interest:
    v_avg3 = (v1825+v1855)/2
    dur3 = 30.0*60.0
    v_dot3 = (v1855 - v1825)/dur3
    drift3 = -(c*v_dot3)*(f)/((c+v_avg3)**2)
    
    print("Drift rate between 18:25 and 18:55 UTC: {} Hz/s".format(drift3))
    
    #plot drift rates vs. freq
    fname = 'measured-drifts.txt'
    infile = open(fname, 'r')
    
    drift_rates = []
    freqs = []
    n=0
    
    for line in infile.readlines():
        if n%2 == 0:
            drift_rates.append(float(line))
        else:
            freqs.append(float(line))
        n += 1
        
    plt.plot(freqs, drift_rates, '.', markersize=20, label='Measured drift rates')
    plt.plot(8400, -4.30405, 'o', markersize=20, label='Mars Express')
    #plt.plot(8439.444444,-23.43561, '*', label='MRO')
    plt.plot(8400,-0.16007, 'o', markersize=20, label='Mars Orbiter Mission')
    plt.plot(8402.655,-0.39325, '*', markersize=20, label='Emirates Mars Mission')
    plt.plot(8400,-3.13645, 'o', markersize=20, label='MAVEN')
    plt.plot(8400, 0.13831, 'o', markersize=20, label='Curiosity / Insight')
    plt.legend()
    plt.xlabel("Frequency [MHz]")
    plt.ylabel("Drift Rates [Hz/s]")
    plt.show()
    
if __name__ == "__main__":
    main()
    
