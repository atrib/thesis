#!/usr/bin/env python3
import csv
import json
import math
import sys

import warnings
warnings.filterwarnings("ignore")

# Radar plot code from matplotlib examples
# https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
def radar_factory(num_vars, frame='circle'):
  """
  Create a radar chart with `num_vars` axes.

  This function creates a RadarAxes projection and registers it.

  Parameters
  ----------
  num_vars : int
      Number of variables for radar chart.
  frame : {'circle', 'polygon'}
      Shape of frame surrounding axes.

  """
  # calculate evenly-spaced axis angles
  theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

  class RadarTransform(PolarAxes.PolarTransform):

    def transform_path_non_affine(self, path):
      # Paths with non-unit interpolation steps correspond to gridlines,
      # in which case we force interpolation (to defeat PolarTransform's
      # autoconversion to circular arcs).
      if path._interpolation_steps > 1:
          path = path.interpolated(num_vars)
      return Path(self.transform(path.vertices), path.codes)

  class RadarAxes(PolarAxes):

    name = 'radar'
    PolarTransform = RadarTransform

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      # rotate plot such that the first axis is at the top
      self.set_theta_zero_location('N')

    def fill(self, *args, closed=True, **kwargs):
      """Override fill so that line is closed by default"""
      return super().fill(closed=closed, *args, **kwargs)

    def plot(self, *args, **kwargs):
      """Override plot so that line is closed by default"""
      lines = super().plot(*args, **kwargs)
      for line in lines:
        self._close_line(line)

    def _close_line(self, line):
      x, y = line.get_data()
      # FIXME: markers at x[0], y[0] get doubled-up
      if x[0] != x[-1]:
        x = np.append(x, x[0])
        y = np.append(y, y[0])
        line.set_data(x, y)

    def set_varlabels(self, labels):
      self.set_thetagrids(np.degrees(theta), labels)

    def _gen_axes_patch(self):
      # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
      # in axes coordinates.
      if frame == 'circle':
        return Circle((0.5, 0.5), 0.5)
      elif frame == 'polygon':
        return RegularPolygon((0.5, 0.5), num_vars,
                              radius=.5, edgecolor="k")
      else:
        raise ValueError("Unknown value for 'frame': %s" % frame)

    def _gen_axes_spines(self):
      if frame == 'circle':
        return super()._gen_axes_spines()
      elif frame == 'polygon':
        # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
        spine = Spine(axes=self,
                      spine_type='circle',
                      path=Path.unit_regular_polygon(num_vars))
        # unit_regular_polygon gives a polygon of radius 1 centered at
        # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
        # 0.5) in axes coordinates.
        spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                            + self.transAxes)
        return {'polar': spine}
      else:
        raise ValueError("Unknown value for 'frame': %s" % frame)

  register_projection(RadarAxes)
  return theta
##################### End of radar plot code 

fontsize = 22

#######################################################################
class Table:
  
  def __init__(self):
    # List of mechanisms, and index of mechanism in table
    self.mechanisms = []
    self.mechanisms_idx = {}
    # List of factors, help and index of factor in table
    self.factors = []
    self.factor_help = {}
    self.factors_idx = {}
    # Table
    self.matrix = []
    # Points and net Scores for mechanisms once calculated
    self.points = {}
    self.scores = {}
    self.points_max = []
    # Errors encountered described
    self.errors = []
    # Help text for factors
    self.help = []
  
  def __str__(self):
    s = 'Table(\n\tmechanisms = {}\n\tfactors = {}\n\ttable = {}\n)'.format(
          self.mechanisms, 
          self.factors,
          self.matrix)
    s += '\tfactors_idx = {}\n'.format(
            self.factors_idx      
          )
    return s
  
  def validate_scoring(self, scoring):
    # Check all factors are keys
    for factor in self.factors:
      if factor not in scoring.keys():
        self.errors.append('key "{}" missing in scoring file'.format(factor))

  def score(self, scoring, normalize = 1):
    self.validate_scoring(scoring)
    if not self.valid():
      return
    
    for factor in self.factors:
      if factor not in scoring:
        self.errors.append('scoring for key "{}" missing in scoring file'.format(factor))
        return
      if len(scoring[factor]) == 0: 
        self.errors.append('scoring for key "{}" has zero values'.format(factor))
        return
    
    self.points_max = [max(scoring[factor].values()) for factor in self.factors]
    # print(self.points_max)
    maxscore = sum(self.points_max)
    # print(maxscore)
    self.help = [scoring['help'][factor] for factor in self.factors]
    
    # Calculate net score on axis for each mechanism
    for mechanism in self.mechanisms:
      score = 0
      mechanism_idx = self.mechanisms_idx[mechanism]
      points = []
      
      # print('Mechanism {} sees '.format(mechanism), end = '')
      # Mechanisms score as the sum of all factors on an axis
      for factor in self.factors:
        factor_idx = self.factors_idx[factor]
        value = self.matrix[mechanism_idx][factor_idx]
        # print('factor = {}, value = {}'.format(factor, value))
        point = scoring[factor][value]
        points.append(point)
        # print(' scores {} for (factor: {}, value: {}), '.format(point, factor, value), end = '')  
        score += point
      # print()
      
      self.points[mechanism] = points
      self.scores[mechanism] = (score * normalize / maxscore) if (normalize != 0) else score
  
  def valid(self):
    return len(self.errors) == 0
  
  def checkvalid(self):
    if not self.valid():
      for error in self.errors:
          print(error)
      sys.exit(1)
      
