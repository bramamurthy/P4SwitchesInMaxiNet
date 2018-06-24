#!/usr/bin/python2

import os
import sys
import json


my_out_str=""

template_lines_tmp = [
'"ADD_LINE"',         1,        '{',
'"ADD_LINE"',         5,        '"__meta__": {',
'"ADD_LINE"',         9,        '"version": [',
'"ADD_LINE"',         13,        '2,',
'"ADD_LINE"',         13,        '0',
'"ADD_LINE"',         9,        ']',
'"ADD_LINE"',         5,        '},',
'"ADD_LINE"',         5,        '"header_types": [',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "standard_metadata_t",',
'"ADD_LINE"',         13,        '"id": 0,',
'"ADD_LINE"',         13,        '"fields": [',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"ingress_port",',
'"ADD_LINE"',         21,        '9',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"packet_length",',
'"ADD_LINE"',         21,        '32',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"egress_spec",',
'"ADD_LINE"',         21,        '9',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"egress_port",',
'"ADD_LINE"',         21,        '9',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"egress_instance",',
'"ADD_LINE"',         21,        '32',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"instance_type",',
'"ADD_LINE"',         21,        '32',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"clone_spec",',
'"ADD_LINE"',         21,        '32',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"_padding",',
'"ADD_LINE"',         21,        '5',
'"ADD_LINE"',         17,        ']',
'"ADD_LINE"',         13,        '],',
'"ADD_LINE"',         13,        '"length_exp": null,',
'"ADD_LINE"',         13,        '"max_length": null',
'"ADD_LINE"',         9,        '},',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "ethernet_t",',
'"ADD_LINE"',         13,        '"id": 1,',
'"ADD_LINE"',         13,        '"fields": [',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"dstAddr",',
'"ADD_LINE"',         21,        '48',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"srcAddr",',
'"ADD_LINE"',         21,        '48',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"etherType",',
'"ADD_LINE"',         21,        '16',
'"ADD_LINE"',         17,        ']',
'"ADD_LINE"',         13,        '],',
'"ADD_LINE"',         13,        '"length_exp": null,',
'"ADD_LINE"',         13,        '"max_length": null',
'"ADD_LINE"',         9,        '},',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "ipv4_t",',
'"ADD_LINE"',         13,        '"id": 2,',
'"ADD_LINE"',         13,        '"fields": [',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"version",',
'"ADD_LINE"',         21,        '4',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"ihl",',
'"ADD_LINE"',         21,        '4',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"diffserv",',
'"ADD_LINE"',         21,        '8',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"totalLen",',
'"ADD_LINE"',         21,        '16',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"identification",',
'"ADD_LINE"',         21,        '16',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"flags",',
'"ADD_LINE"',         21,        '3',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"fragOffset",',
'"ADD_LINE"',         21,        '13',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"ttl",',
'"ADD_LINE"',         21,        '8',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"protocol",',
'"ADD_LINE"',         21,        '8',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"hdrChecksum",',
'"ADD_LINE"',         21,        '16',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"srcAddr",',
'"ADD_LINE"',         21,        '32',
'"ADD_LINE"',         17,        '],',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"dstAddr",',
'"ADD_LINE"',         21,        '32',
'"ADD_LINE"',         17,        ']',
'"ADD_LINE"',         13,        '],',
'"ADD_LINE"',         13,        '"length_exp": null,',
'"ADD_LINE"',         13,        '"max_length": null',
'"ADD_LINE"',         9,        '},',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "routing_metadata_t",',
'"ADD_LINE"',         13,        '"id": 3,',
'"ADD_LINE"',         13,        '"fields": [',
'"ADD_LINE"',         17,        '[',
'"ADD_LINE"',         21,        '"nhop_ipv4",',
'"ADD_LINE"',         21,        '32',
'"ADD_LINE"',         17,        ']',
'"ADD_LINE"',         13,        '],',
'"ADD_LINE"',         13,        '"length_exp": null,',
'"ADD_LINE"',         13,        '"max_length": null',
'"ADD_LINE"',         9,        '}',
'"ADD_LINE"',         5,        '],',
'"ADD_LINE"',         5,        '"headers": [',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "standard_metadata",',
'"ADD_LINE"',         13,        '"id": 0,',
'"ADD_LINE"',         13,        '"header_type": "standard_metadata_t",',
'"ADD_LINE"',         13,        '"metadata": true',
'"ADD_LINE"',         9,        '},',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "ethernet",',
'"ADD_LINE"',         13,        '"id": 1,',
'"ADD_LINE"',         13,        '"header_type": "ethernet_t",',
'"ADD_LINE"',         13,        '"metadata": false',
'"ADD_LINE"',         9,        '},',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "ipv4",',
'"ADD_LINE"',         13,        '"id": 2,',
'"ADD_LINE"',         13,        '"header_type": "ipv4_t",',
'"ADD_LINE"',         13,        '"metadata": false',
'"ADD_LINE"',         9,        '},',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "routing_metadata",',
'"ADD_LINE"',         13,        '"id": 3,',
'"ADD_LINE"',         13,        '"header_type": "routing_metadata_t",',
'"ADD_LINE"',         13,        '"metadata": true',
'"ADD_LINE"',         9,        '}',
'"ADD_LINE"',         5,        '],',
'"ADD_LINE"',         5,        '"header_stacks": [],',
'"ADD_LINE"',         5,        '"parsers": [',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "parser",',
'"ADD_LINE"',         13,        '"id": 0,',
'"ADD_LINE"',         13,        '"init_state": "start",',
'"ADD_LINE"',         13,        '"parse_states": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"name": "start",',
'"ADD_LINE"',         21,        '"id": 0,',
'"ADD_LINE"',         21,        '"parser_ops": [],',
'"ADD_LINE"',         21,        '"transition_key": [],',
'"ADD_LINE"',         21,        '"transitions": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "default",',
'"ADD_LINE"',         29,        '"value": null,',
'"ADD_LINE"',         29,        '"mask": null,',
'"ADD_LINE"',         29,        '"next_state": "parse_ethernet"',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"name": "parse_ethernet",',
'"ADD_LINE"',         21,        '"id": 1,',
'"ADD_LINE"',         21,        '"parser_ops": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"op": "extract",',
'"ADD_LINE"',         29,        '"parameters": [',
'"ADD_LINE"',         33,        '{',
'"ADD_LINE"',         37,        '"type": "regular",',
'"ADD_LINE"',         37,        '"value": "ethernet"',
'"ADD_LINE"',         33,        '}',
'"ADD_LINE"',         29,        ']',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        '],',
'"ADD_LINE"',         21,        '"transition_key": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "field",',
'"ADD_LINE"',         29,        '"value": [',
'"ADD_LINE"',         33,        '"ethernet",',
'"ADD_LINE"',         33,        '"etherType"',
'"ADD_LINE"',         29,        ']',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        '],',
'"ADD_LINE"',         21,        '"transitions": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "hexstr",',
'"ADD_LINE"',         29,        '"value": "0x0800",',
'"ADD_LINE"',         29,        '"mask": null,',
'"ADD_LINE"',         29,        '"next_state": "parse_ipv4"',
'"ADD_LINE"',         25,        '},',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "default",',
'"ADD_LINE"',         29,        '"value": null,',
'"ADD_LINE"',         29,        '"mask": null,',
'"ADD_LINE"',         29,        '"next_state": null',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"name": "parse_ipv4",',
'"ADD_LINE"',         21,        '"id": 2,',
'"ADD_LINE"',         21,        '"parser_ops": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"op": "extract",',
'"ADD_LINE"',         29,        '"parameters": [',
'"ADD_LINE"',         33,        '{',
'"ADD_LINE"',         37,        '"type": "regular",',
'"ADD_LINE"',         37,        '"value": "ipv4"',
'"ADD_LINE"',         33,        '}',
'"ADD_LINE"',         29,        ']',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        '],',
'"ADD_LINE"',         21,        '"transition_key": [],',
'"ADD_LINE"',         21,        '"transitions": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "default",',
'"ADD_LINE"',         29,        '"value": null,',
'"ADD_LINE"',         29,        '"mask": null,',
'"ADD_LINE"',         29,        '"next_state": null',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '}',
'"ADD_LINE"',         13,        ']',
'"ADD_LINE"',         9,        '}',
'"ADD_LINE"',         5,        '],',
'"ADD_LINE"',         5,        '"parse_vsets": [],',
'"ADD_LINE"',         5,        '"deparsers": [',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "deparser",',
'"ADD_LINE"',         13,        '"id": 0,',
'"ADD_LINE"',         13,        '"order": [',
'"ADD_LINE"',         17,        '"ethernet",',
'"ADD_LINE"',         17,        '"ipv4"',
'"ADD_LINE"',         13,        ']',
'"ADD_LINE"',         9,        '}',
'"ADD_LINE"',         5,        '],',
'"ADD_LINE"',         5,        '"meter_arrays": [],',
'"ADD_LINE"',         5,        '"actions": [',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "rewrite_mac",',
'"ADD_LINE"',         13,        '"id": 0,',
'"ADD_LINE"',         13,        '"runtime_data": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"name": "smac",',
'"ADD_LINE"',         21,        '"bitwidth": 48',
'"ADD_LINE"',         17,        '}',
'"ADD_LINE"',         13,        '],',
'"ADD_LINE"',         13,        '"primitives": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"op": "modify_field",',
'"ADD_LINE"',         21,        '"parameters": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "field",',
'"ADD_LINE"',         29,        '"value": [',
'"ADD_LINE"',         33,        '"ethernet",',
'"ADD_LINE"',         33,        '"srcAddr"',
'"ADD_LINE"',         29,        ']',
'"ADD_LINE"',         25,        '},',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "runtime_data",',
'"ADD_LINE"',         29,        '"value": 0',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '}',
'"ADD_LINE"',         13,        ']',
'"ADD_LINE"',         9,        '},',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "_drop",',
'"ADD_LINE"',         13,        '"id": 1,',
'"ADD_LINE"',         13,        '"runtime_data": [],',
'"ADD_LINE"',         13,        '"primitives": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"op": "drop",',
'"ADD_LINE"',         21,        '"parameters": []',
'"ADD_LINE"',         17,        '}',
'"ADD_LINE"',         13,        ']',
'"ADD_LINE"',         9,        '},',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "set_nhop",',
'"ADD_LINE"',         13,        '"id": 2,',
'"ADD_LINE"',         13,        '"runtime_data": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"name": "nhop_ipv4",',
'"ADD_LINE"',         21,        '"bitwidth": 32',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"name": "port",',
'"ADD_LINE"',         21,        '"bitwidth": 9',
'"ADD_LINE"',         17,        '}',
'"ADD_LINE"',         13,        '],',
'"ADD_LINE"',         13,        '"primitives": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"op": "modify_field",',
'"ADD_LINE"',         21,        '"parameters": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "field",',
'"ADD_LINE"',         29,        '"value": [',
'"ADD_LINE"',         33,        '"routing_metadata",',
'"ADD_LINE"',         33,        '"nhop_ipv4"',
'"ADD_LINE"',         29,        ']',
'"ADD_LINE"',         25,        '},',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "runtime_data",',
'"ADD_LINE"',         29,        '"value": 0',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"op": "modify_field",',
'"ADD_LINE"',         21,        '"parameters": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "field",',
'"ADD_LINE"',         29,        '"value": [',
'"ADD_LINE"',         33,        '"standard_metadata",',
'"ADD_LINE"',         33,        '"egress_spec"',
'"ADD_LINE"',         29,        ']',
'"ADD_LINE"',         25,        '},',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "runtime_data",',
'"ADD_LINE"',         29,        '"value": 1',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"op": "add_to_field",',
'"ADD_LINE"',         21,        '"parameters": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "field",',
'"ADD_LINE"',         29,        '"value": [',
'"ADD_LINE"',         33,        '"ipv4",',
'"ADD_LINE"',         33,        '"ttl"',
'"ADD_LINE"',         29,        ']',
'"ADD_LINE"',         25,        '},',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "hexstr",',
'"ADD_LINE"',         29,        '"value": "-0x1"',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '}',
'"ADD_LINE"',         13,        ']',
'"ADD_LINE"',         9,        '},',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "set_dmac",',
'"ADD_LINE"',         13,        '"id": 3,',
'"ADD_LINE"',         13,        '"runtime_data": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"name": "dmac",',
'"ADD_LINE"',         21,        '"bitwidth": 48',
'"ADD_LINE"',         17,        '}',
'"ADD_LINE"',         13,        '],',
'"ADD_LINE"',         13,        '"primitives": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"op": "modify_field",',
'"ADD_LINE"',         21,        '"parameters": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "field",',
'"ADD_LINE"',         29,        '"value": [',
'"ADD_LINE"',         33,        '"ethernet",',
'"ADD_LINE"',         33,        '"dstAddr"',
'"ADD_LINE"',         29,        ']',
'"ADD_LINE"',         25,        '},',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"type": "runtime_data",',
'"ADD_LINE"',         29,        '"value": 0',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '}',
'"ADD_LINE"',         13,        ']',
'"ADD_LINE"',         9,        '}',
'"ADD_LINE"',         5,        '],',
'"ADD_LINE"',         5,        '"pipelines": [',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "ingress",',
'"ADD_LINE"',         13,        '"id": 0,',
'"ADD_LINE"',         13,        '"init_table": "_condition_0",',
'"ADD_LINE"',         13,        '"tables": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"name": "ipv4_lpm",',
'"ADD_LINE"',         21,        '"id": 0,',
'"ADD_LINE"',         21,        '"match_type": "lpm",',
'"ADD_LINE"',         21,        '"type": "simple",',
'"ADD_LINE"',         21,        '"max_size": 1024,',
'"ADD_LINE"',         21,        '"with_counters": false,',
'"ADD_LINE"',         21,        '"direct_meters": null,',
'"ADD_LINE"',         21,        '"support_timeout": false,',
'"ADD_LINE"',         21,        '"key": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"match_type": "lpm",',
'"ADD_LINE"',         29,        '"target": [',
'"ADD_LINE"',         33,        '"ipv4",',
'"ADD_LINE"',         33,        '"dstAddr"',
'"ADD_LINE"',         29,        '],',
'"ADD_LINE"',         29,        '"mask": null',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        '],',
'"ADD_LINE"',         21,        '"actions": [',
'"ADD_LINE"',         25,        '"set_nhop",',
'"ADD_LINE"',         25,        '"_drop"',
'"ADD_LINE"',         21,        '],',
'"ADD_LINE"',         21,        '"next_tables": {',
'"ADD_LINE"',         25,        '"set_nhop": "forward",',
'"ADD_LINE"',         25,        '"_drop": "forward"',
'"ADD_LINE"',         21,        '},',
'"ADD_LINE"',         21,        '"base_default_next": "forward"',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"name": "forward",',
'"ADD_LINE"',         21,        '"id": 1,',
'"ADD_LINE"',         21,        '"match_type": "exact",',
'"ADD_LINE"',         21,        '"type": "simple",',
'"ADD_LINE"',         21,        '"max_size": 512,',
'"ADD_LINE"',         21,        '"with_counters": false,',
'"ADD_LINE"',         21,        '"direct_meters": null,',
'"ADD_LINE"',         21,        '"support_timeout": false,',
'"ADD_LINE"',         21,        '"key": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"match_type": "exact",',
'"ADD_LINE"',         29,        '"target": [',
'"ADD_LINE"',         33,        '"routing_metadata",',
'"ADD_LINE"',         33,        '"nhop_ipv4"',
'"ADD_LINE"',         29,        '],',
'"ADD_LINE"',         29,        '"mask": null',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        '],',
'"ADD_LINE"',         21,        '"actions": [',
'"ADD_LINE"',         25,        '"set_dmac",',
'"ADD_LINE"',         25,        '"_drop"',
'"ADD_LINE"',         21,        '],',
'"ADD_LINE"',         21,        '"next_tables": {',
'"ADD_LINE"',         25,        '"set_dmac": null,',
'"ADD_LINE"',         25,        '"_drop": null',
'"ADD_LINE"',         21,        '},',
'"ADD_LINE"',         21,        '"base_default_next": null',
'"ADD_LINE"',         17,        '}',
'"ADD_LINE"',         13,        '],',
'"ADD_LINE"',         13,        '"action_profiles": [],',
'"ADD_LINE"',         13,        '"conditionals": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"name": "_condition_0",',
'"ADD_LINE"',         21,        '"id": 0,',
'"ADD_LINE"',         21,        '"expression": {',
'"ADD_LINE"',         25,        '"type": "expression",',
'"ADD_LINE"',         25,        '"value": {',
'"ADD_LINE"',         29,        '"op": "and",',
'"ADD_LINE"',         29,        '"left": {',
'"ADD_LINE"',         33,        '"type": "expression",',
'"ADD_LINE"',         33,        '"value": {',
'"ADD_LINE"',         37,        '"op": "valid",',
'"ADD_LINE"',         37,        '"left": null,',
'"ADD_LINE"',         37,        '"right": {',
'"ADD_LINE"',         41,        '"type": "header",',
'"ADD_LINE"',         41,        '"value": "ipv4"',
'"ADD_LINE"',         37,        '}',
'"ADD_LINE"',         33,        '}',
'"ADD_LINE"',         29,        '},',
'"ADD_LINE"',         29,        '"right": {',
'"ADD_LINE"',         33,        '"type": "expression",',
'"ADD_LINE"',         33,        '"value": {',
'"ADD_LINE"',         37,        '"op": ">",',
'"ADD_LINE"',         37,        '"left": {',
'"ADD_LINE"',         41,        '"type": "field",',
'"ADD_LINE"',         41,        '"value": [',
'"ADD_LINE"',         45,        '"ipv4",',
'"ADD_LINE"',         45,        '"ttl"',
'"ADD_LINE"',         41,        ']',
'"ADD_LINE"',         37,        '},',
'"ADD_LINE"',         37,        '"right": {',
'"ADD_LINE"',         41,        '"type": "hexstr",',
'"ADD_LINE"',         41,        '"value": "0x0"',
'"ADD_LINE"',         37,        '}',
'"ADD_LINE"',         33,        '}',
'"ADD_LINE"',         29,        '}',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        '},',
'"SET_CONDN"',        21,        '"true_next": "ipv4_lpm",',
'"ADD_LINE"',         21,        '"false_next": null',
'"CHK_ALLOWED_PATH"', 17,        '}',
'"ADD_LINE"',         13,        ']',
'"ADD_LINE"',         9,        '},',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "egress",',
'"ADD_LINE"',         13,        '"id": 1,',
'"ADD_LINE"',         13,        '"init_table": "send_frame",',
'"ADD_LINE"',         13,        '"tables": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"name": "send_frame",',
'"ADD_LINE"',         21,        '"id": 2,',
'"ADD_LINE"',         21,        '"match_type": "exact",',
'"ADD_LINE"',         21,        '"type": "simple",',
'"ADD_LINE"',         21,        '"max_size": 256,',
'"ADD_LINE"',         21,        '"with_counters": false,',
'"ADD_LINE"',         21,        '"direct_meters": null,',
'"ADD_LINE"',         21,        '"support_timeout": false,',
'"ADD_LINE"',         21,        '"key": [',
'"ADD_LINE"',         25,        '{',
'"ADD_LINE"',         29,        '"match_type": "exact",',
'"ADD_LINE"',         29,        '"target": [',
'"ADD_LINE"',         33,        '"standard_metadata",',
'"ADD_LINE"',         33,        '"egress_port"',
'"ADD_LINE"',         29,        '],',
'"ADD_LINE"',         29,        '"mask": null',
'"ADD_LINE"',         25,        '}',
'"ADD_LINE"',         21,        '],',
'"ADD_LINE"',         21,        '"actions": [',
'"ADD_LINE"',         25,        '"rewrite_mac",',
'"ADD_LINE"',         25,        '"_drop"',
'"ADD_LINE"',         21,        '],',
'"ADD_LINE"',         21,        '"next_tables": {',
'"ADD_LINE"',         25,        '"rewrite_mac": null,',
'"ADD_LINE"',         25,        '"_drop": null',
'"ADD_LINE"',         21,        '},',
'"ADD_LINE"',         21,        '"base_default_next": null',
'"ADD_LINE"',         17,        '}',
'"ADD_LINE"',         13,        '],',
'"ADD_LINE"',         13,        '"action_profiles": [],',
'"ADD_LINE"',         13,        '"conditionals": []',
'"ADD_LINE"',         9,        '}',
'"ADD_LINE"',         5,        '],',
'"ADD_LINE"',         5,        '"calculations": [',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "ipv4_checksum",',
'"ADD_LINE"',         13,        '"id": 0,',
'"ADD_LINE"',         13,        '"input": [',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"type": "field",',
'"ADD_LINE"',         21,        '"value": [',
'"ADD_LINE"',         25,        '"ipv4",',
'"ADD_LINE"',         25,        '"version"',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"type": "field",',
'"ADD_LINE"',         21,        '"value": [',
'"ADD_LINE"',         25,        '"ipv4",',
'"ADD_LINE"',         25,        '"ihl"',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"type": "field",',
'"ADD_LINE"',         21,        '"value": [',
'"ADD_LINE"',         25,        '"ipv4",',
'"ADD_LINE"',         25,        '"diffserv"',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"type": "field",',
'"ADD_LINE"',         21,        '"value": [',
'"ADD_LINE"',         25,        '"ipv4",',
'"ADD_LINE"',         25,        '"totalLen"',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"type": "field",',
'"ADD_LINE"',         21,        '"value": [',
'"ADD_LINE"',         25,        '"ipv4",',
'"ADD_LINE"',         25,        '"identification"',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"type": "field",',
'"ADD_LINE"',         21,        '"value": [',
'"ADD_LINE"',         25,        '"ipv4",',
'"ADD_LINE"',         25,        '"flags"',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"type": "field",',
'"ADD_LINE"',         21,        '"value": [',
'"ADD_LINE"',         25,        '"ipv4",',
'"ADD_LINE"',         25,        '"fragOffset"',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"type": "field",',
'"ADD_LINE"',         21,        '"value": [',
'"ADD_LINE"',         25,        '"ipv4",',
'"ADD_LINE"',         25,        '"ttl"',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"type": "field",',
'"ADD_LINE"',         21,        '"value": [',
'"ADD_LINE"',         25,        '"ipv4",',
'"ADD_LINE"',         25,        '"protocol"',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"type": "field",',
'"ADD_LINE"',         21,        '"value": [',
'"ADD_LINE"',         25,        '"ipv4",',
'"ADD_LINE"',         25,        '"srcAddr"',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '},',
'"ADD_LINE"',         17,        '{',
'"ADD_LINE"',         21,        '"type": "field",',
'"ADD_LINE"',         21,        '"value": [',
'"ADD_LINE"',         25,        '"ipv4",',
'"ADD_LINE"',         25,        '"dstAddr"',
'"ADD_LINE"',         21,        ']',
'"ADD_LINE"',         17,        '}',
'"ADD_LINE"',         13,        '],',
'"ADD_LINE"',         13,        '"algo": "csum16"',
'"ADD_LINE"',         9,        '}',
'"ADD_LINE"',         5,        '],',
'"ADD_LINE"',         5,        '"checksums": [',
'"ADD_LINE"',         9,        '{',
'"ADD_LINE"',         13,        '"name": "ipv4.hdrChecksum|ipv4_checksum",',
'"ADD_LINE"',         13,        '"id": 0,',
'"ADD_LINE"',         13,        '"target": [',
'"ADD_LINE"',         17,        '"ipv4",',
'"ADD_LINE"',         17,        '"hdrChecksum"',
'"ADD_LINE"',         13,        '],',
'"ADD_LINE"',         13,        '"type": "generic",',
'"ADD_LINE"',         13,        '"calculation": "ipv4_checksum",',
'"ADD_LINE"',         13,        '"if_cond": null',
'"ADD_LINE"',         9,        '}',
'"ADD_LINE"',         5,        '],',
'"ADD_LINE"',         5,        '"learn_lists": [],',
'"ADD_LINE"',         5,        '"field_lists": [],',
'"ADD_LINE"',         5,        '"counter_arrays": [],',
'"ADD_LINE"',         5,        '"register_arrays": [],',
'"ADD_LINE"',         5,        '"force_arith": [',
'"ADD_LINE"',         9,        '[',
'"ADD_LINE"',         13,        '"standard_metadata",',
'"ADD_LINE"',         13,        '"ingress_port"',
'"ADD_LINE"',         9,        '],',
'"ADD_LINE"',         9,        '[',
'"ADD_LINE"',         13,        '"standard_metadata",',
'"ADD_LINE"',         13,        '"packet_length"',
'"ADD_LINE"',         9,        '],',
'"ADD_LINE"',         9,        '[',
'"ADD_LINE"',         13,        '"standard_metadata",',
'"ADD_LINE"',         13,        '"egress_spec"',
'"ADD_LINE"',         9,        '],',
'"ADD_LINE"',         9,        '[',
'"ADD_LINE"',         13,        '"standard_metadata",',
'"ADD_LINE"',         13,        '"egress_port"',
'"ADD_LINE"',         9,        '],',
'"ADD_LINE"',         9,        '[',
'"ADD_LINE"',         13,        '"standard_metadata",',
'"ADD_LINE"',         13,        '"egress_instance"',
'"ADD_LINE"',         9,        '],',
'"ADD_LINE"',         9,        '[',
'"ADD_LINE"',         13,        '"standard_metadata",',
'"ADD_LINE"',         13,        '"instance_type"',
'"ADD_LINE"',         9,        '],',
'"ADD_LINE"',         9,        '[',
'"ADD_LINE"',         13,        '"standard_metadata",',
'"ADD_LINE"',         13,        '"clone_spec"',
'"ADD_LINE"',         9,        '],',
'"ADD_LINE"',         9,        '[',
'"ADD_LINE"',         13,        '"standard_metadata",',
'"ADD_LINE"',         13,        '"_padding"',
'"ADD_LINE"',         9,        ']',
'"ADD_LINE"',         5,        ']',
'"ADD_LINE"',         1,        '}',
]

