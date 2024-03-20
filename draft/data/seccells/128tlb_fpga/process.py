#!/usr/bin/env python3
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

text_size = 16

def get_dataset_size(nentries, entrysize = 64):
  netsize = nentries * entrysize
  if netsize < 1024:
    return str(netsize)
  elif netsize < 1024 * 1024:
    return str(int(netsize / 1024)) + 'KB'
  elif netsize < (1024 * 1024 * 1024):
    return str(int(netsize / (1024 * 1024))) + 'MB'
  else:
    return str(int(netsize / (1024 * 1024 * 1024))) + 'GB'

def main():
  with open('data') as datafd:
    table = [line for line in csv.reader(datafd, delimiter=',')]
    
  labels = table[0]
  table = table[1:]
  
  nentries = [int(x[0]) for x in table]
  
  configs = ['base', 'cheri', 'sc']
  CHERI_inst = 191
  CHERI_cycle = 254
  cpr = {} # Cyles per request
  cpi = {} # Cyles per instruction
  for config in configs:
    if config == 'cheri':
      insts_col = [i for i in range(len(labels)) if labels[i] == 'base' + '_minstret'][0]
      cycle_col = [i for i in range(len(labels)) if labels[i] == 'base' + '_mcycle'][0]
    else:    
      insts_col = [i for i in range(len(labels)) if labels[i] == config + '_minstret'][0]
      cycle_col = [i for i in range(len(labels)) if labels[i] == config + '_mcycle'][0]
      
    insts = [int(row[insts_col]) for row in table]
    cycle = [int(row[cycle_col]) for row in table]
    
    instsperreq = [instcount/reqcount for (reqcount, instcount) in zip(nentries,insts)]
    cycleperreq = [cyclecount/reqcount for (reqcount,cyclecount) in zip(nentries,cycle)]
    if config == 'cheri':
      instsperreq = [x + (2 * CHERI_inst) for x in instsperreq]
      cycleperreq = [x + (2 * CHERI_cycle) for x in cycleperreq]
      
    cycleperinst = [cyc/inst for (cyc,inst) in zip(cycleperreq,instsperreq)]
    
    cpr[config] = cycleperreq
    cpi[config] = cycleperinst
    
    insts = [int(row[insts_col]) for row in table]
    cycle = [int(row[cycle_col]) for row in table]
  
    
  xlabels = [get_dataset_size(x) for x in nentries]
  
  fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
  markers = 'xvs'
  colors = [plt.cm.tab10(i) for i in range(len(configs))]
  # ax1 = plt.subplot(2,1,1)
  for config, mark, color in zip(configs, markers, colors):
    ax1.plot(xlabels, cpr[config], marker = mark, color = color)
  ax1.set_ylabel('Cycles\nper request', fontsize = text_size)
  ax1.tick_params(labelsize = text_size * 0.9)
  ax1.set_ylim(bottom=0)
    
  # ax2 = plt.subplot(2,1,2, sharex = ax1)
  for config, mark, color in list(zip(configs, markers, colors))[::-1]:
    ax2.plot(xlabels, cpi[config], marker = mark, color = color)
  ax2.set_ylabel('Cycles\nper instruction', fontsize = text_size)
  ax2.tick_params(labelsize = text_size * 0.9)
  ax2.set_ylim(bottom=1)
    
  ax2.set_xticklabels(xlabels, rotation = 80)
  ax2.set_xlabel('Dataset size', fontsize = text_size)
  
  labels = ['Baseline', 'CHERI', 'SecureCells']
  ax1.legend(labels, bbox_to_anchor=(0, 1, 1, 0), loc="lower left", mode="expand", ncol=3, fontsize = text_size * 0.9)  
  fig.savefig('mycached_small.pdf', bbox_inches='tight')
  # plt.show()

if __name__ == '__main__':
  main()