#**********************************************************************

# Data input functions
def read_table(axis):
  filename = axis + '.csv'
  table = Table()
  with open(filename) as csvfd:
    reader = csv.reader(csvfd)
    
    linecount = 0
    for row in reader:
      if row[0][0] == '#':
        continue
      linecount += 1
      # Strip trailing spaces
      row = [x.strip() for x in row]
      # First line lists factors considered
      if linecount == 1:
        row = row[1:]
        table.factors = row
        idx = 0
        for factor in row:
          table.factors_idx[factor] = idx
          idx += 1
      # Secondline contains help text for factors
      elif linecount == 2:
        row = row[1:]
        # Check that the csv widths are correct
        if(len(table.factors) != len(row)):
          table.errors.append('{}: Help has {} elements while there are {} factors'
                              .format(filename, len(row), len(table.factors)))
          break
        for (factor, help) in zip(table.factors, row):
          table.factor_help[factor] = help
      # Remaining lines actually explain/classify factors for mechanisms
      else:
        # Add mechanism to list of mechanisms
        mechanism = row[0]
        row = row[1:]        
        # Check that the csv widths are correct
        if(len(table.factors) != len(row)):
          table.errors.append('{}: Line {} has {} elements while there are {} factors'
                              .format(filename, linecount, len(row), len(table.factors)))
          break
        table.mechanisms.append(mechanism)
        # Track line index of mechanism
        table.mechanisms_idx[mechanism] = linecount - 3
        # Put line in table
        table.matrix.append(row)        
        
  return table

def read_scoring(axis):
  filename = axis + '_key.json'
  with open(filename) as jsonfd:
    scoring = json.load(jsonfd)
  return scoring

def plot(graphname, axes, labels, tables, normalize = 1):
  mechanisms = tables[axes[0]].mechanisms
  factors = tables[axes[0]].factors
  theta = radar_factory(len(axes), frame='polygon')
  ncols = 4
  nrows = math.ceil(len(mechanisms) / ncols)
  fig, axs = plt.subplots(figsize=(6 * ncols, 4.5 * nrows), 
                          nrows=nrows, ncols=ncols,
                          subplot_kw=dict(projection='radar'))
  edgebuffer = 0.05
  fig.subplots_adjust(wspace=0.4, hspace=0, 
                      bottom=-1.1*edgebuffer, 
                      left = edgebuffer, 
                      top   = 1 - edgebuffer, 
                      right = 1 - edgebuffer)

  colors = ['b', 'r', 'g', 'm', 'y']
  for ax, mechanism in zip(axs.flat, mechanisms):
    ax.set_title(mechanism, weight = 'bold', fontsize = fontsize * 1.2)
    
    data = [tables[x].scores[mechanism] for x in axes]
    ax.plot(theta, data, colors[0])
    ax.fill(theta, data, facecolor = colors[0], alpha=0.25, label='_nolegend_')
    if normalize != 0:
      ax.set_ylim(top = normalize)
      ax.set_yticklabels([])
      # ax.set_yticklabels(['', '', '', '', '{}'.format(normalize)])
    ax.set_varlabels(labels)
    ax.tick_params(axis = 'both', labelsize = fontsize, pad = 12)
    # print()
    
  # plt.show()
  fig.savefig('scoring_{}.pdf'.format(graphname))
  fig.savefig('scoring_{}.png'.format(graphname))

# ################### Table generation 
def to_words(n):
  if n == 0:
    return 'zero'
  
  name = 'neg' if n < 0 else ''
  n = abs(n)
  words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
  while n > 0:
    name = words[n % 10] + name
    n = int(n / 10)
  return name  
  
def generate_macros_and_images(fracs):
  # print(fracs)
  with open('table_macros.tex', 'w+') as fd:
    for n, d in fracs:
      filename = 'circle{}_{}.pdf'.format(n, d)
      commandname = 'frac{}outof{}'.format(to_words(n), to_words(d))
      # Create macro for latex
      line = '\\newcommand{{\\{}}}{{\\includegraphics[height=2ex]{{data/compsok/{}}}}}'.format(commandname, filename)
      print(line, file = fd)
      
      # Create pdf for table
      fig, ax = plt.subplots()
      ax.pie([abs(n), d - abs(n)], 
             colors = ['red' if n < 0 else 'black', 'white'],
             wedgeprops = {'edgecolor' : 'red' if n < 0 else 'black', 
                          'linewidth': 20, 
                          'antialiased': True},
             startangle=-270,
             counterclock=False
             )
      fig.savefig(filename)

    
