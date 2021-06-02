import random
import numpy as np
import numpy_financial as npf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


DEFAULT_ASSUMPTIONS = {
    'Anual Production (Bags/Ha.Year)': {'min': 25, 'likely': 55, 'max': 70},
    'Anual Production Growth (% Yearly)': {'min': 0, 'likely': 1, 'max': 1.5, },
    'Production Cost (R$/Ha.Year)': {'min': 1800 , 'likely': 2500, 'max': 3200},
    'Commodity Price ($/Bag)': {'min': 9.2 , 'likely': 20.8, 'max': 40,},
    'Dolar Price (R$/$)': {'min': 3, 'likely': 5, 'max': 12,},
    'Real Interest Rate (% Yearly)': {'min': 2, 'likely': 5, 'max': 15},
    'Tax Rate on Profit(%)': {'min': 5, 'likely': 5, 'max': 5, },
    }

class MonteCarlo:
    '''MonteCarlo simulator for agricultural business investments'''
    def __init__(self, assumptions, number_simulations, years_per_simulation):
        '''
        assumptions: dict a set of assumptions. 
        '''
        self.assumptions = assumptions
        self.number_simulations = number_simulations
        self.years_per_simulation = years_per_simulation
        self.npvs = None
        self.timeline_example = self.simulate_timeline()
        
    def _calc_triang(self, var_name):
        '''Wrapper function for random.triangular; returns a random number from proposed the distribution in self.assumptions
        var_name: name of variable from self.assumptions to draw a random number
        '''
        return [random.triangular(self.assumptions[var_name]['min'],
                                  self.assumptions[var_name]['max'],
                                  self.assumptions[var_name]['likely'])
                                 ][0]
    def _relu(self, x):
        '''
        Helper function - Rectified linear unit
        x: number
        '''
        
        return x if x>0 else x

    def simulate_year(self, cumulative_prod_growth):
        '''Simulates a single year
        Returns a dict with this year simulated accounting
        cumulative_prod_growth: cumulative production growth scalar used to estimate future production
        '''
        #draws a random number of all relavant assumptions parameters
        production = self._calc_triang('Anual Production (Bags/Ha.Year)')
        production_cost = self._calc_triang('Production Cost (R$/Ha.Year)')
        comodity_price = self._calc_triang('Commodity Price ($/Bag)')
        dolar_price = self._calc_triang('Dolar Price (R$/$)')
        real_interest_rate = self._calc_triang('Real Interest Rate (% Yearly)')
        tax_rate = self._calc_triang('Tax Rate on Profit(%)')
        
        #scales production by the cumulative production growth so far
        production = production * cumulative_prod_growth


        #calculates the revenue and pretax income
        revenue = production * comodity_price * dolar_price
        pretax_income = revenue - production_cost
        
        #calculates taxes as a percentage of pretax income. 
        #If there was a loss, taxes are set to zero with _relu
        taxes = self._relu(pretax_income * tax_rate/100)
        
        #cashflow or net income
        cashflow = pretax_income - taxes
        
        year_results = { 
            'Anual Production (Bags/Ha.Year)': production,
            'Cumulative Prod. Growth': cumulative_prod_growth,
            'Commodity Price ($/Bag)': comodity_price,
            'Dolar Price (R$/$)': dolar_price,
            'Revenue (R$/Ha.Year)': revenue,
            'Production Cost (R$/Ha.Year)': production_cost,
            'Pretax Income (R$/Ha.Year)': pretax_income,
            'Taxes (R$)': taxes,
            'Cashflow(R$/Ha.Year)': cashflow,
            'Real Interest Rate (% Yearly)': real_interest_rate
            }
        return year_results

    def simulate_timeline(self):
        '''
        Simulate a single timeline of however many years was defined in years_per_simulation parameter
        Returns a DataFrame with the timelines accounting 
        '''
        timeline = {}
        cumulative_growth = 1
        for year, results in enumerate(range(self.years_per_simulation)):
            growth = self._calc_triang('Anual Production Growth (% Yearly)')/100
            cumulative_growth *= 1+growth
            timeline[f'Year {year+1}'] = self.simulate_year(cumulative_growth)
        timeline = pd.DataFrame(timeline)
        return timeline

    def calculate_npv(self):
        npvs = []
        for timeline in range(self.number_simulations):
            timeline_results = self.simulate_timeline()
            cashflows = timeline_results.loc['Cashflow(R$/Ha.Year)']
            real_interest_rates = timeline_results.loc['Real Interest Rate (% Yearly)']
            
            #the discount rate must be a scalar in npf.npv
            #therefore it was set to be the geometric mean of the real interest rate in that timeline
            def geometric_mean(iterable):
                a = np.array(iterable)
                return a.prod()**(1.0/len(a))
            
            real_interest_rates_mean = geometric_mean(real_interest_rates.values/100 + 1)
            
            npv = npf.npv(real_interest_rates_mean - 1, cashflows)
            npvs.append(npv)
        npvs = pd.DataFrame(npvs, columns=['NPV'])
        setattr(self, 'npvs', npvs)
        return npvs
    
    def create_graphs(self):
        '''
        Creates 2 Graphs showcasing the Net Present Value distribution across simulations
        '''
        font = {'size'   : 12}
        matplotlib.rc('font', **font)
        if self.npvs is None:
            setattr(self, 'npvs', self.calculate_npv())
        
        npv_dist = sns.displot(self.npvs, x='NPV',)
        ticks = npv_dist.axes[0][0].get_xticks()
        xlabels = ['R$' + '{:,.0f}'.format(x) for x in ticks]
        npv_dist.set_xticklabels(xlabels, rotation=45)
        npv_dist.set_axis_labels(x_var='Net Present Value/Hectare')
        
        npv_cumult_dist = sns.displot(self.npvs, x='NPV', kind='ecdf',
                              complementary=True, height=6, 
                              aspect=1.1618)
        xticks1 = npv_cumult_dist.axes[0][0].get_xticks()
        xlabels1 = ['R$' + '{:,.0f}'.format(x) for x in xticks1]
        ylabels1 = npv_cumult_dist.axes[0][0].get_yticks()
        ylabels1 = [f'{int(ylabel*100)}%' for ylabel in ylabels1]
        
        npv_cumult_dist.set_xticklabels(xlabels1, rotation=45)
        npv_cumult_dist.set_yticklabels(ylabels1, rotation=45)
        npv_cumult_dist.set_axis_labels(x_var='Net Present Value/Agricultural Land Hectare', 
                                        y_var='Probability of at least this NPV')
        return npv_dist, npv_cumult_dist



