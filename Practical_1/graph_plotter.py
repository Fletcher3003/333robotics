import matplotlib.pyplot
import numpy

Data = numpy.loadtxt("LogFile.txt")
print(Data)

matplotlib.pyplot.plot(Data[:,0],Data[:,1], 'r')
matplotlib.pyplot.plot(Data[:,0],Data[:,2], 'b')
#matplotlib.pyplot.axis([0,4,0,16])
matplotlib.pyplot.show()
