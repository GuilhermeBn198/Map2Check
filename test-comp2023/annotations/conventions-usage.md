# conventions and usage of the map2check tool

## conventions for the testcomp functions inside the test files

__VERIFIER_error(): For checking reachability we use the function __VERIFIER_error(). The verification tool can assume the following implementation:
void __VERIFIER_error() { abort(); }
Hence, a function call __VERIFIER_error() never returns and in the function __VERIFIER_error() the program terminates.

__VERIFIER_assume(expression): A verification tool can assume that a function call __VERIFIER_assume(expression) has the following meaning: If 'expression' is evaluated to '0', then the function loops forever, otherwise the function returns (no side effects). The verification tool can assume the following implementation:
void __VERIFIER_assume(int expression) { if (!expression) { LOOP: goto LOOP; }; return; }

__VERIFIER_nondet_X(): In order to model nondeterministic values, the following functions can be assumed to return an arbitrary value of the indicated type: __VERIFIER_nondet_X() with X in {bool, char, int, int128, float, double, loff_t, long, longlong, pchar, pthread_t, sector_t, short, size_t, u32, uchar, uint, uint128, ulong, ulonglong, unsigned, ushort} (no side effects, pointer for void *, etc.). The test tool can assume that the functions are implemented according to the following template:
X __VERIFIER_nondet_X() { X val; return val; }

__VERIFIER_atomic_begin(): For modeling an atomic execution of a sequence of statements in a multi-threaded run-time environment, those statements can be placed between two function calls __VERIFIER_atomic_begin() and __VERIFIER_atomic_end() (deprecated but still valid: those statements can be placed in a function whose name matches __VERIFIER_atomic_). The testers are instructed to assume that the execution between those calls is not interrupted. The two calls need to occur within the same control-flow block; nesting or interleaving of those function calls is not allowed.

malloc(), free(): We assume that the functions malloc and alloca always return a valid pointer, i.e., the memory allocation never fails, and function free always deallocates the memory and makes the pointer invalid for further dereferences.
