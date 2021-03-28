# -*- coding: utf-8 -*-
"""
TTN Gateway Plugin.

Return gateway statistics from the packet forwarder
"""
from json import load
import collectd

gw_stat_file = '/var/ttn/loragwstat.json'
last_time = None
# We synch on the gateway stat_interval
stat_interval = 30


def config(config):
    global gw_stat_file

    for node in config.children:
        key = node.key.lower()
        val = node.values[0]

        if key == 'gatewaystatfile':
            gw_stat_file = val
            collectd.info('ttn_gw plugin: Using stat file %s' % gw_stat_file)


def dispatch(type_instance, value, new_data):
    v = collectd.Values(plugin='ttn_gw',
                        type='gauge',
                        type_instance=type_instance)
    v.dispatch(values=[value if new_data else 0])


def read():
    global gw_stat_file, last_time

    # Read the stats file
    try:
        with open(gw_stat_file, 'r') as f:
            gw_stats = load(f)
    except IOError, e:
        collectd.error('ttn_gw plugin: Cannot read gateway stats file %s' % e)
        collectd.error('ttn_gw plugin: (gateway not runing?)')
        return
    except ValueError:
        collectd.error('ttn_gw plugin: Cannot parse gateway stats file')
        return

    new_data = False
    if last_time != gw_stats['time']:
        new_data = True
        last_time = gw_stats['time']

    current = gw_stats['current']
    keys = (
        'up_radio_packets_received',
        'up_radio_packets_crc_good',
        'up_radio_packets_crc_bad',
        'up_radio_packets_crc_absent',
        'up_radio_packets_dropped',
        'up_radio_packets_forwarded',
        'down_radio_packets_succes',
        'down_radio_packets_failure',
        'down_radio_packets_collision_packet',
        'down_radio_packets_collision_beacon',
        'down_radio_packets_too_early',
        'down_radio_packets_too_late',
        'down_beacon_packets_queued',
        'down_beacon_packets_send',
        'down_beacon_packets_rejected'
    )
    for key in keys:
        dispatch(key, current[key], new_data)


collectd.register_config(config)
collectd.register_read(read, stat_interval)
