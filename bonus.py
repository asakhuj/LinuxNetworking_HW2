#! /usr/bin/python

import libvirt
import time
conn = libvirt.open('qemu:///system')
print('------------------Bonus Question--------------')
print('Resource we are using is Memory usage')
pollingInterval = raw_input('Please enter the polling interval , in seconds')
movingWindowSize = raw_input('Please enter the moving window  size in number')

def getMemoryBased(item):
         return item[1]

#Initializing an array for the VMs
arr_vm = []
for id in conn.listDomainsID():
        dom = conn.lookupByID(id)
        domName = dom.name()
        arr_Domain = []
        for counter in range(0,int(movingWindowSize)):
	    mem = dom.memoryStats()
	    unusedMemory = mem["unused"]
            availableMemory = mem["available"]
            usedMemory =  availableMemory - unusedMemory
            arr_Domain.append(usedMemory)
            time.sleep(int(pollingInterval));
       #Calculate average now
        average = sum(arr_Domain)/len(arr_Domain)
	newArr = []
	newArr.append(domName)
	newArr.append(average)
	arr_vm.append(newArr)	
#print(arr_vm)
arr_final = []
arr_final = sorted(arr_vm,key=getMemoryBased) 

print("Sorted array ") 
print(arr_final) 
print("***************************")
print("Printing VMs on the basis of memory usage , In ASCENDING order : Memory usage is increasing :")
for i in range(len(arr_final)):
        print(arr_final[i][0])

