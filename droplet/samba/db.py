# FIXME put this at droplet-samba packaging level
import sys
sys.path.append('/usr/lib/python2.7/dist-packages')

from samba.credentials import Credentials
from samba.samdb import SamDB
from samba.auth import system_session
from samba.provision.common import setup_add_ldif

import samba

from droplet.sudo import root


def samdb_connect():
    """
    Open and return a SamDB connection
    """
    with root():
        lp = samba.param.LoadParm()
    lp.load("/etc/samba/smb.conf")
    creds = Credentials()
    creds.guess(lp)
    session = system_session()
    samdb = SamDB("/var/lib/samba/private/sam.ldb",
                  session_info=session,
                  credentials=creds,
                  lp=lp)
    return samdb


def load_schema(ldif_file):
    """
    Load a schema from the given file into the SamDB
    """
    samdb = samdb_connect()
    dn = samdb.domain_dn()

    samdb.transaction_start()
    try:
        setup_add_ldif(samdb, ldif_file, {
            "DOMAINDN": dn,
        })
    except:
        samdb.transaction_cancel()
        raise

    samdb.transaction_commit()
