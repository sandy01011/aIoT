from aIoTr.smpk import *
from env.env_noise_smpk import read_env
print(read_env())
print('calling smpk')
test = smpk(read_env(), 'noise')
test.load_env()
test.smpk_proxy()
print('smpk proxy started')
