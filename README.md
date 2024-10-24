# wano_expert
## Purpose of this repository
This repository contains WaNos (Workflow active Nodes) for the expert usage of Nanomatch scientific software. Further information on the software and the installation in connection with WaNos are available at the [Nanomatch documentation page](http://docs.nanomatch.de/)

## Connection to standard WaNo repository
The [standard WaNo repository](https://github.com/NanomatchGmbH/wano) contains WaNos for standard use cases of the Nanomatch software, as applied for example in the Nanoscope environment (see the [Nanoscope documentation for details](https://nanoscope.readthedocs.io/nanoscope.readthedocs.io)). In order to use both standard and expert WaNos, clone both repositories and link WaNos from one folder into the other:

``` 
git clone git@github.com:NanomatchGmbH/wano.git
git clone git@github.com:NanomatchGmbH/wano_expert.git 
cd wano
ln -s ../wano_expert/* .
cd ..
```