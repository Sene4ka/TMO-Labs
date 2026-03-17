import random

class Stats:
    def __init__(self):
        self.arrived = 0
        self.served = 0
        self.rejected = 0
        self.busy_time = 0

class Object:
    def __init__(self):
        pass

    def handle_time(self):
        return 0 # apply some state in children, ex. longer serve time for a patient for some reason

class Patient(Object):
    def __init__(self):
        super().__init__() # later do some gen with small probability of implying time-wasting problems

    def handle_time(self):
        return 0 # for now do not imitate special cases, later return additional time

class Worker:
    def __init__(self, env, stats):
        self.env = env
        self.stats = stats
        self.locked = False

    def work(self, target):
        pass # implement in children, do target handle

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def get_stats(self):
        return self.stats

class Doctor(Worker):
    def __init__(self, env, stats, mu_rate):
        super().__init__(env, stats)
        self.mu_rate = mu_rate

    def work(self, target):
        if self.locked:
            self.stats.rejected += 1
        else:
            self.lock()
            start_time = self.env.now
            service_time = random.expovariate(self.mu_rate)
            yield self.env.timeout(service_time + target.handle_time())
            self.unlock()
            self.stats.busy_time += (self.env.now - start_time)
            self.stats.served += 1

class StreamGenerator:
    def __init__(self, env, stats, worker):
        self.env = env
        self.stats = stats
        self.worker = worker

    def start(self):
        pass # start infinite generation with exp interval

class PatientStreamGenerator(StreamGenerator):
    def __init__(self, env, stats, worker, lambda_rate):
        super().__init__(env, stats, worker)
        self.lambda_rate = lambda_rate

    def start(self):
        while True:
            next_arrival_time = random.expovariate(self.lambda_rate)
            yield self.env.timeout(next_arrival_time)

            self.stats.arrived += 1
            self.env.process(self.worker.work(Patient()))