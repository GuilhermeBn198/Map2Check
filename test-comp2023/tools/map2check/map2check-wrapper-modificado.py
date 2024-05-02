#!/usr/bin/env python3

import os
import argparse
import shlex
import subprocess
import importlib

tool_path = "./map2check "
# default args
extra_tool = "timeout 897s "
command_line = extra_tool + tool_path
timemapsplit = "895"

# Options
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", help="Prints Map2check's version", action='store_true')
parser.add_argument("-p", "--propertyfile", help="Path to the property file")
parser.add_argument("benchmark", nargs='?', help="Path to the benchmark")

args = parser.parse_args()

# ARG options
version = args.version
property_file = args.propertyfile
benchmark = args.benchmark

if version == True:
  os.system(tool_path + "--version")
  exit(0)

if property_file is None:
  print("Please, specify a property file")
  exit(1)

if benchmark is None:
  print("Please, specify a benchmark to verify")
  exit(1)

is_memsafety 	= False
is_reachability = False
is_overflow 	= False
is_memcleanup   = False
is_cov_call = False # testcomp coverage_error_calls category
is_cov_branches = False # testcomp coverage_branches category

f = open(property_file, 'r')
property_file_content = f.read()

if "CHECK( init(main()), LTL(G valid-free) )" in property_file_content:
  is_memsafety = True
elif "CHECK( init(main()), LTL(G valid-deref) )" in property_file_content:
  is_memsafety = True
elif "CHECK( init(main()), LTL(G valid-memtrack) )" in property_file_content:
  is_memsafety = True
elif "CHECK( init(main()), LTL(G valid-memcleanup) )" in property_file_content:
  is_memcleanup = True
elif "CHECK( init(main()), LTL(G ! overflow) )" in property_file_content:
  is_overflow = True
elif "CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )" in property_file_content:
  is_reachability = True
elif "COVER( init(main()), FQL(COVER EDGES(@CALL(reach_error))) )" in  property_file_content:
  is_cov_call = True # linha adicionada para o Testcomp (coverage-error-calls)
elif "COVER( init(main()), FQL(COVER EDGES(@DECISIONEDGE)) )" in property_file_content:
  is_cov_branches = True # linha adicionada para o Testcomp (coverage-branches)
else:
  # We don't support termination
  print("Unsupported Property")
  exit(1)


# Set options
command_line_bkp = ""

if is_memsafety:
  command_line += " --timeout "+timemapsplit+" --memtrack --smt-solver yices2 --generate-witness "
  
elif is_memcleanup:
  command_line += " --timeout "+timemapsplit+" --memcleanup-property --smt-solver yices2 --generate-witness "
  
elif is_reachability:
  command_line_bkp = command_line + " --timeout "+timemapsplit+" --smt-solver yices2 --target-function --generate-witness "
  command_line += " --timeout "+timemapsplit+" --smt-solver yices2 --add-invariants --target-function --generate-witness " 
  ## propriedade originalmente sendo verificada antes de fazermos as modificações
  
elif is_overflow:
  command_line += " --timeout "+timemapsplit+" --check-overflow --smt-solver yices2 --generate-witness "
  
elif is_cov_call:
  command_line_bkp = command_line + " --timeout "+timemapsplit+" --smt-solver yices2 --target-function --generate-witness "
  command_line += " --timeout "+timemapsplit+" --smt-solver yices2 --target-function --generate-witness "   
  ## linha adicionada para o Testcomp (coverage-error-calls)
  
elif is_cov_branches:
  command_line_bkp = command_line + " --timeout "+timemapsplit+"  --check-overflow --smt-solver yices2 --target-function --generate-witness "
  command_line += " --timeout "+timemapsplit+" --smt-solver yices2 --target-function --generate-witness "   # linha adicionada para o Testcomp (coverage-branches)

print("Verifying with MAP2CHECK ")

# Call MAP2CHECK
command_line += benchmark
command_line_bkp += benchmark

print("Command: " + command_line)
args = shlex.split(command_line)
p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(stdout, stderr) = p.communicate()
print(stdout)
# print(stderr)

# Check invariant conflict
if b'failed external call: __map2check_main__' in stderr:
  if is_reachability:
    args = shlex.split(command_line_bkp)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    # print(stdout)
    # print(stderr)


# Parse output
if b'Timed out' in stdout:
  print("Timed out")
  exit(1)


# Error messages
free_offset     = "\tFALSE-FREE: Operand of free must have zero pointer offset"
deref_offset    = "\tFALSE-DEREF: Reference to pointer was lost"
memtrack_offset = "\tFALSE-MEMTRACK"
memcleanup_offset = "\tFALSE-MEMCLEANUP"
target_offset   = "\tFALSE: Target Reached"
overflow_offset = "\tOVERFLOW"

if "VERIFICATION FAILED" in stdout.decode():
    if free_offset in stdout.decode():
      print("FALSE_FREE")
      exit(0)

    if deref_offset in stdout.decode():
      print("FALSE_DEREF")
      exit(0)

    if memtrack_offset in stdout.decode():
      print("FALSE_MEMTRACK")
      exit(0)

    if memcleanup_offset in stdout.decode():
      print("FALSE_MEMCLEANUP")
      exit(0)

    if target_offset in stdout.decode():
      print("FALSE")
      importlib.import_module('data_extractor')
      exit(0)

    if overflow_offset in stdout.decode():
      print("FALSE_OVERFLOW")
      exit(0)


if "VERIFICATION SUCCEEDED" in stdout.decode():
  print("TRUE")
  importlib.import_module('data_extractor')
  exit(0)

print("UNKNOWN")
exit(0)
