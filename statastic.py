import json
import time
import datetime
import psutil
import requests

class Statastic:
    def __init__(self):
        print "System statastic started"

    def get_memory_details(self):
        memory_details ={            
            'virtual_memory':{          
            },
            'swap_memory':{         
            }               
        }
        
        ### System Virtual Memory details ###
        vm = psutil.virtual_memory()
        memory_details['virtual_memory']['total'] = vm.total
        memory_details['virtual_memory']['available'] = vm.available
        memory_details['virtual_memory']['used'] = vm.used
        memory_details['virtual_memory']['free'] = vm.free
        
        memory_details['virtual_memory']['used_percentage'] = vm.percent
        memory_details['virtual_memory']['remaining_percentage'] = (100-vm.percent)

        ### System Swap Memory details ###
        sm = psutil.swap_memory()
        memory_details['swap_memory']['total'] = sm.total
        memory_details['swap_memory']['used'] = sm.used
        memory_details['swap_memory']['free'] = sm.free
        memory_details['swap_memory']['used_percentage'] = sm.percent

        try:
            memory_details['swap_memory']['remaining_percentage'] = (100-sm.percent)
        except:
            memory_details['swap_memory']['remaining_percentage'] = 0       


        # return json.dumps(memory_details,sort_keys=False,indent=4)
        return memory_details

    def get_network_details(self):
        network_details ={
            'network_info':{            
            }               
        }
        
        ### Network details ###
        netstat = psutil.net_io_counters()
        network_details['network_info']['byte_sent'] = netstat.bytes_sent
        network_details['network_info']['byte_received'] = netstat.bytes_recv
        network_details['network_info']['packets_sent'] = netstat.packets_sent
        network_details['network_info']['packets_received'] = netstat.packets_recv
        network_details['network_info']['no_of_sent_error'] = netstat.errin
        network_details['network_info']['no_of_received_error'] = netstat.errout
        network_details['network_info']['sent_packets_droped'] = netstat.dropin
        network_details['network_info']['received_pakets_droped'] = netstat.dropout

        # return json.dumps(network_details,sort_keys=False,indent=4)       
        return network_details

    def get_cpu_details(self):
        cpu_details ={
            'cpu_info':{            
            }               
        }
        
        ### CPU details ###
        cpustat = psutil.cpu_stats()
        cpu_details['cpu_info']['ctx_switches'] = cpustat.ctx_switches
        cpu_details['cpu_info']['interrupts'] = cpustat.interrupts
        cpu_details['cpu_info']['soft_interrupts'] = cpustat.soft_interrupts
        cpu_details['cpu_info']['syscalls'] = cpustat.syscalls

        return cpu_details        

    def get_log(self):

        details = {
            'timestamp': str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')),
            'memory':{},
            'network':{},
            'cpu':{}
        }
        details['memory'] = self.get_memory_details()
        details['network'] = self.get_network_details()
        details['cpu'] = self.get_cpu_details()

        return details


if __name__ == "__main__":

    stat = Statastic()   

    url = "https://lrsapis.herokuapp.com/lrs/api/v1.0/gateway/status"

    while True:
        log = stat.get_log()
        resp = requests.post(url,data=json.dumps(log,indent=4),headers={'Content-Type':'application/json'})  
        time.sleep(10)