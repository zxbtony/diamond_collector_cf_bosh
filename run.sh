#!/bin/bash

if [ "$1" = 'start' ] || [ "$#" == 0 ]; then
	export BOSH_TARGET_HOST="${BOSH_TARGET_HOST:=127.0.0.1}"
	export BOSH_ADMIN_USER="${BOSH_ADMIN_USER:=admin}"
	export BOSH_ADMIN_PWD="${BOSH_ADMIN_PWD:=admin}"
	export BOSH_ENABLE="${BOSH_ENABLE:=False}"
	export BOSH_METRIC="${BOSH_METRIC:=Persistent, Ephemeral, System, SwapUsage, MemoryUsage, CPU(User), CPU(Sys), CPU(Wait), Load}"
	export BOSH_DEPLOYMENTS="${BOSH_DEPLOYMENTS:=deployment,}"
	export CF_ENABLE="${CF_ENABLE:=False}"
	export CF_METRIC="${CF_METRIC:=cpu,memory,disk,}"
	export CF_APPS="${CF_APPS:=app,}"
	export CF_TARGET_HOST="${CF_TARGET_HOST:=http://localhost}"
	export CF_ADMIN_USER="${CF_ADMIN_USER:=admin}"
	export CF_ADMIN_PWD="${CF_ADMIN_PWD:=c1oudc0w}"
	export CF_ORG="${CF_ORG:=ORG}"
	export GRAPHITE_HOST="${GRAPHITE_HOST:=127.0.0.1}"
	export GRAPHITE_PREFIX="${GRAPHITE_PREFIX:=PERF}"
	export GRAPHITE_INTERVAL="${GRAPHITE_INTERVAL:=15}"
	
  
  echo BOSH_TARGET_HOST=$BOSH_TARGET_HOST
	echo BOSH_ADMIN_USER=$BOSH_ADMIN_USER
	echo BOSH_ADMIN_PWD=$BOSH_ADMIN_PWD
	echo BOSH_ENABLE=$BOSH_ENABLE
	echo BOSH_METRIC=$BOSH_METRIC
	echo BOSH_DEPLOYMENTS=$BOSH_DEPLOYMENTS
	echo CF_ENABLE=$CF_ENABLE
	echo CF_METRIC=$CF_METRIC
	echo CF_APPS=$CF_APPS
	echo CF_TARGET_HOST=$CF_TARGET_HOST
	echo CF_ADMIN_USER=$CF_ADMIN_USER
	echo CF_ADMIN_PWD=$CF_ADMIN_PWD
	echo CF_ORG=$CF_ORG
	echo GRAPHITE_HOST=$GRAPHITE_HOST
	echo GRAPHITE_PREFIX=$GRAPHITE_PREFIX
	echo GRAPHITE_INTERVAL=$GRAPHITE_INTERVAL
	
	python init.py
	mkdir -p /etc/diamond/collectors
	mkdir -p /var/log/diamond
	cp -r /collectors/cf /usr/share/diamond/collectors/
	cp -r /collectors/bosh /usr/share/diamond/collectors/
	cp -r /collectors/conf/* /etc/diamond/collectors/
	cp /usr/lib/python2.7/site-packages/etc/diamond/diamond.conf.example /etc/diamond/diamond.conf
	sed -i "s/enabled = False/enabled = $BOSH_ENABLE/g" /etc/diamond/collectors/BoshCollector.conf
	sed -i "s/metric =/metric = $BOSH_METRIC/g" /etc/diamond/collectors/BoshCollector.conf
	sed -i "s/deployments =/deployments = $BOSH_DEPLOYMENTS/g" /etc/diamond/collectors/BoshCollector.conf
	sed -i "s/enabled = False/enabled = $CF_ENABLE/g" /etc/diamond/collectors/CloudFoundryCollector.conf
	sed -i "s/metric =/metric = $CF_METRIC/g" /etc/diamond/collectors/CloudFoundryCollector.conf
	sed -i "s/apps =/apps = $CF_APPS/g" /etc/diamond/collectors/CloudFoundryCollector.conf
	sed -i "148s/# hostname = my_custom_hostname/hostname = Docker/g" /etc/diamond/diamond.conf
	sed -i "65s/host = 127.0.0.1/host = $GRAPHITE_HOST/g" /etc/diamond/diamond.conf
	sed -i "174s/# path_prefix = servers/path_prefix = $GRAPHITE_PREFIX/g" /etc/diamond/diamond.conf
	sed -i "185s/# interval = 300/interval = $GRAPHITE_INTERVAL/g" /etc/diamond/diamond.conf
  sed -i "192s/True/False/g" /etc/diamond/diamond.conf
  sed -i "195s/True/False/g" /etc/diamond/diamond.conf
  sed -i "198s/True/False/g" /etc/diamond/diamond.conf
  sed -i "201s/True/False/g" /etc/diamond/diamond.conf
  sed -i "204s/True/False/g" /etc/diamond/diamond.conf
  sed -i "207s/True/False/g" /etc/diamond/diamond.conf
	diamond
	tail -f /dev/null & wait	
fi

exec "$@"
