import global_e.utility as utility
# from task1_universal import *
# from task2_bank import *

from task1_universal.create import Create
from task1_universal.model import Model
from task1_universal.process import Process

from task2_bank.create import BankCreate
from task2_bank.model import BankModel
from task2_bank.process import BankProcess

from task3_hospital.create import HospitalCreate
from task3_hospital.model import HospitalModal
from task3_hospital.process import HospitalProcess
from task3_hospital.exit import HospitalExit

# # Simple model
# c1 = Create(delayMean=5, name='Simple - Creator', distribution='exp')
# p1 = Process(maxqueue=3, delayMean=5, distribution='exp')

# c1.nextElement = [p1]
# elements = [c1, p1]
# model = Model(elements)
# model.simulate(1000)
# # ---------------------------------------

# # Channel model
# c1 = Create(delayMean=5, name='Channel - Creator', distribution='exp')
# p1 = Process(maxqueue=3, threads=2, delayMean=5, distribution='exp')

# c1.nextElement = [p1]
# elements = [c1, p1]
# model = Model(elements)
# model.simulate(1000)
# ---------------------------------------

# # Probability model
# p1 = Process(maxqueue=3, delayMean=5, distribution='exp')

# p1.probability = [0.7, 0.3]
# c1 = Create(delayMean=5, name='Probability - Creator', distribution='exp')
# p2 = Process(maxqueue=3, delayMean=5, distribution='exp')
# p3 = Process(maxqueue=3, delayMean=5, distribution='exp')

# c1.nextElement = [p1]
# p1.nextElement = [p2, p3]

# elements = [c1, p1, p2, p3]
# model = Model(elements)
# model.simulate(1000)
# ---------------------------------------

# Priority model
# p1 = Process(maxqueue=3, delayMean=5, distribution='exp')
# p1.priorities = [1, 2]

# c1 = Create(delayMean=5, name='Priority - Creator', distribution='exp')
# p2 = Process(maxqueue=3, name='Task 2', delayMean=5, distribution='exp')
# p3 = Process(maxqueue=3, name='Task 3', delayMean=5, distribution='exp')

# c1.nextElement = [p1]
# p1.nextElement = [p2, p3]

# elements = [c1, p1, p2, p3]
# model = Model(elements)
# model.simulate(1000)

# ---------------------------------------

# Bank model
# c1 = BankCreate(delayMean=0.5, name='Bank Creator', distribution='exp')
# p1 = BankProcess(maxqueue=3, delayMean=0.3, name='Casa 1', distribution='exp')
# p2 = BankProcess(maxqueue=3, delayMean=0.3, name='Casa 2', distribution='exp')

# c1.nextElement = [p1, p2]

# # ----Початкові умови----

# # Обидва касири зайняті
# p1.state[0] = 1
# p2.state[0] = 1

# # тривалість обслуговування для кожного касира нормально розподілена з
# # математичним очікуванням, рівним 1 од. часу, і середньоквадратичним відхиленням, рівним 0,3 од. часу;
# p1.tnext[0] = utility.normal(1, 0.3)
# p2.tnext[0] = utility.normal(1, 0.3)

# # Прибуття першого клієнта заплановано на момент часу 0,1 од. часу
# c1.tnext[0] = 0.1

# # У кожній черзі очікують по два автомобіля.
# p1.queue = 2
# p2.queue = 2

# element_list = [c1, p1, p2]
# bank = BankModel(element_list, items_to_balance=[p1, p2])
# bank.simulate(1000)

# ---------------------------------------

# Hospital model
c1 = HospitalCreate(delayMean=15.0, name='Hospital CREATOR', distribution='exp')

registration = HospitalProcess(
    maxqueue=100,
    threads=2,
    name='Registration',
    distribution='exp')

palata_way = HospitalProcess(
    maxqueue=100,
    delayMean=3.0, 
    delayDev=8,
    threads=3,
    name='Way to the palata',
    distribution='uniform')

lab_way = HospitalProcess(
    maxqueue=0,
    delayMean=2.0,
    delayDev=5,
    threads=10,
    name='Way to the lab registration',
    distribution='uniform')

lab_registration = HospitalProcess(
    maxqueue=100,
    delayMean=4.5,
    delayDev=3,
    threads=1,
    name='Registration to lab',
    distribution='erlang')

watching = HospitalProcess(
    maxqueue=100,
    delayMean=4.0,
    delayDev=2,
    threads=1,
    name='Docktor checking',
    distribution='erlang')

registration_way = HospitalProcess(
    maxqueue=0,
    delayMean=2.0,
    delayDev=5,
    threads=10,
    name='Way to the registration',
    distribution='uniform')

exit1 = HospitalExit(name='EXIT1')
exit2 = HospitalExit(name='EXIT2')

c1.nextElement = [registration]
registration.nextElement = [palata_way, lab_way]
palata_way.nextElement = [exit1]
lab_way.nextElement = [lab_registration]
lab_registration.nextElement = [watching]
watching.nextElement = [exit2, registration_way]
registration_way.nextElement = [registration]

registration.priority_patient_types = [1]

registration.patient_path = [[1], [2, 3]]
watching.patient_path = [[3], [2]]

elements = [c1, registration, palata_way, lab_way, lab_registration, watching, registration_way, exit1, exit2]

model = HospitalModal(elements)
model.simulate(1000)
