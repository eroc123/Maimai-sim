#main.py
import os
import threading
import sys
import logging
from webbrowser import get
import psutil, platform
import time
import math
logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.DEBUG)

if sys.platform == "linux" or sys.platform == "linux2":
    PYTHON = 'python'
elif sys.platform == "darwin":
    logging.critical('Does not have support for MAC OS machines')
    logging.info('Exiting...')
    exit()
elif sys.platform == "win32":
    PYTHON = 'py'

#Directory Layout
'''
FOLDER LAYOUT
<root>
|- <assets>
|   |- <charts>
|   |- <images>
|   |   |- hold-double.png
|   |   |- hold.png
|   |   |- star-note-break.png
|   |   |- star-note-double.png
|   |   |- star-note.png
|   |   |- tap-note-double.png
|   |   |- tap-note-single-break.png
|   |   |- tap-note-single.png
|   |- gui.py
|   |- loader.py
|   |- maimai-sim.py
|   |- sprites.py
|   |- inputKeys.py
|- main.py
'''

def check_memory():
    usage = psutil.Process().memory_info().rss / (1024 * 1024)
    logging.debug(f'Currently using {usage} MB of memory')

def debug():
    while True:
        check_memory()
        time.sleep(5)
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_platform_info():
    uname = platform.uname()
    logging.info(f"System: {uname.system}")
    logging.info(f"Node Name: {uname.node}")
    logging.info(f"Release: {uname.release}")
    logging.info(f"Version: {uname.version}")
    logging.info(f"Machine: {uname.machine}")
    logging.info(f"Processor: {uname.processor}")

    logging.info("="*40+ "CPU Info"+ "="*40)
    # number of cores
    logging.info("Physical cores:"+ str(psutil.cpu_count(logical=False)))
    logging.info("Total cores:"+ str(psutil.cpu_count(logical=True)))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    logging.info(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    logging.info(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    logging.info(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    # CPU usage
    logging.info("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        logging.info(f"Core {i}: {percentage}%")
    logging.info(f"Total CPU Usage: {psutil.cpu_percent()}%")
    logging.info("="*40+ "Memory Information"+ "="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    logging.info(f"Total: {get_size(svmem.total)}")
    logging.info(f"Available: {get_size(svmem.available)}")
    logging.info(f"Used: {get_size(svmem.used)}")
    logging.info(f"Percentage: {svmem.percent}%")
    logging.info("="*20+ "SWAP"+ "="*20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    logging.info(f"Total: {get_size(swap.total)}")
    logging.info(f"Free: {get_size(swap.free)}")
    logging.info(f"Used: {get_size(swap.used)}")
    logging.info(f"Percentage: {swap.percent}%")

if __name__ == '__main__':
    logging.debug('Starting new Run')
    get_platform_info()
    threading.Thread(target = debug, daemon=True).start()
    os.system(f'{PYTHON} ./assets/maimai-sim.py') #blocking process


#Simai documentation
#Simai chart button starts from 1 to 8
#BPM is in brackets, and may change throughout the song
#note fraction is written before notes are played, if there is no new fraction, it is kept the same
#note fraction is written in amount of notes per bar
#hold notes are in the format 'startbutton slidetype endbutton [x:y]'
#where
#x is note fraction
#y is amount of bars



# Actrual formula used for speed
# speed = (ln(speed) + 1) * raduis * 0.01

# speed = distance/time

# for chart note format check loader.py
