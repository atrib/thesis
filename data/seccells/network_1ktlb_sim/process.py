#!/usr/bin/env python3
from cProfile import label
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams

cum_cycles_heading = 'cum_mcycles'
text_size = 12

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

def main():
  with open('data.csv') as datafd:
    table = [line for line in csv.reader(datafd, delimiter=',')]
    
  configs = table[0]
  iters   = table[1]
  fields  = table[2]
  
  table = table[3:]
  pkt_sizes = [int(row[0]) for row in table]
  
  col_map = {}
  last_cfg = None
  for cfg,field,iter,col_idx in zip(configs, fields, iters, range(len(fields))):
    if cfg == '':
      cfg = last_cfg
    else:
      last_cfg = cfg
      col_map[cfg] = {}
    
    col_map[cfg][field] = col_idx
  configs = [cfg for cfg in configs if cfg != '']
  configs.append('sczcopy-' + '\u03bc' + 'code')
  
  # print(col_map)
  
  cpb = {}
  trap = 79
  scinval_overhead = trap + 35
  sctfer_overhead = trap + 61
  screcv_overhead = trap + 54
  screval_overhead = trap + 39
  overhead = scinval_overhead + screval_overhead + 2 * (sctfer_overhead + screcv_overhead)
  npackets = 16
  for cfg in configs:
    if cfg == 'sczcopy-' + '\u03bc' + 'code':
      cum_cycles = [int(row[col_map['sczcopy'][cum_cycles_heading]]) for row in table]
      cycles = [(this - prev) for (this, prev) in zip(cum_cycles, [0] + cum_cycles[:-1])]
      cycles = [val - (overhead * npackets) for val in cycles]
    else:
      cum_cycles = [int(row[col_map[cfg][cum_cycles_heading]]) for row in table]
      cycles = [(this - prev) for (this, prev) in zip(cum_cycles, [0] + cum_cycles[:-1])]
    
    cycles_per_byte = [cycle / (size * npackets) for (cycle, size) in zip(cycles, pkt_sizes)]
    cpb[cfg] = cycles_per_byte
  
  figsize = rcParams['figure.figsize']
  figsize = (figsize[0], 0.75*figsize[1])
  fig, ax = plt.subplots(figsize = figsize)
  markers = 'xv*'
  msizes = 10
  # colors = [plt.cm.tab10(i) for i in range(len(configs))]
  colors = ['silver', 'darkorange', 'royalblue']
  edgecolors = ['dimgray', 'orangered', 'blue']
  for cfg, mark, color, edgecolor in zip(configs[:-1], markers, colors, edgecolors):
    ax.plot(pkt_sizes, cpb[cfg], marker = mark, color = color, 
            markeredgecolor = edgecolor, markersize = msizes)
  cfg = 'sczcopy-' + '\u03bc' + 'code'
  ax.plot(pkt_sizes, cpb[cfg], color = colors[-1], 
          marker = markers[-1], linestyle = 'dotted', markeredgecolor = edgecolor, 
          markersize = msizes)
  ax.set_xscale('log')
  ax.set_ylim(bottom=0)
  
  ax.set_xlabel('Packet size (bytes)', fontsize = text_size)
  ax.set_ylabel('Processing cycles\nper packet byte', fontsize = text_size)
  ax.tick_params(labelsize = text_size * 0.9)
  
  labels = ['Uncompartmentalized', 'Compartmentalized-copy', 
            'SecureCells ZC',  'SecureCells ZC-' + '\u03bc' + 'code']  
  plt.legend(labels, fontsize = 0.9 * text_size)
  fig.savefig('nfv_full.pdf', bbox_inches='tight')
  # plt.show()
  
if __name__ == '__main__':
  main()
