import subprocess
import re 
import json

import numpy as np
import time
import pathlib
def queryYesNo(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

class PartitionExecutor:


  def __init__(self, partitions_path, bin_path):

    self.bin_path = bin_path
    self.partitions_path = partitions_path

    with  open (partitions_path + '/heterogeneous/hardware.json', 'r') as m_file:
      
      print('Reading mappings file ')
      self.mapping = json.load(m_file)
      print('There are %d solutions'%len(self.mapping['solutions']))

  def programDevice(self, xclbin):

    shell_command = 'xbutil program -p ' + xclbin
    run = subprocess.run(shell_command, shell=True)
    if run.returncode != 0:
      print("Failed to program the device with " + xclbin)
    return run.returncode
  
  def __validate_solution__(self, solution):
    cores = 0
    try:
      cores = solution['cores']
    except KeyError:
      raise KeyError('Invalid solution format: ' + 
        json.dumps(solution, indent=4) + "\n missing \'cores\' entry")

    sol_number = 0
    try:
      sol_number = solution['index']
    except KeyError:
      try:
        sol_number = solution['sol_number']
      except KeyError:
        raise KeyError('Invalid solution format: ' + 
          json.dumps(solution, indent=4) + "\n missing \'sol_number\' entry")

    unique_index = 0
    try:
      unique_index = solution['hash_index']
    except KeyError:
      try:
        unique_index = solution['index']
      except KeyError:
        raise KeyError('Invalid solution format: ' + 
          json.dumps(solution, indent=4) + "\n missing \'index\' entry")
    
    return (cores, sol_number, unique_index)

  def runAllSolutions(self, output, extra_args, dry_run=False):
    
    self.mapping['extra_args'] = extra_args
    for sol in self.mapping['solutions']:
      (cores, sol_number, unique_index) = self.__validate_solution__(sol)
      config_path = pathlib.Path(
        self.partitions_path + '/heterogeneous/' + str(cores) + '/multicore/config_' + str(sol_number) + '.xml'
      ).resolve()
      if config_path.is_file():
        args = '--cfile=' + str(config_path) + ' ' + extra_args
        perf = self.runSolution(sol, args, dry_run)
        if perf != None:
          print("""frames = {frames} time = {time} fps = {fps:4.4f} trips = {trips}""".format(
            frames = perf['frames'],
            time = perf['time'],
            fps = perf['frames'] / perf['time'],
            trips = perf['trips']
          ))
          sol['perf'] = perf
          with open(output, 'w') as jd:
            jd.write(json.dumps(self.mapping, indent = 4))
        else:
          print("""could not measure performance!""")
      else:
        print(""" 
        config file {} does not exits!
        """.format(str(config_path)))
    
   
    
    
  def runSolution(self, solution, args='', dry_run=False):

    (cores, sol_number, unique_index) = self.__validate_solution__(solution)
  
    binary_path = pathlib.Path(self.bin_path.replace("@INDEX@", str(unique_index)))

    if binary_path.is_file() == False:
      print("Binary file " + str(binary_path) + " does not exits")
      return None
    
    program_name = binary_path.name
    
    

    exec_dir = pathlib.Path(binary_path).parent
    
    xclbin_dir = exec_dir / ('xclbin/' +  program_name + '_kernel.hw.xclbin')


    shell_command = './' + str(program_name) + ' ' + args


    print("""
    ----------------------------------------------------------------------------
    Directory:
      {dir}
    Command:
      {cmd}
    ============================================================================"""
    .format(dir=str(exec_dir), cmd=shell_command))
    err = self.programDevice(str(xclbin_dir))
    if err != 0:
      print("Could not program the device! Erorr code is " + str(err))
      return None
    
    if not dry_run:
      run = subprocess.run(shell_command, shell=True, stdout=subprocess.PIPE, cwd=str(exec_dir))
      if run.returncode != 0:
        print(""" 
        Failed to execute:
        {cmd}
        in direcotory {dir}, program returned {code}

        {err}
        """.format(cmd=shell_command, dir=exec_dir, code=run.returncode, err=run.stdout.decode("utf-8")))
        return None
      else:
        regex_perf = re.compile(r'(\d*) images in (\d*\.\d*) seconds: (\d*\.\d*) FPS')
        regex_plink = re.compile(r'PLink trip count = (\d*)')
        perf = {'frames' : None, 'trips' : None, 'time' : None}
        for ln in run.stdout.decode("utf-8").split('\n'):
          # print(ln)
          matches = regex_perf.match(ln)
          if (matches != None):
            perf['frames'] = int(matches.group(1))
            perf['time'] = float(matches.group(2))
          matches = regex_plink.match(ln)
          if (matches != None):
            perf['trips'] = int(matches.group(1))
        
        return perf
    else:
      return None
      



if __name__ == "__main__":

  
  executor = PartitionExecutor('pwr_fixed', 'unique_@INDEX@_3.3/bin/Top_RVC_Decoder')
  # executor.runSolution({'index' : 0, 'sol_number' : 0, 'cores' : 1}, '--i=foreman_qcif_30.bit --l=10  --d=1048576 --use-default-depth', True)
  executor.runAllSolutions( 'runs.json', '--i=foreman_qcif_30.bit --l=100  --d=1048576 --use-default-depth', False)

