# <codecell> paths and info
import os, sys
homeDir = os.environ['HOMEPATH']
jmodDir = os.environ['JMODELICA_HOME']
workDir = "Desktop" # has to be adapted by the user !!!
moLiDir = os.path.join(homeDir, workDir, "BuildingSystems")

# give the path to directory where package.mo is stored
moLibs = [os.path.join(jmodDir, "ThirdParty\MSL\Modelica"),
          os.path.join(moLiDir,"BuildingSystems"),
         ]

print(sys.version)
print(all(os.path.isfile(os.path.join(moLib, "package.mo")) for moLib in moLibs))
print(os.getcwd())

# <codecell> compile model to fmu
from pymodelica import compile_fmu
model_name = 'BuildingSystems.Applications.SolarThermalSystems.SolarThermalSystem1'
my_fmu = compile_fmu(model_name, moLibs)

# <codecell> simulate the fmu and store results
from pyfmi import load_fmu

myModel = load_fmu(my_fmu)

opts = myModel.simulate_options()
opts['solver'] = "CVode"
opts['ncp'] = 240
opts['result_handling']="file"
opts["CVode_options"]['discr'] = 'BDF'
opts['CVode_options']['iter'] = 'Newton'
opts['CVode_options']['maxord'] = 5
opts['CVode_options']['atol'] = 1e-5
opts['CVode_options']['rtol'] = 1e-5

res = myModel.simulate(start_time=0.0, final_time=864000, options=opts)

# <codecell> plotting of the results
import pylab as P
fig = P.figure(1)
P.clf()
# collector
# radiation
y1 = res['collector.radiationPort.IrrDir']
y2 = res['collector.radiationPort.IrrDir']
t = res['time']
P.subplot(4,1,1)
P.plot(t, y1, t, y2)
P.legend(['collector.radiationPort.IrrDir','collector.radiationPort.IrrDir'])
P.ylabel('Power (W/m2)')
P.xlabel('Time (s)')
# collector and storage temperatures
y1 = res['collector.vol[10].T']
y2 = res['storage.T[1]']
y3 = res['storage.T[10]']
t = res['time']
P.subplot(4,1,2)
P.plot(t, y1, t, y2, t, y3)
P.legend(['collector.vol[10].T','storage.T[1]','storage.T[10]'])
P.ylabel('Temperature (K)')
P.xlabel('Time (s)')
# control signal pump
y1 = res['control.y']
t = res['time']
P.subplot(4,1,3)
P.plot(t, y1)
P.legend(['control.y'])
P.ylabel('signal (1)')
P.xlabel('Time (s)')
# back up heater
y1 = res['hea.Q_flow']
t = res['time']
P.subplot(4,1,4)
P.plot(t, y1)
P.legend(['hea.Q_flow'])
P.ylabel('Power (W)')
P.xlabel('Time (s)')
P.show()
