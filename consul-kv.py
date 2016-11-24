#!/usr/bin/env python

'''
Retrieve consul k/v and add to inventory group based on hierarchy

/ansible/group/key/

/ansible/all/ec2_ami -> [all:vars]
                           ec2_ami=ami-960955e5

Supports strings, lists and dicts

'''

import os
import sys
import json
import argparse
import consul
import re
import yaml
import six

from six.moves import configparser

try:
    import json
except ImportError:
    import simplejson as json

key_prefix = 'ansible'


class ConsulInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()
        self.consul_host = '127.0.0.1'
        self.consul_port = 8500

        self.read_settings()

        self.consul = consul.Consul(
            self.consul_host,
            self.consul_port)

        # All ansible keys will be prefixed with /ansible
        idx, self.consul_keylist = self.consul.kv.get(key_prefix, recurse=True)

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.create_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print json.dumps(self.inventory);

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

    def read_settings(self):
        ''' Reads the settings from the consul.ini file '''
        if six.PY2:
            config = configparser.SafeConfigParser()
        else:
            config = configparser.ConfigParser()

        default_ini_path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)), 'consul.ini')

        ini_path = os.environ.get('CONSUL_INI_PATH', default_ini_path)
        config.read(ini_path)

        if config.has_option('consul', 'host'):
            self.consul_host = config.get('consul', 'host')

        if config.has_option('consul', 'port'):
            self.consul_port = config.get('consul', 'port')

    # Build Ansible inventory
    def create_inventory(self):
        vars_dict = {}

        #vars_dict['consul_keylist'] = self.consul_keylist

        for key_dict in self.consul_keylist:

            full_key = key_dict['Key']
            match = re.match("^"+key_prefix+"/(\w+)/(.*)", full_key)
            if match:
                group = match.group(1)
                key = match.group(2)

                if group not in vars_dict:
                    vars_dict[group] = {}
                    vars_dict[group]['vars'] = {}

                vars_dict[group]['vars'][key] = yaml.load(key_dict['Value'])

        return vars_dict



# Get the inventory.
ConsulInventory()
