import warnings
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib import animation, rc
from IPython.display import HTML

from covid_abs.graphics import *
from covid_abs.experiments import *
from covid_abs.network.graph_abs import *
from covid_abs.network.util import *

global_parameters = dict(

    # General Parameters
    length=300,
    height=300,

    # Demographic
    population_size=300,
    homemates_avg=3,
    homeless_rate=0.0005,
    amplitudes={
        Status.Susceptible: 10,
        Status.Recovered_Immune: 10,
        Status.Infected: 10
    },

    # Epidemiological
    critical_limit=0.01,
    contagion_rate=.9,
    incubation_time=5,
    contagion_time=10,
    recovering_time=20,

    # Economical
    total_wealth=10000000,
    total_business=9,
    minimum_income=900.0,
    minimum_expense=600.0,
    public_gdp_share=0.1,
    business_gdp_share=0.5,
    unemployment_rate=0.12,
    business_distance=20
)

def pset(x, property, value):
    x.__dict__[property] = value
    return False


def vertical_isolation(a):
  if a.economical_status == EconomicalStatus.Inactive:
    if a.house is not None:
      a.house.checkin(a)
    return True
  return False


def sleep(a):
    if not new_day(a.iteration) and bed_time(a.iteration):
        return True
    #elif 9 <= a.iteration % 24 <= 11 and 14 <= a.iteration % 24 <= 16:
    #    return True
    return False

def lockdown(a):
    if a.house is not None:
        a.house.checkin(a)
    return True


def conditional_lockdown(a):
    if a.environment.get_statistics()['Infected'] > .05:
        return lockdown(a)
    else:
        return False


isolated = []


def sample_isolated(environment, isolation_rate=.5, list_isolated=isolated):
    for a in environment.population:
        test = np.random.rand()
        if test <= isolation_rate:
            list_isolated.append(a.id)


def check_isolation(list_isolated, agent):
    if agent.id in list_isolated:
        agent.move_to_home()
        return True
    return False

    global_parameters = dict(

    # General Parameters
    length=300,
    height=300,

    # Demographic
    population_size=300,
    homemates_avg=3,
    homeless_rate=0.0005,
    amplitudes={
        Status.Susceptible: 10,
        Status.Recovered_Immune: 10,
        Status.Infected: 10
    },

    # Epidemiological
    critical_limit=0.01,
    contagion_rate=.9,
    incubation_time=5,
    contagion_time=10,
    recovering_time=20,

    # Economical
    total_wealth=10000000,
    total_business=9,
    minimum_income=900.0,
    minimum_expense=600.0,
    public_gdp_share=0.1,
    business_gdp_share=0.5,
    unemployment_rate=0.12,
    business_distance=20
)

import copy
# most code is copied from the paper! very slim wrapper

def wrapper(g_param_mods,s_params,iterations=1440,iteration_time=25):
  g_params=gen_global_params(**g_param_mods)
  sim = GraphSimulation(**{**g_params, **s_params})
  anim = execute_graphsimulation(sim, iterations=iterations, iteration_time=iteration_time)
  #rc('animation', html='jshtml', embed_limit= 2**128)
  rc('animation', html='html5') #, embed_limit= 2**128
  return anim
  #save_gif(anim, 'do_nothing.gif')

def gen_global_params(**kwargs):
  '''Generates a dictionary of global parameters based on the research group's initial param set. Use a dictionary to feed in new parameter key/value pairs.'''
  g_params = copy.deepcopy(global_parameters)
  for key, val in kwargs.items():
    if key in g_params:
      print("Modifying parameter: {}. Base Value: {} New Value: {}".format(key,global_parameters[key],val))
      g_params[key] = val
    else:
      raise NotImplementedError("Adding new parameters to global parameters not yet implemented")
  
  return g_params

#example
g_param_mods = dict(amplitudes={
    Status.Susceptible: 15,
    Status.Recovered_Immune: 15,
    Status.Infected: 15},
    business_distance=10,
    )
s_params = dict(
    name='madison',
    initial_infected_perc=.02,
    initial_immune_perc=.01,
    contagion_distance=1.,
    callbacks={'on_execute': lambda x: sleep(x) }
    )

wrapper(g_param_mods,s_params)
