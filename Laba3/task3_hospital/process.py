import numpy as np

from task3_hospital.element import HospitalElement


class HospitalProcess(HospitalElement):
    def __init__(self, patient_path=None, **kwargs):
        super().__init__(**kwargs)

        self.patient_types = [-1] * self.threads
        self.queue_patient_types = []

        self.patient_path = patient_path
        self.priority_patient_types = []

        self.time_to_lab = 0
        self.tprev_time_to_lab = 0

        self.tstarts = [-1] * self.threads
        self.tstart_queues = []

        self.patient_type2_finished_time = 0
        self.patient_type2_count = 0

    def inAct(self, next_patient_type, tstart):
        self.next_patient_type = next_patient_type

        if self.name == 'Way to the lab registration':
            self.time_to_lab += self.tcurr - self.tprev_time_to_lab
            self.tprev_time_to_lab = self.tcurr

        if self.name == 'Way to the registration' and next_patient_type == 2:
            self.patient_type2_finished_time += self.tcurr - tstart
            self.patient_type2_count += 1

        freeThreads = self.getAvailable() # беремо вільні потоки для процесу
        if len(freeThreads) > 0:
            for i in freeThreads:
                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                self.patient_types[i] = self.next_patient_type
                self.tstarts[i] = tstart
                break
        else:
            if self.queue < self.maxqueue:
                self.queue += 1
                self.queue_patient_types.append(self.next_patient_type)
                self.tstart_queues.append(tstart)
            else:
                self.failure += 1

    def outAct(self):
        super().outAct()

        threads = self.getCurrent() # беремо загалні, які виконуються
        for i in threads:
            self.tnext[i] = np.inf
            self.state[i] = 0

            prev_patient_type = self.patient_types[i]
            prev_tstart = self.tstarts[i]
            self.patient_types[i] = -1
            self.tstarts[i] = -1

            if self.queue > 0:
                self.queue -= 1
                priority_index = self.get_priority_index()
                self.next_patient_type = self.queue_patient_types.pop(priority_index)

                self.state[i] = 1
                self.tnext[i] = self.tcurr + super().getDelay()
                self.patient_types[i] = self.next_patient_type
                self.tstarts[i] = self.tstart_queues.pop(priority_index)
            if self.nextElement is not None:
                if self.name == 'Way to the registration':
                    self.next_patient_type = 1
                else:
                    self.next_patient_type = prev_patient_type

                if self.patient_path is None:
                    nextElement = np.random.choice(self.nextElement, p=self.probability)
                    nextElement.inAct(self.next_patient_type, prev_tstart)
                else:
                    for idx, path in enumerate(self.patient_path):
                        if self.next_patient_type in path:
                            nextElement = self.nextElement[idx]
                            nextElement.inAct(self.next_patient_type, prev_tstart)
                            break

    def get_priority_index(self):
        for i in self.patient_types:
            for j in np.unique(self.queue_patient_types):
                if j == i:
                    return self.queue_patient_types.index(j)
        else:
            return 0

    def printInfo(self):
        super().printInfo()
        print(f'queue={self.queue}; failure={self.failure}')
        print(f'Patient types={self.patient_types}')

    def doStatistics(self, delta):
        self.meanqueue_length = + delta * self.queue

    def get_type2_meantime(self):
        if self.patient_type2_count != 0:
            return self.patient_type2_finished_time / self.patient_type2_count
        else:
            return np.inf
