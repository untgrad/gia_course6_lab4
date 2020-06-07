#!/usr/bin/env python3
import psutil
import socket
import emails

# set system thresholds:
max_cpu_usage_perc = 80
max_disk_avail_perc = 20
max_mem_avail_mb = 500
chk_local_host_ip = "127.0.0.1"


def chkCPU():
    """check if CPU usage % exceeds max threshold"""
    cpu_usage_perc = psutil.cpu_percent(interval=3)
    return cpu_usage_perc > max_cpu_usage_perc


def chkDisk():
    """check if Disk usage exceeds max threshold"""
    max_disk_usage_perc = 100 - max_disk_avail_perc
    dsk_usage_perc = psutil.disk_usage("/").percent
    return dsk_usage_perc > max_disk_usage_perc


def chkMem():
    """check if Memory usage % exceeds max threshold"""
    one_mb = 2 ** 20
    max_mem_avail = one_mb * max_mem_avail_mb
    mem_avail = psutil.virtual_memory().available
    return mem_avail < max_mem_avail


def chkNet():
    """check if local host name resolves to local IP"""
    local_host_ip = socket.gethostbyname("localhost")
    return local_host_ip != chk_local_host_ip


def sendAlert(alert):
    """output alert error and send email"""
    content = {
        "sender": "automation@example.com",
        "receiver": "student@example.com",
        "subject": alert,
        "body": "Please check your system and resolve the issue as soon as possible.",
        "attachment": None,
    }
    try:
        message = emails.generate_email(**content)
        emails.send_email(message)
    except:
        print("unable to send alert email notification!")
    finally:
        print(alert)
        exit(1)


def main():
    # check system resources:
    print("checking system resources")
    alert = None
    if chkCPU():
        alert = f"Error - CPU usage is over {max_cpu_usage_perc}%"
    elif chkDisk():
        alert = f"Error - Available disk space is less than {max_disk_avail_perc}%"
    elif chkMem():
        alert = f"Error - Available memory is less than {max_mem_avail_mb}MB"
    elif chkNet():
        alert = f"Error - localhost cannot be resolved to {chk_local_host_ip}"

    # alert if error raised:
    if alert:
        sendAlert(alert)
    else:
        print("system ok")


if __name__ == "__main__":
    main()
