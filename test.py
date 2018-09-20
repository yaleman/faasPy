#!/usr/bin/env python3

from faas import FaaSAPI

# config needs the following:
# FaaS API key/password:
#apikey = ""
#apipassword = ""
# requests proxies (or None:
#PROXY={ 'https' : PROXY, 'http' : PROXY }
from config import *

faas = FaaSAPI(apikey, apipassword, PROXY)
investigations = faas.get_investigations()

for dobject in investigations[:1]:
    investigation = faas.get_investigation(dobject['external_references'][0]['external_id'])
    if investigation:

        investigation_report = ""
        iocs = []

        for investigation_object in investigation['objects']:
            if 'x_fireeye_com_note_type' in investigation_object.keys():
                investigation_report = investigation_object['description']
            if 'primary_target' in investigation_object.keys():
                if investigation_object['primary_target'] not in iocs:
                    iocs.append(investigation_object['primary_target'])
            if 'secondary_targets' in investigation_object.keys():
                for s in investigation_object['secondary_targets']:
                    if s not in iocs:
                        iocs.append(s)
        
        print("#"*50)
        print("Name: FaaS {} {}".format(dobject['external_references'][0]['external_id'], dobject['name'], ))
        print("Status in FaaS console: {}".format(dobject['investigation_status']))
        print("Last Updated: {}".format(dobject['modified']))
 
        report = "\nReport:\n{}\n{}".format(dobject['description'].strip(), investigation_report.strip())
        report = report.replace("&nbsp;", " ".replace("  ", " "))
        print(report)
        print("IOCs: {}".format(",".join([ "`{}`".format(ioc) for ioc in iocs])))



