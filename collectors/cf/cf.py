import diamond.collector
import subprocess


class RowContent:
    APP_START_LINE = 4
    METRIC_START_LINE = 12


class AppColContent:
    APP_INSTANCE = 0
    APP_STATUS = 1
    APP_CPU = 5
    APP_MEM_USED = 6
    APP_MEM_TOTAL = 8
    APP_DISK_USED = 9
    APP_DISK_TOTAL = 11


class AppsColContent:
    APP_NAME = 0
    APP_STATUS = 1
    APP_INSTANCE = 2
    APP_MEM = 3
    APP_DISK = 4
    APP_URL = 5


class CloudFoundryCollector(diamond.collector.Collector):
    apps = []

    def __init__(self, config=None, handlers=[], name=None, configfile=None):
        super(CloudFoundryCollector, self).__init__(config, handlers, name, configfile)
        if '*' in self.config['apps']:
            cmd = "cf apps"
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
            lines = result.splitlines()
            for i in range(RowContent.APP_START_LINE, len(lines)):
                self.apps.append(lines[i].split()[AppsColContent.APP_NAME])
        else:
            for app in self.config['apps']:
                self.apps.append(app)

    def get_default_config_help(self):
        config_help = super(CloudFoundryCollector, self).get_default_config_help()
        config_help.update({
            'metric': 'type of metric',
            'apps': 'application',
        })
        return config_help

    def get_default_config(self):
        config = super(CloudFoundryCollector, self).get_default_config()
        config.update({
            'metric': ['cpu', 'memory', 'disk'],
            'apps': ['*'],
        })
        return config

    def record_metric(self, line, app, metric_total, metric_used, metric, metrics):
        total = line.split()[metric_total]
        used = line.split()[metric_used]
        if 'G' in total:
            total = 1024 * float(total[:-1])  # convert to MB
        else:
            total = float(total[:-1])
        if 'G' in used:
            used = 1024 * float(used[:-1])  # convert to MB
        else:
            used = float(used[:-1])
        percent = used/total*100
        metrics['.'.join([app,
                          line.split()[AppColContent.APP_INSTANCE],
                          metric,
                          'total'])] = str(total)
        metrics['.'.join([app,
                          line.split()[AppColContent.APP_INSTANCE],
                          metric,
                          'used'])] = str(used)
        metrics['.'.join([app,
                          line.split()[AppColContent.APP_INSTANCE],
                          metric,
                          'percent'])] = str(percent)

    def collect(self):
        """
        Collector VMS stats
        """
        metrics = {}
        for app in self.apps:
            cmd = "cf app %s" % app
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
            lines = result.splitlines()
            for i in range(RowContent.METRIC_START_LINE, len(lines)):
                if 'cpu' in self.config['metric']:
                    metrics['.'.join([app,
                                      lines[i].split()[AppColContent.APP_INSTANCE],
                                      'cpu',
                                      'percent'])] = lines[i].split()[AppColContent.APP_CPU][:-1]
                if 'memory' in self.config['metric']:
                    self.record_metric(lines[i],
                                       app,
                                       AppColContent.APP_MEM_TOTAL,
                                       AppColContent.APP_MEM_USED,
                                       'memory',
                                       metrics)
                if 'disk' in self.config['metric']:
                    self.record_metric(lines[i],
                                       app,
                                       AppColContent.APP_DISK_TOTAL,
                                       AppColContent.APP_DISK_USED,
                                       'disk',
                                       metrics)

        for key in metrics:
            self.publish(key, metrics[key])


