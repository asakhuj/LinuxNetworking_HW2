#! /usr/bin/python

import libvirt
import time
conn = libvirt.open('qemu:///system')

threshold = raw_input('Please enter the value of threshold in milliseconds')

response = raw_input('Which parameter you want to choose to see the VMs, CPU (press c) or Memory (press m) ')

def getMemoryBased(item):
         return item[1]

def getCPUBased(item):
         return item[2]

#Initializing an array for the VMs
arr_vm = []
for id in conn.listDomainsID():
	dom = conn.lookupByID(id)
	domName = dom.name()
	mem = dom.memoryStats()
	unusedMemory = mem["unused"]
        availableMemory = mem["available"]
        usedMemory =  availableMemory - unusedMemory
	cpuStats1 = dom.getCPUStats(True)
        #print(cpuStats1)
        #In milliseconds
	cpuTime1 = cpuStats1[0]["cpu_time"]/1000000
	 #print(cpuTime1)
        time.sleep(3);
        cpuStats2 = dom.getCPUStats(True)
        cpuTime2 = cpuStats2[0]["cpu_time"]/1000000
        #print(cpuStats2)
	#cpuStats = cpuStats["vcpu_time"]
        cpuPercent =  (cpuTime2- cpuTime1)/3
        #print("CPU percent is ",cpuPercent,"type : ",type(cpuPercent))
       # print("Threshold is ",threshold,"type is",type(threshold))
       # print(int(cpuPercent) > int(threshold))
        if (int(cpuPercent) > int(threshold)) :
            #print('inside if')
            localTime = time.asctime( time.localtime(time.time()) )
            file = open('log.txt','a+')
            file.write("VM : "+str(domName) + " "+str(localTime) +" CPU Usage : in milliseconds "+str(cpuPercent));
            file.write("\n") 
        #print(cpuPercent)
	newArr = []
	newArr.append(domName)
	newArr.append(usedMemory)
        newArr.append(cpuPercent)
	#domInfo = dom.info()
	#newArr.append(domInfo[4])
	#newArr.append(vcpuStats)
	#print(newArr)
	arr_vm.append(newArr)	
#print(arr_vm)
arr_final = []
if response == 'c' :
      arr_final = sorted(arr_vm,key=getCPUBased)
else :
     arr_final = sorted(arr_vm,key=getMemoryBased) 

print("Sorted array ") 
print(arr_final) 
print("***************************")
print("Printing VMs on the basis of criteria given by the user : In ASCENDING order")
for i in range(len(arr_final)):
        print(arr_final[i][0])

