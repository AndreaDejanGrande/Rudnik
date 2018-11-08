import binascii
import halfnode
import struct
import util
import settings
import lib.logger
log = lib.logger.get_logger('coinbasetx')

#if settings.COINDAEMON_Reward == 'POW':
class CoinbaseTransactionPOW(halfnode.CTransaction):
    '''Construct special transaction used for coinbase tx.
    It also implements quick serialization using pre-cached
    scriptSig template.'''
    
    extranonce_type = '>Q'
    extranonce_placeholder = struct.pack(extranonce_type, int('f000000ff111111f', 16))
    extranonce_size = struct.calcsize(extranonce_type)

    def __init__(self, timestamper, coinbaser, value, flags, height, data):
        super(CoinbaseTransactionPOW, self).__init__()
        log.debug("Got to CoinBaseTX")
        #self.extranonce = 0
        
        if len(self.extranonce_placeholder) != self.extranonce_size:
            raise Exception("Extranonce placeholder don't match expected length!")

        tx_in = halfnode.CTxIn()
        tx_in.prevout.hash = 0L
        tx_in.prevout.n = 2**32-1
        tx_in._scriptSig_template = (
            util.ser_number(height) + binascii.unhexlify(flags) + util.ser_number(int(timestamper.time())) + \
            chr(self.extranonce_size),
            util.ser_string(coinbaser.get_coinbase_data() + data)
        )
                
        tx_in.scriptSig = tx_in._scriptSig_template[0] + self.extranonce_placeholder + tx_in._scriptSig_template[1]
    
        tx_out = halfnode.CTxOut()
        tx_out.nValue = value
        tx_out.scriptPubKey = coinbaser.get_script_pubkey()

        if settings.COINDAEMON_TX == 'yes':
            self.strTxComment = "vDinar Pool"
        self.vin.append(tx_in)
        self.vout.append(tx_out)
    
        # Two parts of serialized coinbase, just put part1 + extranonce + part2 to have final serialized tx
        self._serialized = super(CoinbaseTransactionPOW, self).serialize().split(self.extranonce_placeholder)

    def set_extranonce(self, extranonce):
        if len(extranonce) != self.extranonce_size:
            raise Exception("Incorrect extranonce size")
        
        (part1, part2) = self.vin[0]._scriptSig_template
        self.vin[0].scriptSig = part1 + extranonce + part2
#elif settings.COINDAEMON_Reward == 'POS':
class CoinbaseTransactionPOS(halfnode.CTransaction):
    '''Construct special transaction used for coinbase tx.
    It also implements quick serialization using pre-cached
    scriptSig template.'''
    
    extranonce_type = '>Q'
    extranonce_placeholder = struct.pack(extranonce_type, int('f000000ff111111f', 16))
    extranonce_size = struct.calcsize(extranonce_type)

    def __init__(self, timestamper, coinbaser, value, flags, height, data, ntime):
        super(CoinbaseTransactionPOS, self).__init__()
        log.debug("Got to CoinBaseTX")
        #self.extranonce = 0
        
        if len(self.extranonce_placeholder) != self.extranonce_size:
            raise Exception("Extranonce placeholder don't match expected length!")

        tx_in = halfnode.CTxIn()
        tx_in.prevout.hash = 0L
        tx_in.prevout.n = 2**32-1
        tx_in._scriptSig_template = (
            util.ser_number(height) + binascii.unhexlify(flags) + util.ser_number(int(timestamper.time())) + \
            chr(self.extranonce_size),
            util.ser_string(coinbaser.get_coinbase_data() + data)
        )
                
        tx_in.scriptSig = tx_in._scriptSig_template[0] + self.extranonce_placeholder + tx_in._scriptSig_template[1]
    
        tx_out = halfnode.CTxOut()
        tx_out.nValue = value
        tx_out.scriptPubKey = coinbaser.get_script_pubkey()
       
        self.nTime = ntime 
        if settings.COINDAEMON_SHA256_TX == 'yes':
            self.strTxComment = "http://github.com/ahmedbodi/stratum-mining"
        self.vin.append(tx_in)
        self.vout.append(tx_out)
        
        # Two parts of serialized coinbase, just put part1 + extranonce + part2 to have final serialized tx
        self._serialized = super(CoinbaseTransactionPOS, self).serialize().split(self.extranonce_placeholder)

    def set_extranonce(self, extranonce):
        if len(extranonce) != self.extranonce_size:
            raise Exception("Incorrect extranonce size")
        
        (part1, part2) = self.vin[0]._scriptSig_template
        self.vin[0].scriptSig = part1 + extranonce + part2
