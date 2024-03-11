from typing import Mapping
from subprocess import run, PIPE, STDOUT
from app.models.sign import SignKind
import re
import os
from app.settings import logger


_info = re.compile(r'^(?P<type>(pub|sec))\s*(?P<algo>\w+)/(?P<id>[a-zA-Z0-9]+).*(?P<started>[\d-]{10}).*\[expires: (?P<expire>[\d-]{10})\]$')
_finger = re.compile(r'[A-Z0-9]{1,4}')

def list_keys(public: bool = True) -> list[Mapping[str, str]]:
    output = run(['gpg', '-k' if public else '-K', '--keyid-format=long'], stdout=PIPE).stdout.decode('utf-8')
    keys = []

    for _key_info in output.split('\n\n')[:-1]:

        info, finger, cred, *_ = filter(lambda x: '---' not in x and '/.gnupg/' not in x, _key_info.split('\n'))

        keys.append(
            {**_info.search(info).groupdict(), 
             'fingerprint': ' '.join(_finger.findall(finger.strip())),
             'credentials': re.sub(r'uid\s+', '', cred)}
        )
        
    return keys

def export(user: str, ascii: bool = True) -> bytes:
    cmd = ['--batch', '--export', '0x'+user]
    if ascii:
        cmd = ['gpg', '-a'] + cmd
    else: 
        cmd = ['gpg'] + cmd
    output = run(cmd, stdout=PIPE, stderr=STDOUT)

    return output.stdout

def sign(path: str, user: str, pin: str, kind: SignKind|str = SignKind.detached, 
         ascii: bool = False, fixFileExists: bool = False) -> Mapping[str, str]:
    cmd = ['gpg', '--batch', '--no-tty', '--pinentry-mode=loopback', 
                  '--passphrase-fd', '0', '-u', user, '-o', path+'.sig']
    if ascii:
        cmd.append('-a')
    cmd += ['--sign', str(kind), path]
    p = run(cmd, input=pin.encode('utf-8'), stdout=PIPE, stderr=PIPE)

    output, err = p.stdout.decode('utf-8'), p.stderr.decode('utf-8')

    if 'Bad passphrase' in err:
        raise PermissionError("Bad passphrase")
    if 'File exists' in err:
        if not fixFileExists:
            raise FileExistsError
        os.remove(path+'.sig')
        sign(path, user, pin, kind, ascii)

    logger.debug(output)
    logger.debug(err)
    if err:
        raise SystemError(err)
    
    if output == '':
        return {'success': True, 'path': path, 'singed_path': path+'.sig'}

    

def verify(sig_path: str, path: str|None = None) -> Mapping[str, str]:
    cmd = ['gpg', '--verify', sig_path]

    if path:
        cmd.append(path)
    p = run(cmd, stdout=PIPE, stderr=STDOUT)

    output = p.stdout.decode('utf-8')

    if 'No such file' in output:
        raise FileNotFoundError
    if 'no valid' in output:
        raise TypeError
    if 'No public key' in output or p.returncode != 0:
        return {'success': False, 'result': output}
    
    return {'success': True, 'result': output}
