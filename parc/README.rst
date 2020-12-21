========================================================================
README: PARC Instruction Set Simulator
========================================================================

A Pydgin description of the PARC ISA which implements an ISS capable of
executing ELF binaries.

------------------------------------------------------------------------
Building PARC Applications
------------------------------------------------------------------------

Prerequisition
--------------------
This requires ``pydgin-parc-xcc`` (``maven-sys-xcc``) cross-compiler.
Goto pydgin-parc-xcc and read instructions how to compile the xcc.

ASM Test Case
--------------------
   % cd $parc_home/asm_tests
   % mkdir build
   % cd build
   % ../configure --host=maven
   % make
   % cd $parc_home

   Run the ISS simulation:
   % python ./parc-sim.py --test -d insts,rf asm_tests/build/parcv1-gcd

   Or debug with ipdb:
   % ipdb ./parc-sim.py --test -d insts,rf asm_tests/build/parcv1-gcd

   Read more from on how to build GCD customized instruction.
   https://github.com/kevinyuan/pydgin-parc-xcc/blob/master/README

Building C Application Without System Calls
--------------------

This repository should contain a copy of the simplified ubmarks (without
system calls) used in ECE4750. To compile them for PARC, first ensure
you have the maven cross compiler installed (available on the BRG
servers) and execute the following::

  $ cd ~/vcd/git-brg/pydgin/ubmark-nosyscalls
  $ mkdir build-
  $ cd build-
  $ ../configure --host=maven
  $ make ubmark-vvadd


Building C Application With System Calls
------------------

The PARC ISS is also capable of executing more complicated benchmarks
with system calls. To build them, you must checkout and compile the
maven-apps-misc repository from Github::

  $ cd ~/vc/git-brg
  $ git clone git@github.com:cornell-brg/maven-app-misc.git
  $ mkdir ~/vc/git-brg/maven-app-misc/build-
  $ cd ~/vc/git-brg/maven-app-misc/build-
  $ ../configure --host=maven
  $ make

------------------------------------------------------------------------
Executing the PARC ISS
------------------------------------------------------------------------

With Python
-----------

The PARC ISS can be executed directly with a Python interpreter. While
slow, it provides a faster code-test-debug cycle than the compiled
interpreter. To execute, run::

  $ python parc-sim.py ../ubmark-nosyscalls/build-/ubmark-vvadd

With C and JIT
--------------

Using the RPython translation toolchain, we can convert the PARC ISS
into a C executable with a JIT-optimizing compiler. To perform the
translation (takes ~5 minutes), run::

  $ PYTHONPATH='/work/bits0/dml257/hg-pypy/pypy' python \
    /work/bits0/dml257/hg-pypy/pypy/rpython/translator/goal/translate.py \
    --opt=jit \
    -sim.py

To execute, run::

  $ pydgin-parc-jit ../ubmark-nosyscalls/build-/ubmark-vvadd

We can also generate a C executable *without* the JIT-optimizing
compiler by removing the ``--opt=jit`` flag.  While typically not as
high-performance as the JIT-enabled executable, compilation times are
much faster (30 seconds).