condn_for_allowed_paths = [

 '"NONE"',       17,  '{',
 '"REP_CONDN"',  21,  '"name": "condition_1",',
 '"SUB_ID"',     21,  '"id": 1,',
 '"NONE"',       21,  '"expression": {',
 '"NONE"',       25,      '"type": "expression",',
 '"NONE"',       25,      '"value": {',
 '"NONE"',       29,          '"op": "and",',
 '"NONE"',       29,          '"left": {',
 '"NONE"',       33,              '"type": "expression",',
 '"NONE"',       33,              '"value": {',
 '"NONE"',       37,                  '"op": "==",',
 '"NONE"',       37,                  '"left": {',
 '"NONE"',       41,                      '"type": "field",',
 '"NONE"',       41,                      '"value": [',
 '"NONE"',       45,                          '"ipv4",',
 '"NONE"',       45,                          '"srcAddr"',
 '"NONE"',       41,                      ']',
 '"NONE"',       37,                  '},',
 '"NONE"',       37,                  '"right": {',
 '"NONE"',       41,                      '"type": "hexstr",',
 '"REP_SADDR"',  41,                      '"value": "0x0a00020a"',
 '"NONE"',       37,                  '}',
 '"NONE"',       33,              '}',
 '"NONE"',       29,          '},',
 '"NONE"',       29,          '"right": {',
 '"NONE"',       33,              '"type": "expression",',
 '"NONE"',       33,              '"value": {',
 '"NONE"',       37,                  '"op": "==",',
 '"NONE"',       37,                  '"left": {',
 '"NONE"',       41,                      '"type": "field",',
 '"NONE"',       41,                      '"value": [',
 '"NONE"',       45,                          '"ipv4",',
 '"NONE"',       45,                          '"dstAddr"',
 '"NONE"',       41,                      ']',
 '"NONE"',       37,                  '},',
 '"NONE"',       37,                  '"right": {',
 '"NONE"',       41,                      '"type": "hexstr",',
 '"REP_DADDR"',  41,                      '"value": "0x0a00010a"',
 '"NONE"',       37,                  '}',
 '"NONE"',       33,              '}',
 '"NONE"',       29,          '}',
 '"NONE"',       25,      '}',
 '"NONE"',       21,  '},',
 '"REP_TLBL"',   21,  '"true_next": "ipv4_lpm",',
 '"REP_FLBL"',   21,  '"false_next": "condition_2"',
 '"ITER_CHK"',   17,  '}'
]

