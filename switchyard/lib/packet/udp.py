from switchyard.lib.packet.packet import PacketHeaderBase,Packet
import struct

'''
References:
    IETF RFC 768
'''

# FIXME: currently does *nothing* about checksum

class UDP(PacketHeaderBase):
    __slots__ = ['_srcport','_dstport','_len']
    __PACKFMT__ = '!HHHH'
    __MINSIZE__ = struct.calcsize(__PACKFMT__)

    def __init__(self):
        self.srcport = self.dstport = 0
        self._len = self.size()

    def size(self):
        return struct.calcsize(UDP.__PACKFMT__)

    def to_bytes(self):
        '''
        Return packed byte representation of the UDP header.
        '''
        return struct.pack(UDP.__PACKFMT__, self._srcport, self._dstport,
            self._len, 0)

    def from_bytes(self, raw):
        '''Return an Ethernet object reconstructed from raw bytes, or an
           Exception if we can't resurrect the packet.'''
        if len(raw) < UDP.__MINSIZE__:
            raise Exception("Not enough bytes ({}) to reconstruct an UDP object".format(len(raw)))
        fields = struct.unpack(UDP.__PACKFMT__, raw[:UDP.__MINSIZE__])
        self._srcport = fields[0]
        self._dstport = fields[1]
        self._len = fields[2]
        return raw[UDP.__MINSIZE__:]

    def __eq__(self, other):
        return self.srcport == other.srcport and \
            self.dstport == other.dstport

    @property
    def srcport(self):
        return self._srcport

    @property
    def dstport(self):
        return self._dstport

    @srcport.setter
    def srcport(self,value):
        self._srcport = value

    @dstport.setter
    def dstport(self,value):
        self._dstport = value

    def __str__(self):
        return '{} {}->{}'.format(self.__class__.__name__, self.srcport, self.dstport)

    def next_header_class(self):
        return None

    def pre_serialize(self, raw, pkt, i):
        self._len = self.size() + len(raw)
