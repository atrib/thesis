#!/usr/bin/env python3
from cProfile import label
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

cum_cycles_heading = 'cum_mcycles'
text_size = 16

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
  trap = 81
  scinval_overhead = trap + 33
  sctfer_overhead = trap + 53
  screcv_overhead = trap + 45
  screval_overhead = trap + 47
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
    
  fig, ax = plt.subplots()
  markers = 'xvs'
  colors = [plt.cm.tab10(i) for i in range(len(configs))]
  for cfg, mark, color in zip(configs[:-1], markers, colors):
    ax.plot(pkt_sizes, cpb[cfg], marker = mark, color = color)
  cfg = 'sczcopy-' + '\u03bc' + 'code'
  ax.plot(pkt_sizes, cpb[cfg], color = colors[-2], 
          marker = markers[-1], linestyle = 'dotted')
  ax.set_xscale('log')
  ax.set_ylim(bottom=0)
  
  ax.set_xlabel('Packet size (bytes)', fontsize = text_size)
  ax.set_ylabel('Processing cycles per packet byte', fontsize = text_size)
  ax.tick_params(labelsize = text_size * 0.9)
  
  labels = ['Uncompartmentalized', 'Compartmentalized-copy', 
            'SecureCells ZC',  'SecureCells ZC-' + '\u03bc' + 'code']  
  plt.legend(labels, fontsize = 0.9 * text_size)
  fig.savefig('nfv_small.pdf', bbox_inches='tight')
  # plt.show()
  
if __name__ == '__main__':
  main()
