import re
from django.db import models

# Create your models here.

sizein = { 'G':1073741824,
           'M':1048576,
           None:1}

size_re = re.compile('(?P<num>[0-9][0-9]*(\.[0-9]+)?)(?P<unit>[MG])?')

def _parse_size(size):
    m = size_re.match(size)
    if not m:
        raise ValueError("Invalid size specification: %s" % (size,))
    num = float(m.groupdict()['num'])
    unit = m.groupdict()['unit']
    if not unit in ['M','G', None]:
        raise ValueError("Unit must be one of M or G or None")
    return int(num * sizein[unit])

def import_record(server, textline):
    parts = [i.strip() for i in textline.split()]
    p = Partition.objects.create(server=server)
    p.filesystem = parts[0]
    p.use = _parse_size(parts[2])
    p.size = _parse_size(parts[1])
    p.mount = parts[5]
    p.save()
    
def ip_validator(ip):
    """Check for valid IP"""
    return True

class Server(models.Model):

    ipaddr = models.IPAddressField(max_length=20, validators=[ip_validator])
    assettag = models.CharField(max_length=25)
    servicetag = models.CharField(max_length=25)
    domain = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    hostname = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=255)

    def fqdn(self):
        """Compose the fully qualified domain name from the hostname and domain
        >>> from cfgmake.models import Server
        >>> svr = Server(hostname="foo")
        >>> svr.domain = "uwinnipeg.ca"
        >>> svr.fqdn()
        'foo.uwinnipeg.ca'
        """
        return '.'.join([self.hostname, self.domain])

    def __unicode__(self):
        return self.hostname

class Partition(models.Model):

    filesystem = models.CharField(max_length=255, blank=True)
    size = models.IntegerField(null=True)
    use = models.IntegerField(null=True)
    mount = models.CharField(max_length=255, blank=True)
    server = models.ForeignKey(Server)
    
    def avail(self):
        return self.size - self.use
    
    def __unicode__(self):
        return self.filesystem

class UnixUser(models.Model):

    iscrypted = models.BooleanField()
    login = models.CharField(max_length=50, blank=False, null=False)
    passwd = models.CharField(verbose_name="Password", max_length=255)
    uid = models.IntegerField(verbose_name="User ID", blank=False, null=False)
    gid = models.IntegerField(verbose_name="Group ID", blank=False, null=False)
    fullname = models.CharField(max_length=255)
    home = models.CharField(verbose_name="Home Directory", max_length=255)

class ConfigFile(models.Model):

    path = models.CharField(max_length=255)
    template = models.FileField(upload_to="config/")

class Application(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    executable = models.CharField(max_length=255)
    configfiles = models.ForeignKey(ConfigFile)
    servers = models.ManyToManyField(Server)

    def __unicode__(self):
        return self.name
