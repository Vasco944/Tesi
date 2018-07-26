import sys
sys.path.append("/marconi/home/userexternal/aantonie/workspace/nest-simulator/b/lib64/python2.7/site-packages")
import nest
import time
import numpy as np

def tic():
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    if 'startTime_for_tictoc' in globals():
        tempo = float(time.time()) - float(startTime_for_tictoc)
        print ("Elapsed time is %.3f seconds" % tempo)
    else:
        print "Toc: start time not set"

def Write_Weights(PFPC_conn,MFDCN_conn,PCDCN_conn,W_file1,W_file2,W_file3):
    weights1 = nest.GetStatus(PFPC_conn, "weight")
    weights2 = nest.GetStatus(MFDCN_conn, "weight")
    weights3 = nest.GetStatus(PCDCN_conn, "weight")
    #v1 = nest.GetStatus(PFPC_conn,'modulator')
    #V_file1 = open("VT.dat","w")
    #for w in v1:
        #V_file1.write(str(w)+" ")
    #V_file1.write("\n")
    for w in weights1:
        W_file1.write(str(w)+" ")
    W_file1.write("\n")
    for w in weights2:
        W_file2.write(str(w)+" ")
    W_file2.write("\n")
    for w in weights3:
        W_file3.write(str(w)+" ")
    W_file3.write("\n")
    
def Compute_Output(spikedetectorDCN, DCN, Output_variables):
    tau_time_constant = 0.060 # 60 ms
    kernel_amplitude = np.sqrt(2.0/tau_time_constant)
    
    dSD = nest.GetStatus(spikedetectorDCN,keys='events')[0]
    evs = dSD["senders"]
    
    # Update the output variables with an exponential decay
    Output_variables[0]*=np.exp(-0.001/tau_time_constant)
    Output_variables[1]*=np.exp(-0.001/tau_time_constant)
    
    for spikes in evs:
        if spikes < np.mean(DCN):
            Output_variables[0]+=kernel_amplitude # Positive Output
        else:
            Output_variables[1]+=kernel_amplitude # Negative Output
    
    nest.SetStatus(spikedetectorDCN, [{"n_events": 0}])
        
    return Output_variables, spikedetectorDCN

def Generate_Input_Activity(MF, MF_number, Signal,t):
    n_signal = len(Signal)
    Spikes = [np.nan]*MF_number
    i = 0
    for signal_i in Signal:
        In_min=-0.01
        In_max=1.01
        Signal_norm = (signal_i-In_min)/(In_max-In_min) # [0-1]
        MF_centers = np.linspace(In_min+(In_max-In_min)/((MF_number-n_signal)/(n_signal)),
                                 In_max-(In_max-In_min)/((MF_number-n_signal)/n_signal),
                                 (MF_number/n_signal))
        for MFi in MF_centers:
            Distancei = np.abs(Signal_norm-MFi)
            if Distancei < 0.02*np.random.rand():
                Spikes[i] = float(t)
            elif np.random.rand()<0.01:
                Spikes[i] = float(t)
            i+=1
    return Spikes          


# colorful text (yay!)
color_dictionary = {}
color_dictionary['white']  = '\033[97m'
color_dictionary['blue']   = '\033[94m'
color_dictionary['green']  = '\033[92m'
color_dictionary['red']    = '\033[91m'
color_dictionary['yellow'] = '\033[93m'
color_dictionary['cyan']   = '\033[96m'
color_dictionary['purple'] = '\033[95m'


# progressbar display
def progressbar(progress, pbnum=40):
    global color_dictionary
    import sys
    loadbar = ""
    for i in range(pbnum):
        if i<=int(progress*float(pbnum)):
            loadbar = loadbar + "="
        else:
            loadbar = loadbar + " "
    #~ sys.stdout.write("\r"+"["+loadbar+"] "+str(int(progress*100.0))+"%")
    if progress < 0.33:
        sys.stdout.write("\r"+"["+color_dictionary['red'   ]+loadbar+'\033[0m'+"]"+" "+str(int(progress*100.0))+"%")
    elif progress < 0.66:
        sys.stdout.write("\r"+"["+color_dictionary['yellow']+loadbar+'\033[0m'+"]"+" "+str(int(progress*100.0))+"%")
    else:
        sys.stdout.write("\r"+"["+color_dictionary['green' ]+loadbar+'\033[0m'+"]"+" "+str(int(progress*100.0))+"%")
    if progress>=1.0:
        print(" "+'\033[0m'+"OK "+'\033[0m')
    sys.stdout.flush()
