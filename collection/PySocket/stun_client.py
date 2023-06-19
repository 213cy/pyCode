# https://datatracker.ietf.org/doc/html/rfc3489
# https://github.com/jtriley/pystun/tree/develop/stun
# https://github.com/evilpan/P2P-Over-MiddleBoxes-Demo/blob/master/stun/classic_stun_client.py

import sys
import socket
import logging
import random


class MsgAttrs():
    # stun attributes
    AttrToVal = {
        'MappedAddress': '0001',
        'ResponseAddress': '0002',
        'ChangeRequest': '0003',
        'SourceAddress': '0004',
        'ChangedAddress': '0005',
        'Username': '0006',
        'Password': '0007',
        'MessageIntegrity': '0008',
        'ErrorCode': '0009',
        'UnknownAttribute': '000A',
        'ReflectedFrom': '000B',
        'XorOnly': '0021',
        'XorMappedAddress': '8020',
        'ServerName': '8022',
        'SecondaryAddress': '8050'
    }
    ValToAttr = dict(zip(AttrToVal.values(), AttrToVal.keys()))

    @classmethod
    def change_request(cls, change_addr=False, change_port=False):
        # padding is unnecessary
        v = 29*'0' + str(change_addr+0) + str(change_port+0) + '0'
        return cls({'ChangeRequest': format(int(v,2),'08x') })

    @classmethod
    def from_bytes(cls, buf, len_remain):
        assert len(buf) == len_remain
        retVal = {}
        cur = 0
        while len_remain > 0:
            attr_type = buf[cur:cur + 2].hex()
            attr_key = cls.ValToAttr.get(attr_type, 'attr_unknow')
            attr_len = int.from_bytes(buf[cur + 2:cur + 4], 'big')
            attr_value = buf[cur + 4:cur + 4 + attr_len].hex()
            retVal[attr_key] = attr_value
            cur = cur + 4 + attr_len
            len_remain = len_remain - (4 + attr_len)
        if len_remain != 0:
            raise ValueError('corrupted param buf')
        return cls(retVal)

    def __init__(self, dict_attr=None):
        if dict_attr is None:
            self.dict_attr = {}
        else:
            self.dict_attr = dict_attr
        # leng = 0
        # for k in self.dict_attr.values():
        #     leng = leng + 4 + int(len(k)/2)
        # self.byte_length = len

    def to_bytes(self):
        buf = b''
        for k,v in self.dict_attr.items():
            l = int(len(v)/2)
            buf = buf + bytes.fromhex(self.AttrToVal[k]+format(l,'04x')+v)
        return buf

    def parse_address(self, key):
        byte_addr = bytes.fromhex(self.dict_attr[key])
        ip = '.'.join(map(str, byte_addr[-4:]))   
        port =  int.from_bytes(byte_addr[2:-4], 'big') 
        return ip,port 

    def __str__(self):
        buf = ''
        for k,v in self.dict_attr.items():
            if k.endswith('Address'):
                ip, port =  self.parse_address(k)
                buf = buf + f'<Attr {k:15} | {ip}:{port}>\n'
            else:
                buf = buf + f'<Attr {k:15} | {v}>\n'
        return buf


class Message():
    # stun message types
    TypeToVal = {
        'BindRequestMsg': '0001',
        'BindResponseMsg': '0101',
        'BindErrorResponseMsg': '0111',
        'SharedSecretRequestMsg': '0002',
        'SharedSecretResponseMsg': '0102',
        'SharedSecretErrorResponseMsg': '0112'
    }
    ValToType = dict(zip(TypeToVal.values(), TypeToVal.keys()))

    @classmethod
    def from_bytes(cls, data):
        msgtyp_value = data[0:2].hex()
        msgtype = cls.ValToType.get(msgtyp_value, 'Msg_Unknow')
        if not msgtype == "BindResponseMsg":
            breakpoint()

        # length = int(data[2:4].hex(), 16)
        length = int.from_bytes(data[2:4],'big')
        assert len(data) == length + 20
        msgattrs = MsgAttrs.from_bytes(data[20:], length)
        tranid = data[4:20].hex()
        return cls( msgtype, msgattrs, tranid)

    def __init__(self, msgtype, msgattrs, tranid = None):
        self.type = msgtype
        self.type_value = self.TypeToVal[msgtype]
        self.attrs = msgattrs
        if tranid:
            self.tranid = tranid
        else:
            # self.transactionId =  randint(0, (1 << 128) - 1)
            self.tranid = ''.join(random.choices('0123456789abcdef', k=32))  # 128/4

    def to_bytes(self):
        body = self.attrs.to_bytes()
        head_str = self.TypeToVal[self.type]+format(len(body),'04x')+self.tranid
        head  = bytes.fromhex(head_str)
        return head + body

    def __str__(self):
        s = 5 * '-' + f'{self.type}[{self.type_value}]' + 5 * '-'
        return s + f'\n{str(self.attrs)}' + 50 * '-'


