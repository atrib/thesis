#!/usr/bin/env python3
from cProfile import label
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams

insts_heading = 'minstret'
cycle_heading = 'mcycle'
tlb_miss_heading = 'tlbmisses'
text_size = 18

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
  with open('data.csv') as datafd:
    table = [line for line in csv.reader(datafd, delimiter=',')]
  
  configs = table[0]
  iters = table[1]
  fields = table[2]
  table = table[3:]
  nentries = [int(row[0]) for row in table]
  
  col_map = {}
  last_cfg = None
  for cfg,field,iter,col_idx in zip(configs, fields, iters, range(len(fields))):
    if cfg == '':
      cfg = last_cfg
    else:
      last_cfg = cfg
      col_map[cfg] = {}
    if cfg == None:
      continue
    
    col_map[cfg][field] = col_idx
  # print(col_map)
  configs = [cfg for cfg in configs if cfg != '']
  configs.append('CHERI')
  
  CHERI_inst = 191
  CHERI_cycle = 254
  cpr = {} # Cycles per request
  cpi = {} # Cycles per instruction
  for cfg in configs:
    insts = [int(row[col_map['Baseline' if cfg == 'CHERI' else cfg][insts_heading]]) for row in table]  
    cycle = [int(row[col_map['Baseline' if cfg == 'CHERI' else cfg][cycle_heading]]) for row in table]  
    
    if cfg == 'CHERI':
      cycle_per_req  = [(cyc / req) + (2 * CHERI_cycle) for (cyc, req)  in zip(cycle, nentries)]
      insts_per_req  = [(inst / req) + (2 * CHERI_inst) for (inst, req) in zip(insts, nentries)]
      cycle_per_inst = [cpr / ipr for (cpr,ipr) in zip(cycle_per_req, insts_per_req)]
    else:
      cycle_per_inst = [cyc / inst for (cyc, inst) in zip(cycle, insts)]
      cycle_per_req  = [cyc / req  for (cyc, req)  in zip(cycle, nentries)]
    
    cpr[cfg] = cycle_per_req
    cpi[cfg] = cycle_per_inst
    
  ######### Creating figure 
  xlabels = [get_dataset_size(x) for x in nentries]
  
  figsize = rcParams['figure.figsize']
  figsize = (figsize[0], 1.2*figsize[1])
  fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize = figsize)
  markers = 'x*+'
  msizes = [10, 10, 10]
  colors = ['silver', 'royalblue', 'darkorange']
  edgecolors = ['dimgray', 'blue', 'orangered']
  # colors = [plt.cm.tab10(i) for i in range(len(configs))]
  for config, mark, color, edgecolor, msize in zip(configs, markers, colors, edgecolors, msizes):
    ax1.plot(xlabels, cpr[config], marker = mark, color = color, 
            markersize = msize, markeredgecolor = edgecolor)
  ax1.set_ylabel('Cycles\nper req.', fontsize = text_size, rotation = 90)
  ax1.tick_params(labelsize = text_size * 0.9)
  ax1.set_ylim(bottom=0)
    
  for config, mark, color, edgecolor, msize in list(zip(configs, markers, colors, edgecolors, msizes))[::-1]:
    ax2.plot(xlabels, cpi[config], marker = mark, color = color, 
              markersize = msize, markeredgecolor = edgecolor)
  ax2.set_ylabel('Cycles\nper inst.', fontsize = text_size, rotation = 90)
  ax2.tick_params(labelsize = text_size * 0.9)
  ax2.set_ylim(bottom=1)
  
  for config, mark, color, edgecolor, msize in list(zip(configs, markers, colors, edgecolors, msizes))[::-1]:
    if config != 'CHERI':
      tlb_misses = [int(row[col_map[config][tlb_miss_heading]]) for row in table]
      tlbmpr = [miss/req for (miss, req) in zip(tlb_misses, nentries)]
      ax3.plot(xlabels, tlbmpr, marker = mark, color = color, 
                markersize = msize, markeredgecolor = edgecolor)
    else:
      tlb_misses = [int(row[col_map['Baseline'][tlb_miss_heading]]) for row in table]
      tlbmpr = [miss/req for (miss, req) in zip(tlb_misses, nentries)]
      ax3.plot(xlabels, tlbmpr, marker = mark, color = color, 
                markersize = msize, markeredgecolor = edgecolor)

  ax3.set_ylabel('TLB miss\nper req.', fontsize = text_size, rotation = 90)
  ax3.tick_params(labelsize = text_size * 0.9)
  # ax3.set_ylim(bottom=-0.25 * 1000000)
  
  ax3.set_xticklabels(xlabels, rotation = 80)
  ax3.set_xlabel('Dataset size', fontsize = text_size)
  
  ax1.legend(configs, bbox_to_anchor=(-0.22, 1, 1, 0), loc="lower left", 
             ncol=3, fontsize = text_size * 0.9)  
  fig.align_ylabels((ax1, ax2, ax3))
  fig.savefig('mycached_full.pdf', bbox_inches='tight')
  # plt.show()
    
if __name__ == '__main__':
  main()