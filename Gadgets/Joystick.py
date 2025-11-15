import PCF8591 as ADC
import time
import math

def setup():
    ADC.setup(0x48)
    
list2 = ['*', 'A', '*']

def Print_R(index):
    if index < 2:
        list2[index] = '*'
        list2[index + 1] = 'A'
        index = index + 1
    
    print(list2)
    return index
        
def Print_L(index):
    if index > 0:
        list2[index] = '*'
        list2[index - 1] = 'A'
        index = index - 1
    
    print(list2)
    return index
            

def loop():
    index = 1
    while True:
        x = ADC.read(1)
        
        if x > 240:
            index = Print_R(index)
            while ADC.read(1) > 240:
                time.sleep(0.1)
        if x < 15:
            index = Print_L(index)
            while ADC.read(1) < 15:
                time.sleep(0.1)
            
        time.sleep(0.01)

if __name__ == '__main__':
    try:
        setup()
        loop()
    
    except KeyError:
        pass
        
        
        