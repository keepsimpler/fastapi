from app.core.cfcasign import CFCASignature

def test_create_cfca_signature():
    cfca_signature = CFCASignature()
    assert isinstance(cfca_signature, CFCASignature)

def test_get_sign():
    cfca_signature = CFCASignature()
    source_data = 'a=1&b=2'
    pfx_file_name = 'JFJT.pfx'
    res, signed_data = cfca_signature.get_sign(algorithm='rsa',
                            source_data=source_data,
                            pfx_file_name=pfx_file_name,
                            pfx_password='111111',  # TODO: config
                            hash_alg='sha-1')
    assert res==0