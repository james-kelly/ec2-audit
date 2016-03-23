from datetime import datetime

import boto.ec2
from dateutil.parser import *

REGIONS = ["us-west-2", "us-west-1", "us-east-1", "eu-west-1", ]
ffs = list()

for region in REGIONS:
    conn = boto.ec2.connect_to_region(region)
    reservations = conn.get_all_reservations()
    for reservation in reservations:
        instances = reservation.instances
        for instance in instances:
            tag_names = [k.lower() for k, v in instance.tags.iteritems()]
            launch_time = parse(instance.launch_time)
            current_time = datetime.now(launch_time.tzinfo)
            uptime = current_time - launch_time
            if instance.state == u'running' and 'Application' in tag_names:
                ffs.append(instance)

for instance in sorted(ffs, lambda a, b: cmp(parse(a.launch_time), parse(b.launch_time))):
    print "{id}|{launch_time}|{public_dns_name}|{instance_type}|{placement}|{key_name}|{tags}".format(
        id=instance.id,
        launch_time=instance.launch_time,
        public_dns_name=instance.public_dns_name,
        instance_type=instance.instance_type,
        placement=instance.placement,
        key_name=instance.key_name,
        tags=",".join("=".join(x) for x in instance.tags.iteritems())
    )
