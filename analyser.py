import sys
import time
import logging
import re
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logs_from_folder = 'Input'
logs_to_folder_file_name = './Output/time_taken.log'

class On_file(FileSystemEventHandler):
  def on_created(self, event):
    super(On_file, self).on_created(event)

    time_stamp_regex = r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}'
    time_taken_regex = r'\d+$'
    
    match_list = []
    elem_sum = 0
    incident_setting = 10
    coverage = 3
    incident_on = False

    if not event.is_directory:
      with open(event.src_path, "r") as file:
        for line in file:
          match_line = []
          for time_stamp_match in re.finditer(time_stamp_regex, line, re.S):
            time_stamp = time_stamp_match.group()
            match_line.append(datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S'))
          for time_taken_match in re.finditer(time_taken_regex, line, re.S):
            time_taken = time_taken_match.group()
            match_line.append(int(time_taken))
          if len(match_line) > 0: # exclude lines where nothing was found
            match_list.append(match_line)
      
            for elem in match_list:
              elem_sum = elem_sum + elem[1]
            time_taken_average = elem_sum / len(match_list)
      
            if time_taken_average >= incident_setting and incident_on == False:
              logging.info("%s long answer start %s" % (match_list[0][0], match_list[0][1]))
              incident_on = True
      
            if time_taken_average < incident_setting and incident_on == True:
              logging.info('%s long answer end %s' % (match_list[0][0], match_list[1][1]))
              incident_on = False
      
            if len(match_list) > coverage:
              match_list.pop(0)
              elem_sum = 0


if __name__ == "__main__":
    logging.basicConfig(filename=logs_to_folder_file_name,
                        level=logging.INFO,
                        format='%(message)s')
    event_handler = On_file()
    observer = Observer()
    observer.schedule(event_handler, logs_from_folder)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
