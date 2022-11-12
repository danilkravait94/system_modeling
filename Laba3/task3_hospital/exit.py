import numpy as np

from task3_hospital.element import HospitalElement


class HospitalExit(HospitalElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tnext = [np.inf]
        self.finished_times = [0, 0, 0]
        self.patient_type_count = [0, 0, 0]

    def inAct(self, next_patient_type, tstart):
        index = next_patient_type - 1
        self.finished_times[index] += self.tcurr - tstart
        self.patient_type_count[index] += 1

        # виконуємо збільшення лічильника кількості
        super().outAct()

    def get_mean_finished_time(self, patient_type):
        index = patient_type - 1
        count = self.patient_type_count[index]
        if count != 0:
            return self.finished_times[index] / count
        else:
            return np.inf
