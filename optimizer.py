# code modifed from https://medium.com/thelorry-product-tech-data/load-optimization-problem-1baa116656df

from google.cloud import bigquery
import pandas as pd
pd.set_option("display.max_columns", None)

# Construct a BigQuery client object.
client = bigquery.Client("gcp-hackathon2023-16")

class Package:
    def __init__(self, weight, height, length, width):
        self.weight = weight
        self.height = height
        self.length = length
        self.width = width
        self.volume = height * length * width
packages = []
get_all_packages = client.query(""" SELECT * FROM `gcp-hackathon2023-16.Demo.Package` """)  # Make an API request.
for row in get_all_packages:
    packages.append(Package(row[0], row[1], row[2], row[3]))
    
class Vehicle:
    def __init__(self, name_id, quantity, max_weight, length, height, width):
        self.name_id = name_id
        self.quantity = quantity
        self.max_weight = max_weight
        self.max_volume = length * height * width
        self.length = length
        self.height = height
        self.width = width
        
vehicles = []
get_all_vehicles = client.query(""" SELECT * FROM `gcp-hackathon2023-16.Demo.Vehicle` """)  # Make an API request.
for row in get_all_vehicles:
    vehicles.append(Vehicle(row[0], row[1], row[2], row[3], row[4], row[5]))

# vehicles = [
#     Vehicle('LORRY-L', 5000, 24261874.16, 17 * 30.48, 7.2 * 30.48, 7 * 30.48),
#     Vehicle('LORRY-M', 3000, 19980366.96, 14 * 30.48, 7.2 * 30.48, 7 * 30.48),
#     Vehicle('LORRY-S', 1000, 7079211.65, 10 * 30.48, 5 * 30.48, 5 * 30.48),
#     Vehicle('VAN', 500, 2378615.11, 8 * 30.48, 3 * 30.48, 3.5 * 30.48),
#     Vehicle('4x4', 500, 1189307.56, 4 * 30.48, 3 * 30.48, 3.5 * 30.48)]
    

# Calculate the total weight and total volume of all packages
total_volume = sum(p.volume for p in packages)
total_weight = sum(p.weight for p in packages)
total_length = sum(p.length for p in packages)
total_width = sum(p.width for p in packages)
total_height = sum(p.height for p in packages)

# main process
from ortools.linear_solver import pywraplp
import warnings
warnings.filterwarnings('ignore')

# create data model for knapsack problem 
# paramter optimize are data to be packing into the available vehicle in totalLorry
def create_data_model(packages, vehicles):
    """Create the data for the example."""
    data = {}
    data['weights'] = list(p.weight for p in packages)
    data['volumes'] = list(p.volume for p in packages)
    data['heights'] = list(p.height for p in packages)
    data['lengths'] = list(p.length for p in packages)
    data['widths'] = list(p.width for p in packages)
    
    data['packages'] = list(range(len(data['weights'])))
    data['num_packages'] = len(data['weights'])
    
    max_volumes = []
    max_weights = []
    max_lengths = []
    max_widths = []
    max_heights = []
    truck_types = []
    
    # starting from small vehicle first
    vehicles.reverse()

    # register max_weight and max_volume for each available vehicle
    for v in vehicles:
        for i in range(v.quantity):
            max_volumes.append(v.max_volume)
            max_weights.append(v.max_weight)
            max_lengths.append(v.length)
            max_widths.append(v.width)
            max_heights.append(v.height)
            truck_types.append(v.name_id)
    
    data['max_volume'] = max_volumes 
    data['max_weight'] = max_weights 
    data['max_length'] = max_lengths
    data['max_width'] = max_widths
    data['max_height'] = max_heights
    data['truck_types'] = truck_types
    data['vehicles'] = list(range(len(data['max_volume'])))
    return data



data = create_data_model(packages, vehicles)

# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver('SCIP')

# Variables
# x[i, j] = 1 if item i is packed in bin j.
x = {}
for i in data['packages']:
    for j in data['vehicles']:
        x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

# Constraints
# Each item can be in at most one bin.
for i in data['packages']:
    solver.Add(sum(x[i, j] for j in data['vehicles']) <= 1)
    
# Each bin must not have an item which exceeds it's max height.
for j in data['vehicles']:
    for i in data['packages']:
        solver.Add(x[i,j] * data['heights'][i] <= data['max_height'][j])
        
# Each bin must not have an item which exceeds it's max length.
for j in data['vehicles']:
    for i in data['packages']:
        solver.Add(x[i,j] * data['lengths'][i] <= data['max_length'][j])
        
# Each bin must not have an item which exceeds it's max width.
for j in data['vehicles']:
    for i in data['packages']:
        solver.Add(x[i,j] * data['widths'][i] <= data['max_width'][j])

# The amount packed in each bin cannot exceed its max weight.
for j in data['vehicles']:
    solver.Add(
        sum(x[(i, j)] * data['weights'][i]
            for i in data['packages']) <= data['max_weight'][j])

# The amount packed in each bin cannot exceed its max volume.
for j in data['vehicles']:
    solver.Add(
        sum(x[(i, j)] * data['volumes'][i]
            for i in data['packages']) <= data['max_volume'][j])

# Add objectives
objective = solver.Objective()
for i in data['packages']:
    for j in data['vehicles']:
        objective.SetCoefficient(x[(i, j)], data['volumes'][i])
        
objective.SetMaximization()
status = solver.Solve()

# print info
_totalLeftVolume = 0
_totalLeftWeight = 0
if status == pywraplp.Solver.OPTIMAL:
    assign = []
    total_weight = 0
    total_packages = 0
    print('Total Packages:', len(packages))
    print()
    for j in data['vehicles']:
        bin_weight = 0
        bin_volume = 0
        print('Vehicle ', j, '[', data['truck_types'][j] ,'] - max_weight:[', "{:,.2f}".format(data['max_weight'][j]), '] - max volume:[', "{:,.2f}".format(data['max_volume'][j]), ']' )
        for i in data['packages']:
            if x[i, j].solution_value() > 0:
                assign.append(i)
                total_packages += 1
                print('Item', i, '- weight:', data['weights'][i],
                      ' volumes:', data['volumes'][i], ' height:', data['heights'][i])
                bin_weight += data['weights'][i]
                bin_volume += data['volumes'][i]
        print('Packed truck volume:', "{:,.2f}".format(bin_volume))
        print('Packed truck weight:', "{:,.2f}".format(bin_weight))
        print()
        if (bin_volume > 0) & (bin_weight > 0):
            leftVolume = data['max_volume'][j] - bin_volume
            leftWeight = data['max_weight'][j] - bin_weight
        else:
            leftVolume = 0
            leftWeight = 0
        print('Left Volume', "{:,.2f}".format(leftVolume))
        print('Left Weight', "{:,.2f}".format(leftWeight))
        print()
        print()
        total_weight += bin_weight
        _totalLeftVolume += leftVolume
        _totalLeftWeight += leftWeight
    print('Total packed weight:', "{:,.2f}".format(total_weight))
    print('Total packed volume:', "{:,.2f}".format(objective.Value()))
    print('Total item assigned:', "{:,.0f}".format(total_packages))
    print()
    print("#" * 100)
    print('Total Left Volume', "{:,.2f}".format(_totalLeftVolume))
    print('Total Left Weight', "{:,.2f}".format(_totalLeftWeight))
    print("#" * 100)
else:
    print('The problem does not have an optimal solution.')
print()