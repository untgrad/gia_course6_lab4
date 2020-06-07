#!/usr/bin/env python3
import psutil
import socket
import emails

# set system thresholds:
max_cpu_usage_perc = 80
max_disk_avail_perc = 20
max_mem_avail_mb = 500
local_host_ip = "127.0.0.1"


def chkCPU():
    """check if CPU usage % exceeds max threshold"""
    cpu_usage_perc = psutil.cpu_percent(interval=5)
    return cpu_usage_perc > max_cpu_usage_perc


def chkDisk():
    """check if Disk usage exceeds max threshold"""
    max_disk_usage_perc = 100 - max_disk_avail_perc
    dsk_usage_perc = psutil.disk_usage("/").percent
    return dsk_usage_perc > max_disk_usage_perc


def chkMem():
    """check if Memory usage % exceeds max threshold"""
    max_memory_avail = 2 ** 20 * max_mem_avail_mb
    mem_avail = psutil.virtual_memory().available
    return mem_avail < max_memory_avail


def chkNet():
    local_host_name = socket.gethostbyname("localhost")
    return local_host_name != local_host_ip


def sendAlert(alert):
    print(alert)
    sender = "automation@example.com"
    receiver = "student-02-9b4ca355b2b2@example.com"
    subject = alert
    body = "Please check your system and resolve the issue as soon as possible."
    message = emails.generate_email(sender, receiver, subject, body)
    emails.send_email(message)


def main():
    # check system resources:
    print("checking system resources")
    alert = None
    if chkCPU():
        alert = "Error - CPU usage is over {}%".format(max_cpu_usage_perc)
        sendAlert(alert)
    elif chkDisk():
        alert = "Error - Available disk space is less than {}%".format(
            max_disk_avail_perc
        )
        sendAlert(alert)
    elif chkMem():
        alert = "Error - Available memory is less than {}MB".format(max_mem_avail_mb)
        sendAlert(alert)
    elif chkNet():
        alert = "Error - localhost cannot be resolved to {}".format(local_host_ip)
        sendAlert(alert)
    else:
        print("system ok")


if __name__ == "__main__":
    main()