def add_str_to_out_atpos( pos, inp_str ):
    tmp_out_str = ""
    for cnt in xrange(1, pos ):
        tmp_out_str = tmp_out_str + ' '
    tmp_out_str = tmp_out_str + inp_str
    return tmp_out_str

def add_rules_for_allowed_paths( outfile ):
    with open('in_topo.json') as data_file:
        data = json.load(data_file)

    my_allowed_paths = []
    for item in dict.items( data["allowed_paths"] ):
        my_allowed_paths.append(item)

    allowed_paths_len = len(my_allowed_paths)
    if (allowed_paths_len <= 0):
        print "Nothing in Allowed Paths... Returning...."
        return

    next_lbl_id = 1


    # next_lbl_id  is already set to 1

    allowed_path_len = len(my_allowed_paths)
    cur_allowed_path_idx = 0

    for key, value in my_allowed_paths :

        cur_allowed_path_idx =  cur_allowed_path_idx + 1
        cur_host_path_len = len(value)
        cur_host_idx = 0

        for hname in value :
            # Go 2 iterations. In 1st Iteration add condition for forward path.
            # In 2nd iteration, add condition for reverse path

            cur_host_idx = cur_host_idx + 1
            iter_cnt = 0

            for iter_cnt in xrange(0,2) :
                if (iter_cnt == 0 ):
                    src_host = key
                    dst_host = hname
                else : 
                    src_host = hname
                    dst_host = key
                print "Processing for ...", src_host, "->", dst_host
            
                mylen = len(condn_for_allowed_paths)
                print "Length of conditional paths...", mylen

                cnt = 0
                while (cnt < mylen) :
                    mycondn = condn_for_allowed_paths[cnt]
                    cnt = cnt + 1
                    idx = condn_for_allowed_paths[cnt]
                    cnt = cnt + 1
                    value = condn_for_allowed_paths[cnt]
                    cnt = cnt + 1
                    if (mycondn == '"NONE"' ):
                        # print "No Spl processing ..." 
                        my_out_str = add_str_to_out_atpos( idx, value )
                        print >> outfile, my_out_str
                    if (mycondn == '"REP_CONDN"' ):
                        # print "Replace condition : " 
                        condn_lbl = str("condition_") + str(next_lbl_id)
                        tmp_str = '"name": '
                        tmp_str = tmp_str + '"' + condn_lbl + '",'
                        my_out_str = add_str_to_out_atpos( idx, tmp_str )
                        print >> outfile, my_out_str
                    if (mycondn == '"SUB_ID"' ):
                        # print "Substitute ID : ..." 
                        tmp_str = '"id": '
                        tmp_str = tmp_str + str(next_lbl_id) + ','
                        my_out_str = add_str_to_out_atpos( idx, tmp_str )
                        print >> outfile, my_out_str
                    if (mycondn == '"REP_SADDR"' ):
                        # print "Rep Source Addr : "
                        tmp_str = '"value": '
                        src_hnum = int(src_host[1:])
                        hnum = "%02x" % src_hnum 
                        tmp_ipaddr = "0x0a00" + hnum + "0a"
                        tmp_str = tmp_str + '"' + tmp_ipaddr + '"'
                        my_out_str = add_str_to_out_atpos( idx, tmp_str )
                        print >> outfile, my_out_str
                    if (mycondn == '"REP_DADDR"' ):
                        # print "Rep Dest Addr : "
                        tmp_str = '"value": '
                        src_hnum = int(dst_host[1:])
                        hnum = "%02x" % src_hnum 
                        tmp_ipaddr = "0x0a00" + hnum + "0a"
                        tmp_str = tmp_str + '"' + tmp_ipaddr + '"'
                        my_out_str = add_str_to_out_atpos( idx, tmp_str )
                        print >> outfile, my_out_str
                    if (mycondn == '"REP_TLBL"' ):
                        # print "Rep True Label : "
                        tmp_str = '"true_next": "ipv4_lpm",'
                        my_out_str = add_str_to_out_atpos( idx, tmp_str )
                        print >> outfile, my_out_str
                    if (mycondn == '"REP_FLBL"' ):
                        # print "Rep False Label "

                        tmp_str = '"false_next": '
                        next_lbl_id = next_lbl_id + 1

                        if ( iter_cnt == 0 ):
                            condn_lbl = str("condition_") + str(next_lbl_id)
                            tmp_str = tmp_str + '"' + condn_lbl + '"'

                        else :
                            if( cur_host_idx < cur_host_path_len ):
                                condn_lbl = str("condition_") + str(next_lbl_id)
                                tmp_str = tmp_str + '"' + condn_lbl + '"'
                            elif(cur_allowed_path_idx < allowed_path_len ):
                                condn_lbl = str("condition_") + str(next_lbl_id)
                                tmp_str = tmp_str + '"' + condn_lbl + '"'
                            else :
                                condn_lbl = "null"
                                tmp_str = tmp_str + condn_lbl 

                        my_out_str = add_str_to_out_atpos( idx, tmp_str )
                        print >> outfile, my_out_str
                    if (mycondn == '"ITER_CHK"' ):
                        if ( iter_cnt == 0 ):
                            tmp_str = value + ','
                        if ( iter_cnt == 1 ):  
                            if( cur_host_idx < cur_host_path_len ):
                                tmp_str = value + ','
                            elif(cur_allowed_path_idx < allowed_path_len ):
                                tmp_str = value + ','
                            else :
                                tmp_str = value
                        my_out_str = add_str_to_out_atpos( idx, tmp_str )
                        print >> outfile, my_out_str
            # Inner Iter loop for reverse path
    return

