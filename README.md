# Diamond Collector for Bosh and CF

## Environment Variable
#### BOSH_TARGET_HOST
  -Default = 127.0.0.1
#### BOSH_ADMIN_USER
  -Default = admin
#### BOSH_ADMIN_PWD
  -Default = admin
#### BOSH_ENABLE
  -Default = True
#### BOSH_METRIC
  -Default = "Persistent,Ephemeral,System,SwapUsage,MemoryUsage,CPU(User),CPU(Sys),CPU(Wait),Load"
#### BOSH_DEPLOYMENTS
  -Default = cf_perfsh4
#### CF_ENABLE
  -Default = True
#### CF_METRIC
  -Default = cpu,memory,disk,
#### CF_APPS
  -Default = "app"
  -NOTE: * for all apps
#### CF_TARGET_HOST
  -Default = http://localhost
#### CF_ADMIN_USER
  -Default = admin 
#### CF_ADMIN_PWD
  -Default = c1oudc0w
#### CF_ORG
  -Default = ORG
#### GRAPHITE_HOST
  -Default = 127.0.0.1
#### GRAPHITE_PREFIX
  -Default = CF_BOSH
#### GRAPHITE_INTERVAL
  -Default = 15

## Usage
* Run Diamond Collector
```sh
docker run --rm -d \
	-e BOSH_TARGET_HOST=127.0.0.1 \
	-e BOSH_ADMIN_USER=admin \
	-e BOSH_ADMIN_PWD=admin \
	-e BOSH_ENABLE=True \
	-e BOSH_METRIC="Persistent,Ephemeral,System,SwapUsage,MemoryUsage,CPU(User),CPU(Sys),CPU(Wait),Load" \
	-e BOSH_DEPLOYMENTS=cf_perfsh4, \
	-e CF_ENABLE=True \
	-e CF_METRIC=cpu,memory,disk, \
	-e CF_APPS=cms-ngisspace, \
	-e CF_TARGET_HOST=http://localhost\
	-e CF_ADMIN_USER=admin \
	-e CF_ADMIN_PWD=c1oudc0w \
	-e CF_ORG=ORG \
	-e GRAPHITE_HOST=127.0.0.1 \
	-e GRAPHITE_PREFIX=CF_BOSH \
	-e GRAPHITE_INTERVAL=15 \
	zxbtony/diamond_collector_cf_bosh
```
