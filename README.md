DNSBL
=====

Simple backend for periodically query DNS-based Blackhole Lists and send alert report via email.

Backends should handle hundreds of providers in seconds, thanks to [Gevent](http://www.gevent.org/).


Usage
-----
```bash
pip install -r requirements.txt
python /opt/base_dnsbl_check.py -u $USERNAME -p $PASSWORD -s $SERVER -r $RECIPIENT -a $ADDRESS -P $PORT -t $TIMEOUT
```