def generate_table_frontmatter(fd, ncols, continued = False):
  columnformat = '!l| ' + '?c ' * (ncols - 1)
  print('\\begin{threeparttable}', file=fd)
  if continued:
    print('\t\\ContinuedFloat')
  # print('\t\\centering', file = fd)
  # Ignore {{\\linewidth}}
  print('\t\\begin{{tabular}}{{{}}}'.format(columnformat), file=fd)
  print('\t\t\\toprule', file = fd)
  
def generate_table_endmatter(fd, caption, label, help, continued = False):
  print('\t\t\\bottomrule', file = fd)
  print('\t\\end{tabular}', file=fd)
  # print('\t\\caption[{}]{{{}}}'.format('' if continued else caption, caption), file = fd)
  # print('\t\\label{{{}}}'.format(label), file = fd)
  
  print('\t\\begin{tablenotes}', file=fd)
  count = 0
  for htext in help:
    count += 1
    print('\t\t\\item[{}] {}'.format(count, htext), file = fd)
  print('\t\\end{tablenotes}', file=fd)
  
  print('\\end{threeparttable}', file=fd)

def factors(n):
  fac = set()
  for i in range(2, n + 1):
    if n % i == 0:
      fac.add(i)
  return fac

def simplify(numerator, denominator):
  if numerator == 0:
    return (0, 1)
  # print('{}/{}'.format(numerator, denominator))
  while (int(numerator) != numerator) or (int(denominator) != denominator):
    numerator *= 10
    denominator *= 10
    
  numerator = int(numerator)
  denominator = int(denominator)
  # print('{}/{}'.format(numerator, denominator))
    
  facs = factors(numerator).union(factors(denominator))
  
  for fac in facs:
    if numerator % fac == 0 and denominator % fac == 0:
      numerator = int(numerator / fac)
      denominator = int(denominator / fac)
  
  # print('{}/{}'.format(numerator, denominator))
  return (numerator, denominator)
  
def generate_table_row(fd, mechanism, axes, tables, normalize = 1):
  line = '\t\t'
  line += mechanism
  mechanism_idx = tables[axes[0]].mechanisms_idx[mechanism]
  fracs = set()
  
  for axis in axes:
    table = tables[axis]
    # Find points for particular mechanism for this factor. 
    # Assuming sorting of points and factors is same
    assert len(table.factors) == len(table.points[mechanism])
    for point, maxpoint in zip(table.points[mechanism], table.points_max):
      (p, m) = simplify(point, maxpoint)
      commandname = 'frac{}outof{}'.format(to_words(p), to_words(m))
      line += '& \\{} '.format(commandname)
      fracs.add((p, m))
      
  line += '\\\\'
  print(line, file = fd)
  return fracs
  
def generate_table_header_row(fd, axes, tables):
  print('\t\t\\rowstyle{\\bfseries}', file = fd)
  line = '\t\tMechanism '
  count = 0
  for axis in axes:
    for factor in tables[axis].factors:
      count += 1
      line += '& \\rotatebox{{{}}}{{{}}} '.format(90, '{}\\tnote{{{}}}'.format(factor, count))
  line += '\\\\ \\midrule'
  print(line, file = fd)

def datatable(graph, axes, tables, normalize = 1):
  # print(graph)
  fracs = set()
  with open('table_{}.tex'.format(graph), 'w+') as fd:
    ncols = sum([len(tables[axis].factors) for axis in axes])
    mechanisms = tables[axes[0]].mechanisms
    mechanisms_idx = tables[axes[0]].mechanisms_idx
    # print(axes)
    # print(tables)
    # print(tables[axes[0]].factors)
    # print(mechanisms)
    
    # Generate table
    generate_table_frontmatter(fd, ncols + 1)
    generate_table_header_row(fd, axes, tables)
    for mechanism in mechanisms:
      s = generate_table_row(fd, mechanism, axes, tables, normalize)
      # print(s)
      fracs = fracs.union(s)
    # print(fracs)
    generate_table_endmatter(fd, 'asdf', 'asdf', sum([tables[axis].help for axis in axes], []))
  
  return fracs
  
# Main application
def main():
  with open('axes.json') as axesfd:
    graphaxes = json.load(axesfd)
    fracs = set()
    
    for graph, axesdesc in graphaxes.items():
      axes = [x.strip() for x in axesdesc.keys()]
      axeshelp = [axesdesc[x].strip() for x in axesdesc.keys()]
      # print(row)
    
      # Input data from csv and json files
      # Get points for each scoring factor and score axes
      tables = {}
      scoring = {}
      for axis in axes:
        # print(axis)
        # Read table comparing mechanisms on one axis 
        axistable = read_table(axis)
        axistable.checkvalid()
        tables[axis] = axistable
        # print(axistable)
        
        # Read scoring for mechanisms for this axis
        axisscoring = read_scoring(axis)
        axistable.checkvalid()
        scoring[axis] = axisscoring
        
        # Calculate scoring on this axis
        tables[axis].score(axisscoring)
        axistable.checkvalid()
        # print('{}'.format(axistable.scores))
      
      # Plot data 
      plot(graph, axes, axeshelp, tables)
      
      # Table of data
      s = datatable(graph, axes, tables)
      fracs = fracs.union(s)
    # Generate 
    generate_macros_and_images(fracs)
  
if __name__ == '__main__':
  main()
