import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt

st.header("Emergency Department Utilisation")
st.subheader("Daily Service Volume")
st.caption('https://digital.nhs.uk/data-and-information/publications/statistical/hospital-accident--emergency-activity/2020-21')

with st.sidebar:    
    
    daily_average = st.slider(
        "average daily service utilisation in number of arrivals", 
        min_value=30, max_value=700, value=60, step=5)

    duration = st.slider(
        "average time in emergency department from arrival to discharge", 
        min_value=1.5, max_value=10.0, value=3.0, step=0.25)

st.write(f"""
    A daily average of {daily_average} patient arrivals 
    counts to round about {round(daily_average*365/1000)},000 per year 
    which represents a *{['low-volume', 'high-volume'][daily_average*365 >= 50_000]}* emergency department.
    """)

a, b, c = [-0.41917051,  0.07538841, -0.00241279]
intercept = 2.976047189345115

demand_per_hour = [(a*hour**1 + b*hour**2 + c*hour**3 + intercept)*(daily_average/100) for hour in range(24)]

patients_waiting = [0 for _ in range(48)]

for h, arrival in enumerate(demand_per_hour):
    for i in range(round(duration)):
        patients_waiting[h+i] += arrival

patients_waiting = [round(x) for x in patients_waiting]
patients_waiting = [x + y for x, y in zip(patients_waiting[:24], patients_waiting[24:])]

demand = pd.DataFrame()
demand["arrivals"] = [round(x) for x in demand_per_hour]
demand["pat_waiting"] = patients_waiting

st.line_chart(demand)

st.write(f"""
    A service with {daily_average} arrivals per day on average 
    will see {demand['arrivals'][13]} arrivals between 13:00 and 14:00 o'clock.
    During that time there will be {patients_waiting[13]} patients in the department
    if average time spent in the ED is {duration} hours.
    """)

st.subheader("Arrivals & Discharge Simulation")

with st.expander("List of Arrivals and Discharges"):

    import random
    import simpy

    RANDOM_SEED = 42
    CAPACITY = int(daily_average/10)
    DURATION = duration
    ARRIVAL_TIME = 1
    SIM_TIME = 25

    class Emergency_Department(object):
        def __init__(self, env, capacity, duration):
            self.env = env
            self.capacity = simpy.Resource(env, capacity)
            self.duration = duration

        def care(self, patient):
            yield self.env.timeout(random.randrange(DURATION-2, DURATION+3))

    def patient(env, name, ed):
        arrival_time = env.now
        
        st.markdown('%s arrives at %d:00' % (name, env.now))
        with ed.capacity.request() as request:
            yield request

            yield env.process(ed.care(name))
            
            st.markdown('%s leaves at %d:00, time spent: %d hour(s)' % (name, env.now, env.now - arrival_time ))

    def setup(env, capacity, duration, arrival_time):
        ed = Emergency_Department(env, capacity, duration)

        i = 0
        
        for el in demand["arrivals"]:
            yield env.timeout(1)
            for _ in range(el):
                i += 1
                env.process(patient(env, 'Patient %d' % i, ed))


    random.seed(RANDOM_SEED)  # This helps reproducing the results

    env = simpy.Environment()
    env.process(setup(env, CAPACITY, DURATION, ARRIVAL_TIME))

    env.run(until=SIM_TIME)

st.subheader("Distribution of Specialties")
st.caption('Lee, Jarone, 2018, "Emergency Department Utilization Dataset", https://doi.org/10.7910/DVN/EZBGYR, Harvard Dataverse, V1, UNF:6:2pQqwsrwzkdWx9RFq5MIBg== [fileUNF]')

specialty_str = [
    'Circulatory',
    'Digestive',
    'Musculoskeletal',
    'Skin, Breast',
    'Nervous',
    'Respiratory',
    'Ear, Nose, Mouth, Dental',
    'Kidney, Urinary Tract',
    'Mental',
    'Injuries, Poisoning, Comp',
    'Health Status',
    'Endocrine, Metabolic',
    'Infections',
    'Alcohol / Drug, Abuse',
    'Eye',
    'Reproductive',
    'Blood, Immune System',
    'Pregnancy, Childbirth',
    'Liver, Pancreas',
    'Burns',
    'Neoplasm',
    'HIV Infections'
]

specialty_float = [
    0.14193708883852066,
    0.14033390458289569,
    0.13530322295317596,
    0.08413953231245508,
    0.07883243960417934,
    0.06971087401183039,
    0.0639338824700094,
    0.05591796119188457,
    0.04074299297915861,
    0.038006523301453925,
    0.03654154458510697,
    0.031179169661120016,
    0.023771352755818452,
    0.014566863839902704,
    0.012245010780032064,
    0.011471059760075184,
    0.007297252473879153,
    0.005998120404665819,
    0.005583503786831776,
    0.0015755431477693625,
    0.0008568743435236884,
    5.5282215711205703e-05
]

fig, ax = plt.subplots()
ax.pie(specialty_float[:-5], labels=specialty_str[:-5], rotatelabels=True, normalize=True)

st.pyplot(fig)

st.subheader("Literature")
st.caption("Yarmohammadian MH, Rezaei F, Haghshenas A, Tavakoli N. Overcrowding in emergency departments: A review of strategies to decrease future challenges. J Res Med Sci. 2017 Feb 16;22:23. doi: 10.4103/1735-1995.200277. PMID: 28413420; PMCID: PMC5377968.")
st.caption("Savioli G, Ceresa IF, Gri N, Bavestrello Piccini G, Longhitano Y, Zanza C, Piccioni A, Esposito C, Ricevuti G, Bressan MA. Emergency Department Overcrowding: Understanding the Factors to Find Corresponding Solutions. J Pers Med. 2022 Feb 14;12(2):279. doi: 10.3390/jpm12020279. PMID: 35207769; PMCID: PMC8877301.")