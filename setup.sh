export PYTHONPATH=$PWD:$PYTHONPATH
#use python2.6 from CMSSW
if [ -e "/net/software_cms/$SCRAM_ARCH/external/python/2.6.4-cms16/etc/profile.d/init.sh" ]; then
  source /net/software_cms/$SCRAM_ARCH/external/python/2.6.4-cms16/etc/profile.d/init.sh
  source /net/software_cms/$SCRAM_ARCH/external/openssl/0.9.8e-cms5/etc/profile.d/init.sh
fi
