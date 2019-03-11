import threading
import time
import random
from queue import Queue

global threads, lock
threads = []
lock = threading.Lock()
customer_threads = []
customer_names = ["Aaron", "Fabian", "Barrett", "Harold", "Andrew", "Arnold", "Cam", "Cal",
         "Chris", "Charlie", "Dave", "Dan", "Derek", "Devin", "Eric",
         "Elijah", "Frank", "Fred", "Gary", "George", "Hal", "Harry",
         "Isaac", "Ishmael", "Jared", "Jake", "Jeremy", "Kevin", "Kris",
         "Larry", "Louie", "Mark", "Mort", "Nathan", "Norb", "Oscar",
         "Orville", "Peter", "Paul", "Quinn", "Rob", "Rick", "Steve",
         "Tim", "Trevor", "Ulysses", "Victor", "Walter", "Xavier",
         "Yadier", "Zack"]

barbers = ['Paul The Barber', 'John The Barber', 'Jack The Barber']
responses = ['is delighted with their haircut', 'is happy with their haircut', 'likes their haircut', 'is unhappy with their haircut', 'hates their haircut']
print('------------------------------------------------------------')
print('          The barbershop is getting ready to open           ')
print('------------------------------------------------------------')
time.sleep(2)
print('------------------------------------------------------------')
print('The barbershop is open and the first customers are arriving!')
print('------------------------------------------------------------')
time.sleep(2)


def addCustomer(name):
    global lock, customer_threads

    lock.acquire()
    customer_threads.append(name)
    lock.release()


def customerFinished(name):
    global lock, customer_threads

    lock.acquire()
    customer_threads.remove(name)
    lock.release()


def customer(sem_seats, waitingroom_seats,customer_name):
    global threads, lock
    print('>>>> {} enters the barbers and is looking for a seat'.format(customer_name))
    if not waitingroom_seats.full():
        i = 0
        sem_seats.acquire()
        waitingroom_seats.put(customer_name)
        sem_seats.release()
        addCustomer(customer_name)
        print(customer_name, 'has a seat in the waiting room')   
    else:
        print('There are no seats, {} leaves'.format(customer_name))


def barber(sem_barber, sem_seats, waitingroom_seats,barber_name):
    global threads, lock
    print('---> {} is awake and looking for a customer <---'.format(barber_name))
    if not waitingroom_seats.empty():
        sem_seats.acquire()
        customer = waitingroom_seats.get()
        sem_seats.release()
        sem_barber.acquire()
        print('{} is cutting {}\'s hair'.format(barber_name, customer))
        time.sleep(random.randint(1,10))
        print("{} is finished cutting {}'s hair".format(barber_name, customer))
        print("{} {} from {}".format(customer, random.choice(responses), barber_name))
        customerFinished(customer)
        sem_barber.release()
    else:
        print("No customers, time for sleep!")
    time.sleep(random.randint(1,10))


if __name__ == '__main__':
    
    waitingroom_seats = Queue(maxsize=15)
    sem_barber=threading.BoundedSemaphore(value=3)
    sem_seats=threading.BoundedSemaphore(value=15)

    for i in range(len(customer_names)):
        customer_name = random.choice(customer_names)
        t1 = threading.Thread(target=customer, name=customer_name, args=(sem_seats, waitingroom_seats,customer_name))
        threads.append(t1)
        customer_names.remove(customer_name)
        if random.randint(0,1) and len(barbers) != 0:
            barber_name = barbers[random.randint(0,2)]
            t2 = threading.Thread(target=barber, name=barber_name, args=(sem_seats, sem_barber, waitingroom_seats,barber_name))
            threads.append(t2)
    if len(barbers) != 0:
        for i in range(0,len(barbers)):
            barber_name = barbers[random.randint(0,2)]
            t2 = threading.Thread(target=barber, name=barber_name, args=(sem_seats, sem_barber, waitingroom_seats,barber_name))
            threads.append(t2)
    time.sleep(2)          

    for thread in threads:
        time.sleep(random.randint(1,10))
        thread.start()

    for thread in threads:
        thread.join()


    print ("All done for the day, time to close the Barbershop!")

