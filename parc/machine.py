#=======================================================================
# machine.py
#=======================================================================

from pydgin.machine import Machine
from pydgin.storage import RegisterFile
from pydgin.utils   import r_uint

#-----------------------------------------------------------------------
# State
#-----------------------------------------------------------------------
class State( Machine ):
  _virtualizable_ = ['pc', 'num_insts']
  def __init__( self, memory, debug, reset_addr=0x400):
    Machine.__init__(self, memory, RegisterFile(), debug, reset_addr=reset_addr )

    # parc special
    self.src_ptr  = 0
    self.sink_ptr = 0
    self.gcd_ncycles = 0

    # indicate if this is running a self-checking test
    self.testbin  = False

    # executable name
    self.exe_name = ""

    # syscall stuff... TODO: should this be here?
    self.breakpoint = r_uint( 0 )

  def fetch_pc( self ):
    return self.pc
