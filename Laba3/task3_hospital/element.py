from global_e.element import Element


class HospitalElement(Element):
    # Тип хворого Відносна частота Середній час
    #     1               0,5            15
    #     2               0,1            40
    #     3               0,4            30
    patient_type_delayMean = { 1: 15, 2: 40, 3: 30 }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_patient_type = None

    def getDelay(self):
        self.set_registration_delayMean()
        return super().getDelay()

    def set_registration_delayMean(self):
        if self.name == 'Registration':
            self.delayMean = HospitalElement.patient_type_delayMean[self.next_patient_type]

    def inAct(self, next_patient_type, tstart):
        pass
