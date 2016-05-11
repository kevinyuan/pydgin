#!/usr/bin/python

# TLB Model with LRU replacement policy

class PageTable:
  # Constructor for the class.
  # The default page table size is 8
  def __init__(self, table_size = 8):
    self.hits = 0
    self.misses = 0
    self.tlb = {}
    self.pg_table_size = table_size

  #Routine to mask the LSB bits
  def mask_lsb(self, value):
    return ((value & 0xFFFFFC00) >> 10)

  # Routine to populate the page table with pg_table_size entries
  def populate_table(self, key):
    self.tlb.clear()
    self.tlb.setdefault(key, [])
    self.tlb[key].append(1)  #valid bit
    self.tlb[key].append(1)  #Physical Address
    self.tlb[key].append(1)  #Number to keep track for LRU
    for x in range(1, self.pg_table_size):
      self.tlb.update({key + x : [1, x*10, 1]})


  def update_table(self, key):
    key_addresses = self.tlb.keys()
    stale_key = key_addresses[0]
    old_index = self.tlb.get(key_addresses[0])
    highest_index = old_index

    for delete_key in self.tlb.keys():
      if ( self.tlb.get(delete_key)[2] < old_index[2]):
        stale_key = delete_key
        old_index = self.tlb.get(delete_key)

    del self.tlb[stale_key]
    self.tlb.update({key : [1, 1000, 1]})
    return

  def tlb_lookup(self, searchkey):
    key_addresses = self.tlb.keys()
    #First time, hash will be empty, so returns an empty list
    if not key_addresses:
      self.misses += 1
      self.populate_table(searchkey)
      return
    elif (searchkey not in key_addresses):
      self.update_table(searchkey) #Update the page table now using LRU
      self.misses += 1
    else:
      #There is a hit and hence LRU value needs to be updated accordingly.
      valid = self.tlb.get(searchkey)[0]
      phys_addr = self.tlb.get(searchkey)[1]
      lru_value = self.tlb.get(searchkey)[2]
      lru_value += 1
      del self.tlb[searchkey]
      self.tlb.update({searchkey : [valid, phys_addr, lru_value]})
      self.hits += 1
    return

def main():
  sample_table = PageTable(8)
  sample_table.tlb_lookup(sample_table.mask_lsb(0x00222220))
  sample_table.tlb_lookup(sample_table.mask_lsb(0x00222221))
  sample_table.tlb_lookup(sample_table.mask_lsb(0x10000020))
  sample_table.tlb_lookup(sample_table.mask_lsb(0x10000020))
  sample_table.tlb_lookup(sample_table.mask_lsb(0x023445020))
  print "Hits=" + str(sample_table.hits)
  print "Misses=" + str(sample_table.misses)
    
if __name__ == "__main__":
  main()

