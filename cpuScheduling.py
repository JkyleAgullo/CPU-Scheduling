import heapq

class Process:
    def __init__(self, process_id, arrival_time, burst_time, priority):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.remaining_time = burst_time


def round_robin_sched(processes, time_quantum):
    queue = processes.copy()
    current_time = 0

    while queue:
        current_process = queue.pop(0)
        current_time = max(current_time, current_process.arrival_time)

        if hasattr(current_process, 'remaining_time'):  # Check if the attribute already exists
            if current_process.remaining_time <= time_quantum:
                current_time += current_process.remaining_time
                current_process.remaining_time = 0
            else:
                current_time += time_quantum
                current_process.remaining_time -= time_quantum
                queue.append(current_process)
        else:
            if current_process.burst_time <= time_quantum:  # Initialize remaining_time if not present
                current_time += current_process.burst_time
                current_process.remaining_time = 0
            else:
                current_time += time_quantum
                current_process.remaining_time = current_process.burst_time - time_quantum
                queue.append(current_process)

        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

    print("ROUND ROBIN SCHEDULING\n")
    calculate_metrics(processes)


def shortest_job_first_sched(processes):
    queue = processes.copy()
    current_time = 0

    while queue:
        queue.sort(key=lambda x: (x.burst_time, x.arrival_time))  # Sort the queue based on burst time (shortest job first)
        current_process = queue.pop(0)

        current_time = max(current_time, current_process.arrival_time)
        current_time += current_process.burst_time
        current_process.completion_time = current_time
        current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

    print("SHORTEST JOB FIRST SCHEDULING", end="\n\n")
    calculate_metrics(processes)


def pre_emptive_priority(processes):
    queue = []
    current_time = 0
    completed_processes = []

    while processes or queue:
        while processes and processes[0].arrival_time <= current_time:
            process = processes.pop(0)
            heapq.heappush(queue, (process.priority, process))

        if queue:
            current_process = heapq.heappop(queue)[1]

            if current_process.remaining_time == current_process.burst_time:
                current_process.waiting_time = current_time - current_process.arrival_time

            if current_process.remaining_time > 0:
                current_process.remaining_time -= 1
                current_time += 1

                heapq.heappush(queue, (current_process.priority, current_process))
            else:
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                completed_processes.append(current_process)

        else:
            current_time += 1

    print("PREEMPTIVE PRIORITY SCHEDULING", end="\n\n")
    calculate_metrics(completed_processes)


def calculate_metrics(processes):
    total_waiting_time = 0
    total_turnaround_time = 0
    total_cpu_burst_time = 0
    num_processes = len(processes)

    for process in processes:
        total_waiting_time += process.waiting_time
        total_turnaround_time += process.turnaround_time
        total_cpu_burst_time += process.burst_time

    cpu_utilization = (total_cpu_burst_time / float(processes[-1].completion_time)) * 100
    system_throughput = num_processes / float(processes[-1].completion_time)
    avg_waiting_time = total_waiting_time / float(num_processes)
    avg_turnaround_time = total_turnaround_time / float(num_processes)

    for process in processes:
        print(f"P{process.process_id} Waiting Time: {process.waiting_time}")
    print("\nCPU Utilization: {:.2f}%".format(cpu_utilization))
    print("System Throughput: {:.2f}".format(system_throughput))
    print("Average Waiting Time: {:.2f}".format(avg_waiting_time))
    print("Average Turnaround Time: {:.2f}".format(avg_turnaround_time))
    print("\n")


def main():
    # Create a list of Process objects
    processes = [
        Process(1, 0, 8, 3),
        Process(2, 1, 6, 1),
        Process(3, 2, 9, 2),
        Process(4, 3, 5, 4)
    ]

    # Perform scheduling using the defined functions
    round_robin_sched(processes, 2)
    shortest_job_first_sched(processes)
    pre_emptive_priority(processes)


if __name__ == "__main__":
    main()
