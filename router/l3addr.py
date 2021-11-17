from icecream import ic
from utils import maskToHostMask, maskToInt

# Disable debugging output
ic.disable()


class L3Addr:

    def __init__(self, val):
        '''Accept values as str (e.g., "10.111.12.13") or 32-bit int.
        Store in both formats (for convenience).'''
        if isinstance(val, str):
            self._as_str = val
            parts = val.split('.')
            if len(parts) != 4:
                raise ValueError("str val must have the form x.y.z.w")

            res = self.ipToInt(parts)
            self._as_int = res

        elif isinstance(val, int):
            if val > 2 ** 32 - 1:
                raise ValueError("val does not fit in 32 bits")
            self._as_int = val
            self._as_str = ""
            for i in [24, 16, 8]:
                part = val // (2 ** i)
                self._as_str += str(part) + "."
                val -= part * (2 ** i)
            self._as_str = self._as_str + str(val % 2 ** 8)
            
        else:
            raise TypeError("val must be a int or str")

    # converts param to an int
    def as_int(self):
        return self._as_int

    # converts param to a string
    def as_str(self):
        return self._as_str

    # returns the network part of the ipAdress as an int
    def network_part_as_int(self, mask_numbits: int) -> int:
        mask = maskToInt(mask_numbits)
        return self._as_int & mask

    # returns the network part of the ipAdress as a Layer 3 address
    def network_part_as_L3Addr(self, mask_numbits: int):
        return L3Addr(self.network_part_as_int(mask_numbits))

    # returns the host part of the ipAdress as a Layer 3 address
    def host_part_as_L3Addr(self, mask_numbits: int):
        """ function returns a host as an IPv4 int"""
        mask = maskToHostMask(mask_numbits)
        host_mask = self._as_int & mask
        return L3Addr(host_mask)

    # equality operation
    def __eq__(self, other):
        return self._as_int == other.as_int()

    # returns object as a string
    def __str__(self):
        return f'{self._as_str}'

    def is_bcast(self) -> bool:
        return '255' in self.as_str()   ## needs to be tested

    def ipToInt(self, ipAddrParts):
        """ stackoverflow.com/questions/9590965/convert-an-ip-string-to-a-number-and-vice-versa
        
        convert parts (list of strings) into one integer value in variable res 
        
        """
        result = (int(ipAddrParts[0]) << 24) + (int(ipAddrParts[1]) << 16) +\
                (int(ipAddrParts[2]) << 8) + (int(ipAddrParts[3]))

        return result

if __name__ == "__main__":
    a = L3Addr("10.11.12.13")
    assert a.as_str() == "10.11.12.13"
    assert a.as_int() == 168496141
    assert a.is_bcast()

    try:
        L3Addr(2**32)
        assert "Failed to check value that is too large"
    except ValueError as v:
        pass    

    assert L3Addr(168496141).as_str() == "10.11.12.13"

    assert a.network_part_as_L3Addr(24).as_str() == "10.11.12.0"
    assert a.network_part_as_L3Addr(16).as_str() == "10.11.0.0"
    assert a.network_part_as_L3Addr(20).as_str() == "10.11.0.0"

    assert (a.network_part_as_int(8) ==
            0b0000_1010_0000_0000_0000_0000_0000_0000)

    assert a.host_part_as_L3Addr(16).as_str() == "0.0.12.13"
    
    b = L3Addr("0.0.0.0")
    assert b.as_str() == "10.11.12.13"
    assert b.as_int() == 168496141

    print('L3Addr: all tests passed!')
