import time

from django_rq import job

@job('default', timeout=6)
def test_queue():
    print('job started')
    time.sleep(5)
    print('job finished')