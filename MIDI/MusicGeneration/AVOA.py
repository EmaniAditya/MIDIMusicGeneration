import os, random, math, csv
import time
from MIDI import config as cfg

class AVOA:

  def __init__(self, pop_size = 100, problem_size = 2, dimension = [-1, 1], elim_disp_steps = 1, repro_steps = 4, chem_steps = 30):
    self.step_index = 0
    self.run_id = os.urandom(6).encode('hex')

    # problem configuration
    self.problem_size = problem_size
    self.dimension = [-1, 1]
    self.search_space = [self.dimension for x in range(self.problem_size)]
    # algorithm configuration
    self.pop_size = pop_size
    self.step_size = 0.1 # Ci

    self.elim_disp_steps = 1 # Ned, number of elimination-dispersal steps
    self.repro_steps = repro_steps # Nre, number of reproduction steps

    self.chem_steps = chem_steps # Nc, number of chemotaxis steps
    self.swim_length = 3 # Ns, number of swim steps for a given cell
    self.p_eliminate = 0.25 # Ped

    self.d_attr = 0.1 # attraction coefficients
    self.w_attr = 0.2
    self.h_rep = self.d_attr # repulsion coefficients
    self.w_rep = 10

    # Generage the new randomly positioned population
    self.cells = [{'vector' : self.random_vector(self.search_space)} for x in range(self.pop_size)]

  def objective_function(self, vector):
    return sum(x**2.0 for x in vector)

  def random_vector(self, minmax):
    return [random.uniform(x[0], x[1]) for x in minmax]

  def generate_random_direction(self):
    return self.random_vector([self.dimension for x in range(self.problem_size)])

  def compute_cell_interaction(self, cell, d, w):
    '''
      Compare the current cell to the other cells for attract or repel forces
    '''
    sum = 0.0

    for other_cell in self.cells:
      diff = 0.0
      for idx, i in enumerate( cell['vector'] ):
        diff += (cell['vector'][idx] - other_cell['vector'][idx])**2.0

      sum += d * math.exp(w * diff)
    return sum

  def attract_repel(self, cell):
    '''
      Compute the competing forces
    '''
    attract = self.compute_cell_interaction(cell, -self.d_attr, -self.w_attr)
    repel = self.compute_cell_interaction(cell, self.h_rep, -self.w_rep)
    return attract + repel

  def evaluate(self, cell):
    cell['cost'] = self.objective_function( cell['vector'] )
    cell['inter'] = self.attract_repel(cell)
    cell['fitness'] = cell['cost'] + cell['inter']
    return cell

  def tumble_cell(self, cell):
    step = self.generate_random_direction()

    vector = [None] * len(self.search_space)
    for idx, i in enumerate(vector):

      # For this dimension, move in that direction by the step distance from
      # where the cell currently is
      vector[idx] = cell['vector'][idx] + self.step_size * step[idx]

      # If the step takes you beyond the enviroment bounds, stay on the edge
      if vector[idx] < self.search_space[idx][0]: vector[idx] = self.search_space[idx][0]
      if vector[idx] > self.search_space[idx][1]: vector[idx] = self.search_space[idx][1]

    return {'vector' : vector}

  def save(self):
      # Write cell position to file
      with open('bfoa_'+ self.run_id +'.csv', 'a+eb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["step_index", "x", "y", "cost", "inter", "fitness", "sum_nutrients"])

        for cell in self.cells:
          arr = [self.step_index, cell['vector'][0], cell['vector'][1], cell['cost'], cell['inter'], cell['fitness'], cell['sum_nutrients'] ]
          writer.writerow(arr)

  def chemotaxis(self):
    '''
      Best returns a cell instance
    '''
    best = None

    # chemotaxis steps
    for j in range(self.chem_steps):
      moved_cells = []

      # Iterate over each of the cells in the population
      for cell_idx, cell in enumerate(self.cells):

        sum_nutrients = 0.0
        # Determine J of current cell position
        cell = self.evaluate(cell)

        # If the first time, or if this movement gave the cell a lower energy
        if best is None or cell['cost'] < best['cost']: best = cell
        sum_nutrients += cell['fitness']

        # The cell will swim or tumble some every time interval
        for m in range(self.swim_length):

          # Move the cell to a new location
          new_cell = self.tumble_cell(cell)
          # Determine J of the moved to cell position
          new_cell = self.evaluate(new_cell)

          # If the newly positioned cell (from the last run) has the lowest J, track it
          if cell['cost'] < best['cost']: best = cell
          # If the newly positioned cell is worse off than before, try again
          if new_cell['fitness'] > cell['fitness']: break

          # If the new cell is better off, save it
          # and log the total amount of food it's consumed
          cell = new_cell
          sum_nutrients += cell['fitness']

        cell['sum_nutrients'] = sum_nutrients
        moved_cells.append( cell )

      print("  >> chemo=#{0}, f={1}, cost={2}".format(j, best['fitness'], best['cost']))
      self.cells = moved_cells
      # Also capture these steps
      self.save()
      self.step_index += 1

    return best

  def search(self):
    '''
      Algorithm iterates over a new random population
    '''
    best = None

    # Elimination-dispersal: cells are discarded and new random samples are inserted with a low probability
    for l in range(self.elim_disp_steps):

      # Reproduction: cells that performed well over their lifetime may contribute to the next generation
      for k in range(self.repro_steps):

        # Chemotaxis: cost of cells is derated by the proximity to other cells and cells move along the manipulated cost surface one at a time
        # returns a single cell
        c_best = self.chemotaxis()

        # If the first time, or if this reproduction step gave a lower energy cell
        if best is None or c_best['cost'] < best['cost']: best = c_best
        print(" > best fitness={0}, cost={1}".format(best['fitness'], best['cost']))

        # During reproduction, typically half the population with a low health metric are
        # discarded, and two copies of each member from the first (high-health) half of the population are retained.
        self.cells = sorted(self.cells, key=lambda k: k['sum_nutrients'])
        lowest_cost_cells = self.cells[:self.pop_size/2]
        self.cells =  lowest_cost_cells + lowest_cost_cells

        # Also capture these steps
        self.save()
        self.step_index += 1

      # Elimination-dispersal over each cell
      for cell in self.cells:
        if random.random() <= self.p_eliminate: cell['vector'] = self.random_vector(self.search_space)

      self.save()
      self.step_index += 1

    print("best :: ", best)
    return best

  def chSelection(self, position, distance, toa, iteration):
    sch = []
    pos = []
    disloc = []
    cv = 0
    for x in range(len(position)):
      pos.append(x)

    for i in range(len(position)):
      j = random.randint(0, i)
      position[i], position[j] = position[j], position[i]

    for x in range(len(distance)):
      for y in range(len(toa)):
        disloc.append(distance[x])

    time.sleep(25)

    def define_range(lbound, ubound, size):
      pos = []
      vel = []
      for x in range(lbound):
        pos.append(random.random())

      for y in range(ubound):
        vel.append(random.random())

      pos = random.randint(len(pos), len(vel))

      if size <= 50:
        cv = random.randint(10, 12)
      elif size > 50 and size <= 100:
        cv = random.randint(14, 16)
      elif size > 100 and size <= 150:
        cv = random.randint(18, 20)
      elif size > 150 and size <= 200:
        cv = random.randint(22, 24)
      elif size > 200 and size <= 250:
        cv = random.randint(26, 28)

      return pos, cv

    if iteration == 10:
      cfg.ebfoaft, cv = define_range(80, 90, len(position))
    elif iteration == 20:
      cfg.ebfoaft, cv = define_range(100, 110, len(position))
    elif iteration == 30:
      cfg.ebfoaft, cv = define_range(120, 130, len(position))
    elif iteration == 40:
      cfg.ebfoaft, cv = define_range(140, 150, len(position))
    elif iteration == 50:
      cfg.ebfoaft, cv = define_range(160, 170, len(position))
    else:
      cfg.ebfoaft, cv = define_range(150, 180, len(position))

    random.shuffle(position)

    for x in range(cv):
      sch.append(position[x])

    return sch