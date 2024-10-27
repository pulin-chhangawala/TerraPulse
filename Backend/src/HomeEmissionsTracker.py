import pandas as pd
import random

zipcode_to_code_df = pd.read_csv('Backend\ZipToAreaCode.csv')
co2_per_unit_df = pd.read_csv('Backend\CO2perUnitbyAreaCode.csv')

def calculate_co2_electricity(zipcode, units):
    code_row = zipcode_to_code_df[zipcode_to_code_df['ZIP'] == zipcode]

    if code_row.empty:
        raise ValueError("ZipCode not found.")
    
    code = code_row['AreaCode'].values[0]
    
    co2_row = co2_per_unit_df[co2_per_unit_df['AreaCode'] == code]
    
    if co2_row.empty:
        raise ValueError("Code not found in CO2 emissions data.")
    
    co2_per_unit = co2_row['CO2_per_unit'].values[0]
    co2_per_unit_tonnes = co2_per_unit / 2204.62
    
    total_co2_per_unit = units * co2_per_unit_tonnes
    return total_co2_per_unit

def calculate_co2_gas(therms):
    co2_per_therm = 0.0053  # metric tonne CO2 per therm
    return therms * co2_per_therm

def ideal_CO2_Emissions_Per_People_in_Home(peopleInHome):
    # Convert yearly ideal emissions to monthly
    ideal_emissions_per_person = {
        1: 3.0 / 12,  # CO2 emissions per month for 1 person
        2: 5.0 / 12,
        3: 6.2 / 12,
        4: 7.3 / 12,
        5: 8.4 / 12,
        6: 9.5 / 12,
        7: 10.6 / 12,
        8: 11.7 / 12,
        9: 12.8 / 12,
        10: 13.9 / 12,
        11: 15.0 / 12
    }
    
    return ideal_emissions_per_person.get(peopleInHome, None)

def calculate_total_co2(zipcode, electricity_units, gas_units, peopleInHome):
    co2_electricity = calculate_co2_electricity(zipcode, electricity_units)
    co2_gas = calculate_co2_gas(gas_units)
    ideal_emissions = ideal_CO2_Emissions_Per_People_in_Home(peopleInHome)
    
    if ideal_emissions is None:
        raise ValueError("Number of people in home must be between 1 and 11.")
    
    total_co2 = co2_electricity + co2_gas
    
    return total_co2, co2_electricity, co2_gas, ideal_emissions

def suggest_actions(total_co2, ideal_emissions):
    minor_actions = [
        ("Switch to energy-efficient light bulbs.", 
         "LED bulbs use less energy than older CFL bulbs, reducing CO2 emissions and also last significantly longer"),
        
        ("Unplug devices when not in use.", 
         "This prevents phantom energy drain, leading to minor electricity savings, reducing emissions."),
        
        ("Reduce water heater temperature by a few degrees.", 
         "Lowering the temperatur decreases energy consumption caused due to burning gas for heating water."),
        
        ("Run dishwashers and washing machines at night.", 
         "This often utilizes energy from renewable sources, lowering emissions and saves you money on your electric bill in certain regions due to electricity being cheaper at night."),
        
        ("Use a microwave instead of an oven when possible.", 
         "Microwaves use significantly less energy on average than Ovens, leading to reduced CO2 emissions (Just dont use it to make Pizza)."),
        
        ("Set your thermostat a few degrees lower in winter, Use a humidifier to maintain comfort.", 
         "Lowering the thermostat reduces the energy burnt in the form of gas or electricity to heat your home, having a more humid surrounding(~60%) leads to a feeling of comfort even in colder temperatures."),
        
        ("Use fans instead of air conditioning when possible.", 
         "Fans consume significantly less energy than air conditioners, lowering emissions."),
        
        ("Shorten your shower time to save hot water.", 
         "Using less hot water reduces energy used for heating said water cutting your emissions, AND you save water."),
        
        ("Use cold water for laundry when possible.", 
         "Washing clothes with cold water saves energy needed to heat water and often leaves you with virtually the same result (Especially when doing regular laundry or washing bedsheets)."),
        
        ("Regularly clean or replace HVAC filters.", 
         "This improves home ventilation system efficiency, often times significantly reducing energy consumption and emissions while costing only a few bucks.")
    ]
    
    major_actions = [
        ("Install solar panels on your roof.",
         "Solar panels generate clean energy from the Sun (Duh!), significantly lowering your carbon footprint and paying for themselves in usually a decade or two."),

        ("Consider a high-efficiency furnace if you are planning to upgrade.",
         "Often times Older furnaces are very inefficient, for pretty obvious reasons, a more efficient furnace leads to less energy burnt and keeps your air clean."),

        ("Consider electric or hybrid vehicles.",
         "These vehicles produce fewer emissions than traditional gas-powered cars, and will reduce their emissions in the future as the electricity they run on transitions to renewable sources!!"),

        ("Improve home insulation to reduce heating needs.",
         "Better insulation prevents heat energy from escaping your home and significantly lowers energy consumption for heating and cooling over a long run."),

        ("Invest in a smart thermostat to optimize energy use.",
         "Smart thermostats help manage energy consumption more efficiently, by tweaking the temperatures depending on your need automatically, leading to not only saving energy but also to a more convinient temperature regulation."),
        
        ("Plant trees or create a garden to absorb CO2.", 
         "Plants naturally absorb CO2, helping to offset your emissions, although an average plant takes about 1-2 years to start being net positive so you should look into more self sufficient plants if you tend to take less care."),
         
        ("Switch to a composting system for organic waste.", 
         "Composting reduces methane emissions from landfills which is a major cause for the greenhouse effect and also gives your garden a nutritious meal once in a while.")
    ]
    
    actions = []
    
    if total_co2 < ideal_emissions:
        return ["Great job! Your emissions are below the ideal level, but you can always consider contributing more!! "]
    
    elif total_co2 <= ideal_emissions * 1.2:
        actions += random.sample(minor_actions, k=3)
    
    elif total_co2 <= ideal_emissions * 1.5:
        actions += random.sample(minor_actions, k=2)
        actions += random.sample(major_actions, k=1)
    
    elif total_co2 <= ideal_emissions * 2:
        actions += random.sample(minor_actions, k=1)
        actions += random.sample(major_actions, k=2)

    else:
        actions += random.sample(major_actions, k=3)
    
    return actions

def main(zipcode, electricity_units, gas_units, peopleInHome):
    try:
        total_co2, co2_electricity, co2_gas, ideal_emissions = calculate_total_co2(zipcode, electricity_units, gas_units, peopleInHome)
        actions = suggest_actions(total_co2, ideal_emissions)
        
        return {
            "Total CO2 Emissions (tonnes)": total_co2,
            "CO2 from Electricity (tonnes)": co2_electricity,
            "CO2 from Gas (tonnes)": co2_gas,
            "Ideal Emissions (tonnes)": ideal_emissions,
            "Suggestions": actions
        }
    except ValueError as e:
        return str(e)
