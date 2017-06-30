import time
import subprocess


def operation(name):
    command = 'curl -s -X POST https://api.telegram.org/bot{}/start'.format(token)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                        

def loader(cls, inq, outq, errq):
    while True:
        tupl = inq.get()
        if tupl is None:
            inq.task_done()
            break

        name = tupl
        start = time.time()
        operation(name)
        duration = time.time() - start
        outq.put(duration)
        inq.task_done()

    return

def load(name_list, con_num):

    (outq, errq,) = run_concurrently(loader, name_list, con_num)

    times = []
    while not outq.empty():
        i = outq.get()
        times.append(i)
        outq.task_done()

def run_concurrently(func, seq, threads_number):
    # Accepts:
    # func - a function or a bound method which is to take 3 parameters:
    #   input_queue, output_queue, error_queue;
    # seq  - a sequence of items that are put into the input queue;
    # threads_number - concurrency factor, the number of threads to use
    #  in a pool.
    # Returns output and error queues, correspondingly.
    inq, outq, errq,  = Queue(), Queue(), Queue()

    # Spawn thread pool
    workers = []
    for i in range(threads_number):
        worker = threading.Thread(target=func, args=(inq, outq, errq))
        worker.daemon = False
        worker.start()
        workers.append(worker)

    # Place work in queue
    for item in seq:
        inq.put(item)

    # Threads wait 'None' for exit
    for i in range(threads_number):
        inq.put(None)

    # Wait until worker threads are done to exit, then terminate
    inq.join()

    for worker in workers:
        worker.join()

    return (outq, errq,)

if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(os.path.join(dir_path, 'token'), 'r')
    token = f.read() #'310046588:AAGqktDy4wf71g-wpZD_H84JTJLY7nOD9b8'
    token = token[:-1]

    load(map(str, range(300)), 50)
