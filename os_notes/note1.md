## Kernels and Processes

### kernel to user mode

1. new process
2. resume after an exception, interrupt or system call
3. switch to different process
4. user-level upcall

### mode switch on x86

user level process is running, exception or traps occurs:

1. save three key values. `stack pointer (ss && esp)`, `execution flags (eflags)` and `instruction pointer (cs && eip)`.
2. switch onto the kernel exception stack.
3. push three key values onto the new stack.
4. optionally save error code.
5. invoke the interrupt handler.
