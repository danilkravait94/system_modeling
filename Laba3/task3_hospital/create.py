import numpy as np
from task3_hospital.element import HospitalElement


class HospitalCreate(HospitalElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def outAct(self):
        # виконуємо збільшення лічильника кількості
        super().outAct()
        # встановлюємо коли пристрій буде вільним
        self.tnext[0] = self.tcurr + super().getDelay()
        # Тип хворого Відносна частота Середній час
        #     1               0,5            15
        #     2               0,1            40
        #     3               0,4            30
        self.next_patient_type = np.random.choice([1, 2, 3], p=[0.5, 0.1, 0.4])
        nextElement = self.get_nextElement()
        nextElement.inAct(self.next_patient_type, self.tcurr)
