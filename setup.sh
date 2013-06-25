export PYTHONPATH=$PWD:$PYTHONPATH
#use python2.6 from CMSSW
if [ -e "/net/software_cms/slc5_ia32_gcc434/external/python/2.6.4-cms2/etc/profile.d/init.sh" ]; then
  source /net/software_cms/slc5_ia32_gcc434/external/python/2.6.4-cms2/etc/profile.d/init.sh
  source /net/software_cms/slc5_ia32_gcc434/external/openssl/0.9.7m/etc/profile.d/init.sh
fi
