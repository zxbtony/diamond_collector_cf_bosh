import diamond.collector
import re
import subprocess

class RowContent:
    INFORM = 0
    DIRECTORTASK = 1
    TASKNUM = 2
    SEPARATE_1 = 6
    HEADER_1 = 7
    HEADER_2 = 8
    SEPARATE_2 = 9
    METRIC_START_LINE = 10
    METRIC_LAST_LINE = -4


class BoshCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(BoshCollector, self).get_default_config_help()
        config_help.update({
            'metric': 'type of metric',
            'deployments': 'Deployments',
        })
        return config_help

    def get_default_config(self):
        config = super(BoshCollector, self).get_default_config()
        config.update({
            'metric': ['Persistent', 'Ephemeral', 'System',
                       'SwapUsage', 'MemoryUsage', 'CPU(User)',
                       'CPU(Sys)', 'CPU(Wait)', 'Load'],
            'deployments': ['cf_perfsh4'],
        })
        return config

    def record_metric(self, lines, metrics, metric, category, col):
        for i in range(RowContent.METRIC_START_LINE, len(lines) + RowContent.METRIC_LAST_LINE):
            cols = "".join(lines[i].split()).split("|")
            if 'n/a' not in cols[col]:
                if '%' in cols[col]:
                    metrics['.'.join([cols[1].split("(")[0], category, metric])] = cols[col].split("%")[0]
                else:
                    metrics['.'.join([cols[1].split("(")[0], category, metric])] = cols[col]

    def collect(self):
        """
        Collector VMS stats
        """
        metrics = {}
        for deployment in self.config['deployments']:
            command = "bosh vms --vitals %s" % deployment
            result = subprocess.Popen(command,
                                      shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT).stdout.read()
            lines = result.splitlines()
            for metric in self.config['metric']:
                if metric in ['Persistent', 'Ephemeral', 'System']:
                    category = 'disk'
                elif metric in ['MemoryUsage', 'SwapUsage']:
                    category = 'memory'
                elif 'CPU' in metric:
                    category = 'CPU'
                elif metric in 'Load':
                    category = 'load'
                if 'CPU' not in metric and 'Load' not in metric:
                    col = "".join(lines[RowContent.HEADER_1].split()).split("|").index(metric)
                    self.record_metric(lines, metrics, metric, category, col)
                elif 'CPU' in metric:
                    metric = re.split("\W+", metric)[1]
                    col = "".join(lines[RowContent.HEADER_2].split()).split("|").index(metric)
                    self.record_metric(lines, metrics, metric, category, col)
                elif 'Load' in metric:
                    col = "".join(lines[RowContent.HEADER_1].split()).split("|").index(metric)
                    for i in range(RowContent.METRIC_START_LINE, len(lines) + RowContent.METRIC_LAST_LINE):
                        cols = "".join(lines[i].split()).split("|")
                        metrics['.'.join([cols[1].split("(")[0], category, 'avg01'])] = cols[col].split(",")[0]
                        metrics['.'.join([cols[1].split("(")[0], category, 'avg05'])] = cols[col].split(",")[1]
                        metrics['.'.join([cols[1].split("(")[0], category, 'avg15'])] = cols[col].split(",")[2]
        for key in metrics:
            self.publish(key, metrics[key])