class Interface:
    '''
    Creates a user interface for exploring different assumptions parameters configurations 
    '''
    def __init__(self, assumptions=DEFAULT_ASSUMPTIONS):

        self.root = tk.Tk()
        self.root.title('Agricultural Land Valuation')
        #https://icon-library.com/icon/soy-icon-24.html
        self.root.iconbitmap('icon.ico')
        
        
        self.mainframe = tk.Frame(self.root)
        self.mainframe.pack()
        self.assumptions = assumptions
       
        self.construct_assumptions_table_UI()
        self.construct_montecarlo_params_UI()
        self.construct_run_UI()
        
        self.root.mainloop()
    def construct_assumptions_table_UI(self):
        '''
        Creates a spreadsheet for altering the viewing and altering parameters
        '''
        #initializes spreadsheet
        min_label = tk.Label(self.mainframe, text='Minimum')
        likely_label = tk.Label(self.mainframe, text='Most Likely')
        max_label = tk.Label(self.mainframe, text='Maximum')
        
        #sets the location for each column 
        min_label.grid(row=0, column=1)
        likely_label.grid(row=0, column=2)
        max_label.grid(row=0, column=3)
        
        entry_dict = {}
        
        #Creates a new line foi input for each of the initial assumptions
        #and inserts the default value
        for i, assumption in enumerate(self.assumptions):
            label = tk.Label(self.mainframe, text=assumption)
            
            min_entry = tk.Entry(self.mainframe)
            min_entry.insert(0, self.assumptions[assumption]['min'])
            
            likely_entry = tk.Entry(self.mainframe)
            likely_entry.insert(0, self.assumptions[assumption]['likely'])
            
            max_entry = tk.Entry(self.mainframe)
            max_entry.insert(0, self.assumptions[assumption]['max'])
            
            entry_dict[assumption] = {'min': min_entry,
                                      'likely': likely_entry,
                                      'max': max_entry
                                      }
            #positions each widget
            label.grid(row=i+1, column=0)
            min_entry.grid(row=i+1, column=1)
            likely_entry.grid(row=i+1, column=2)
            max_entry.grid(row=i+1, column=3)
        self.entry_dict = entry_dict

    def user_input_to_assumption_dict(self):
        '''
        Collects user input assumptions to a new self.assumptions dict
        '''
        assumptions = {}
        for assumption_entry in self.entry_dict.keys():
            assumptions[assumption_entry] = {parameter_edge: float(self.entry_dict[assumption_entry]
                                                                   [parameter_edge].get()) 
                                             for parameter_edge in 
                                             self.entry_dict[assumption_entry]}
        return assumptions

    def run_simulation_and_display_results(self):
        self._clear_frame(self.results_frame)
        number_simulations = int(self.number_simulations_entry.get())
        years_per_simulation = int(self.years_per_simulation_entry.get())
        
        #updates assumptions dict at run time
        assumptions = self.user_input_to_assumption_dict()
        simulator = MonteCarlo(assumptions, number_simulations, years_per_simulation)

        results = simulator.calculate_npv()
        npv_mean = tk.Label(self.results_frame, 
                            text='Average NPV: R$'+ '{:,.0f}'.format(results.mean()[0]) +'.00')
        dist, cumul_dist = simulator.create_graphs()
        
        #displays NPV distributions
        fig0 = dist.fig
        fig0.tight_layout()
        image_frame = tk.Frame(self.results_frame)
        canvas0 = FigureCanvasTkAgg(fig0, master=image_frame)
        canvas0.get_tk_widget().grid(row=0, column=0)
        
        
        #displays NPV cumulative distributions
        fig1 = cumul_dist.fig
        fig1.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=image_frame)
        canvas1.get_tk_widget().grid(row=0, column=1)
        image_frame.pack()
        
        npv_mean.pack()
        self.results_frame.pack()

    def _clear_frame(self, frame_var):
        '''
        Destroys all widgets from frame
        '''
        for widget in frame_var.winfo_children():
           widget.destroy()
    def construct_montecarlo_params_UI(self):
        '''
        Creates and collects user input for MonteCarlo engine parameters
        '''
        mc_params_frame = tk.Frame(self.root)
        mc_params_frame.pack()
        
        #creates and positions number of simulations parameter
        number_simulations_label = tk.Label(mc_params_frame, text="Number of Simulations")
        number_simulations_entry = tk.Entry(mc_params_frame)
        #sets number of simulation to 1000 as default
        number_simulations_entry.insert(0, 1000)
        number_simulations_label.grid(row=0,column=0)
        number_simulations_entry.grid(row=0,column=1)
        self.number_simulations_entry = number_simulations_entry
        
        #creates and positions the years per simulation parameter
        years_per_simulation_label = tk.Label(mc_params_frame, text="Years/Simulation")
        years_per_simulation_entry = tk.Entry(mc_params_frame)
        #sets 20 years per simulation as default
        years_per_simulation_entry.insert(0, 20)
        years_per_simulation_label.grid(row=1,column=0)
        years_per_simulation_entry.grid(row=1,column=1)
        self.years_per_simulation_entry = years_per_simulation_entry
        
    def construct_run_UI(self):
        '''
        Construct and positions the run button
        '''
        run_frame = tk.Frame(self.root)
        run_frame.pack()
        button = tk.Button(run_frame, 
                           command=self.run_simulation_and_display_results, 
                           text='Run Simulations')
        button.pack()
        results_frame = tk.Frame(self.root)
        self.results_frame = results_frame

if __name__=='__main__':
    UI = Interface()