#else:
class CoinbaseTransaction(halfnode.CTransaction):
    '''Construct special transaction used for coinbase tx.
    It also implements quick serialization using pre-cached
    scriptSig template.'''
    
    extranonce_type = '>Q'
    extranonce_placeholder = struct.pack(extranonce_type, int('f000000ff111111f', 16))
    extranonce_size = struct.calcsize(extranonce_type)

    def __init__(self, timestamper, coinbaser, value, flags, height, data, ntime):
        super(CoinbaseTransaction, self).__init__()
        log.debug("Got to CoinBaseTX")
        #self.extranonce = 0
        
        if len(self.extranonce_placeholder) != self.extranonce_size:
            raise Exception("Extranonce placeholder don't match expected length!")

        tx_in = halfnode.CTxIn()
        tx_in.prevout.hash = 0L
        tx_in.prevout.n = 2**32-1
        tx_in._scriptSig_template = (
            util.ser_number(height) + binascii.unhexlify(flags) + util.ser_number(int(timestamper.time())) + \
            chr(self.extranonce_size),
            util.ser_string(coinbaser.get_coinbase_data() + data)
        )
                
        tx_in.scriptSig = tx_in._scriptSig_template[0] + self.extranonce_placeholder + tx_in._scriptSig_template[1]
    
        tx_out = halfnode.CTxOut()
        tx_out.nValue = value
        tx_out.scriptPubKey = coinbaser.get_script_pubkey()
       
        self.nTime = ntime 
        self.vin.append(tx_in)
        self.vout.append(tx_out)
    
        # Two parts of serialized coinbase, just put part1 + extranonce + part2 to have final serialized tx
        self._serialized = super(CoinbaseTransaction, self).serialize().split(self.extranonce_placeholder)

    def set_extranonce(self, extranonce):
        if len(extranonce) != self.extranonce_size:
            raise Exception("Incorrect extranonce size")
        
        (part1, part2) = self.vin[0]._scriptSig_template
        self.vin[0].scriptSig = part1 + extranonce + part2
# vDinar only, second coinbase transaction
class CoinbaseDonationsTransaction(halfnode.CTransaction):
    '''Construct special vDinar donationstransaction used
    for coinbase tx. It also implements quick serialization
    using pre-cached scriptSig template.'''
    
    extranonce_type = '>Q'
    extranonce_placeholder = struct.pack(extranonce_type, int('f000000ff111111f', 16))
    extranonce_size = struct.calcsize(extranonce_type)

    def __init__(self, timestamper, coinbaser, value, flags, height, data):
        super(CoinbaseDonationsTransaction, self).__init__()
        log.debug("Got to donations' CoinBaseTX")
        #self.extranonce = 0
        
        if len(self.extranonce_placeholder) != self.extranonce_size:
            raise Exception("Extranonce placeholder don't match expected length!")
        
        donations_tx_in = halfnode.CTxIn()
        donations_tx_in.prevout.hash = 0L
        donations_tx_in.prevout.n = 2**32-1
        donations_tx_in._scriptSig_template = (
            util.ser_number(height) + binascii.unhexlify(flags) + util.ser_number(int(timestamper.time())) + \
            chr(self.extranonce_size),
            util.ser_string(coinbaser.get_coinbase_data() + data)
        )
        donations_tx_in.scriptSig = donations_tx_in._scriptSig_template[0] + self.extranonce_placeholder + donations_tx_in._scriptSig_template[1]

        donations_tx_out = halfnode.CTxOut()
        donations_tx_out.nValue = value / 49
        donations_tx_out.scriptPubKey = coinbaser.get_donations_script_pubkey()
    
        self.vin.append(donations_tx_in)
        self.vout.append(donations_tx_out)

        # Two parts of serialized coinbase, just put part1 + extranonce + part2 to have final serialized tx
        self._serialized = super(CoinbaseDonationsTransaction, self).serialize().split(self.extranonce_placeholder)

    def set_extranonce(self, extranonce):
        if len(extranonce) != self.extranonce_size:
            raise Exception("Incorrect extranonce size")

        #vDinar only, set extra nonce to donations' signature
        (donations_part1, donations_part2) = self.vin[0]._scriptSig_template
        self.vin[0].scriptSig = donations_part1 + extranonce + donations_part2