def main():

    tmp_len = len(template_lines_tmp)
    print "Template Lines Length ...", tmp_len

    with open('in_topo.json') as data_file:
        data = json.load(data_file)

    my_allowed_paths = []
    for item in dict.items( data["allowed_paths"] ):
        my_allowed_paths.append(item)

    data_file.close()
    allowed_paths_len = len(my_allowed_paths)
    if (allowed_paths_len <= 0):
        print "Nothing in Allowed Paths... Returning...."


    with open('routernew.json', 'w') as f_handle:
        idx = 0
        while (idx < tmp_len) :
            cmd = template_lines_tmp[idx]
            idx = idx + 1
            posn = template_lines_tmp[idx]
            idx = idx + 1
            value = template_lines_tmp[idx]
            idx = idx + 1

            my_out_str = ""
            if (cmd == '"ADD_LINE"' ):
                # print "Add Line ..." 
                my_out_str = add_str_to_out_atpos( posn, value )
                print >> f_handle, my_out_str
            if (cmd == '"SET_CONDN"' ):
                if (allowed_paths_len <= 0):
                    print "Nothing in Allowed Paths... "
                    my_out_str = add_str_to_out_atpos( posn, value )
                    print >> f_handle, my_out_str
                else :
                    next_lbl_id = 1
                    condn_lbl = str("condition_") + str(next_lbl_id)
                    out_str_1 = '                    "true_next": '
                    out_str = out_str_1 + '"' + condn_lbl + '",' 
                    print >> f_handle, out_str
            if (cmd == '"CHK_ALLOWED_PATH"' ):
                if (allowed_paths_len <= 0):
                    print "Nothing in Allowed Paths... "
                    my_out_str = add_str_to_out_atpos( posn, value )
                    print >> f_handle, my_out_str
                else :
                    # We may have to put a comma delimiter
                    my_out_str = add_str_to_out_atpos( posn, value )
                    my_out_str = my_out_str + ','
                    print >> f_handle, my_out_str

                    # Do the special processing here...
                    add_rules_for_allowed_paths(  f_handle )

        f_handle.close()

if __name__ == '__main__':
    main()

