#!/usr/bin/env python3

import os
import argparse
import shlex
import subprocess

tool_path = "./map2check "
# default args
extra_tool = "timeout 895s "
command_line = extra_tool + tool_path

# Options
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", help="Prints Map2check's version", action='store_true')
parser.add_argument("-p", "--propertyfile", help="Path to the property file")
#parser.add_argument("-c", "--validatece", help="Validating counterexample", action='store_true')
parser.add_argument("benchmark", nargs='?', help="Path to the benchmark")

args = parser.parse_args()

# ARG options
version = args.version
property_file = args.propertyfile
validate_ce = True
benchmark = args.benchmark

if version == True:
  os.system(tool_path + "--version")
  exit(0)

if validate_ce == True:
  print("Enabled counterexample validation ...")

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
else:
  # We don't support termination
  print("Unsupported Property")
  exit(1)


# Set options
if is_memsafety:
  command_line += " --memtrack --generate-witness "
elif is_memcleanup:
  command_line += " --memcleanup-property --generate-witness "
elif is_reachability:
  command_line += " --smt-solver yices2 --add-invariants --target-function --generate-witness "
elif is_overflow:
  command_line += " --check-overflow --generate-witness "

print("Verifying with MAP2CHECK ")
# Call MAP2CHECK
command_line += benchmark
print("Command: " + command_line)

args = shlex.split(command_line)

p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(stdout, stderr) = p.communicate()

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

    # Validating counterexample
    if validate_ce == True:
      output_tmp_ce = open('ce.tmp', 'w')
      output_tmp_ce.write(stdout.decode())
      output_tmp_ce.close()
      command_line_ce = "../utils/ce-validation.py ce.tmp"
      args = shlex.split(command_line_ce)

      # checkout same var name!!!!
      p_ce = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      (stdout_ce, stderr_ce) = p_ce.communicate()

      # Parse counterexample output
      if b'[ERROR-CE]' in stdout_ce:
        result_tmp_ce = open('result_ce.tmp', 'w+')
        result_tmp_ce.write("ERROR counterexample in " + benchmark + "\n")
        result_tmp_ce.close()


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
      exit(0)

    if overflow_offset in stdout.decode():
      print("FALSE_OVERFLOW")
      exit(0)


if "VERIFICATION SUCCEEDED" in stdout.decode():
  print("TRUE")
  exit(0)

print("UNKNOWN")
exit(0)