def send_and_recv(sock, stun_server, request):
    for entry in [3,2,1]:
        try:
            logging.debug(f'SEND: {request}')
            sock.sendto(request.to_bytes(), stun_server)
        except socket.gaierror:
            logging.warning(f"SEND: to {stun_server} fail({entry}) !")
            continue
        try:
            data, addr = sock.recvfrom(2048)
            response = Message.from_bytes(data)
            logging.debug(f'RECV: {response}')
            return response
        except socket.timeout as e:
            logging.warning(f'RECV: timeout({entry}) !')
    return None

def test(sock, stun_server, change_type=None):
    if change_type == 'ip_port':
        msgbody = MsgAttrs.change_request(True,True)
    elif change_type =='port':
        msgbody = MsgAttrs.change_request(False,True)
    else:
        msgbody = MsgAttrs()
    logging.info(f'connect to {stun_server[0]}:{stun_server[1]}, change : <{change_type}>')
    binding_request = Message('BindRequestMsg' ,msgbody)
    binding_response = send_and_recv(sock, stun_server, binding_request)

    logging.info(20*'='+f'     succeed: {bool(binding_response)}'+'\n')
    return binding_response


def test_nat(sock, stun_server, local_ip='0.0.0.0'):
    class NAT():
        PUBLIC      = 'The open Internet'
        UDP_BLOCKED = 'Firewall that blocks UDP'
        SYMMETRIC_UDP_FIREWALL = 'Firewall that allows UDP out, and responses have to come back to the source of the request'
        FULL_CONE = 'Full Cone NAT <1>'
        ADDR_RISTRICT  = '(Address) Rristrict Cone NAT <2>'
        PORT_RISTRICT  = 'Port Rristrict Cone NAT <3>'
        SYMMETRIC = 'Symmetric NAT <4>'

    resp = test(sock, stun_server)
    if resp is None:
        return NAT.UDP_BLOCKED
    resp_ip_port = test(sock, stun_server, 'ip_port')

    local_addr = sock.getsockname()
    logging.debug(f'local ip is {local_ip} | sockname is {local_addr}')
    mapped_addr = resp.attrs.parse_address('MappedAddress')
    logging.warning(f'          >>>>>> {mapped_addr} <<<<<<')
    ind = (mapped_addr == local_addr) + 2 * (resp_ip_port is not None)
    if ind:
        typ = (None, NAT.SYMMETRIC_UDP_FIREWALL, NAT.FULL_CONE, NAT.PUBLIC)[ind]
        return typ
    
    changed_addr = resp.attrs.parse_address('ChangedAddress')
    resp_new = test(sock, changed_addr)
    assert not (resp_new is None)
    # resp_port = test(sock, stun_server, 'port')
    resp_port = test(sock, (stun_server[0],changed_addr[1]), 'port')

    ma = resp.attrs.dict_attr['MappedAddress']
    ma_new = resp_new.attrs.dict_attr['MappedAddress']
    logging.debug(f'{ma} {ma_new}')
    if ma == ma_new:
        if resp_port is None:
            return NAT.PORT_RISTRICT
        else:
            return NAT.ADDR_RISTRICT
    else:
        return NAT.SYMMETRIC


STUN_SERVERS = [
    ('stun.voipstunt.com', 3478),
    ('stun.voipbuster.com', 3478),
    ('stun.pppan.net', 3478),
    ('stun.ekiga.net', 3478),
    ('stun.ideasip.com', 3478),
    ]

def main():
    if True:
        # logging.basicConfig(level=logging.DEBUG)
        logging.basicConfig(level=logging.INFO)
        # logging = logging.getLogger("pystun")
        logging.info(f'argument length: {len(sys.argv)-1}' )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # sock.bind(('0.0.0.0', 65432))
    
    try:
        # choose a stun server
        ntype = test_nat(sock, STUN_SERVERS[0], '0.0.0.0')
    except KeyboardInterrupt:
        sys.exit()
    sock.close()
    print('NAT_TYPE: ' + ntype)

# main()
if __name__ == '__main__':
    main()