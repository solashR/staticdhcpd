#General settings
#####
#Changes take effect on reload
#######################################
SYSTEM_NAME = 'staticDHCPd'
LOG_CAPACITY = 1000 #: The number of events to keep in the server's log-buffer.
POLL_INTERVALS_TO_TRACK = 20 #: The amount of stats to keep track of.

#Server settings
#####
#Changes take effect on restart
#######################################
DHCP_SERVER_IP = '192.168.0.10' #: The IP of the interface on which DHCP responses should be sent.
SERVER_PORT = 67 #: The port on which DHCP requests are to be received; 67 is the standard.
CLIENT_PORT = 68 #: The port on which clients wait for DHCP responses; 68 is the standard.
UNAUTHORIZED_CLIENT_TIMEOUT = 60 #: The number of seconds for which to ignore unknown MACs.
MISBEHAVING_CLIENT_TIMEOUT = 300 #: The number of seconds for which to ignore potentially malicious MACs.

WEB_ENABLED = True #: True to enable access to server statistics and logs.
WEB_IP = '192.168.1.10' #: The IP of the interface on which the HTTP interface should be served.
WEB_PORT = 30880 #: The port on which the HTTP interface should be served.

#Server behaviour settings
#####
#Changes take effect on reload
#######################################
SKIP_REQUEST_VALIDATION = True #: If False, all DHCPREQUESTs must have their MAC-IP pair checked.
#Since there are no leases, this step is irrelevant as long as all DHCP clients are behaving properly.
#(And, in the event of a malicious alteration, the damage is no different from a manually configured box)
ALLOW_DHCP_RENEW = False #: If True, DHCP clients may renew their "lease" before it expires.
#Since there are no leases, this setting makes no real difference.
POLLING_INTERVAL = 30 #: The frequency at which the DHCP server's stats will be polled.
SUSPEND_THRESHOLD = 8 #: The number of times a well-behaved MAC can search for or request an IP within the polling interval.

#Database settings
#####
#Changes take effect on restart
#######################################
DATABASE_ENGINE = 'MySQL' #: Allowed values: MySQL, SQLite

MYSQL_DATABASE = 'dhcp' #: The name of your database.
MYSQL_USERNAME = 'dhcp_user' #: The name of a user with SELECT access.
MYSQL_PASSWORD = 'dhcp_pass' #: The password of the user.
MYSQL_HOST = None #: The host on which MySQL is running. None for 'localhost'.
MYSQL_PORT = 3306 #: The port on which MySQL is running; ignored when HOST is None.
MYSQL_MAXIMUM_CONNECTIONS = 4 #: The number of threads that may read the database at once.

SQLITE_FILE = '/etc/staticDHCPd/dhcp.sqlite3' #: The file that contains your SQLite database.

#DHCP-processing functions
#####
#Changes take effect on reload
#######################################
#DO NOT TOUCH LINES BELOW THIS POINT
import pydhcplib.type_strlist
#DO NOT TOUCH LINES ABOVE THIS POINT

def loadDHCPPacket(packet, client_ip):
	"""
	If you do not need an option, just comment it out.
	
	If you need to add an option, consult pyDHCPlib's documentation.
	
	client_ip is a quadruple of octets. 
	"""
	#Two weeks, expressed as a four-byte value in seconds.
	#This field is required.
	packet.SetOption('ip_address_lease_time', [0, 18, 117, 0])
	
	#Default gateway, subnet mask, and broadcast address.
	packet.SetOption('router', [192,168,168,1])
	packet.SetOption('subnet_mask', [255,255,255,0])
	packet.SetOption('broadcast_address', [192,168,168,255])
	
	#Search domain/nameservers. Note that there are two IPs specified.
	packet.SetOption('domain_name', pydhcplib.type_strlist.strlist("hamsterx.homelinux.org").list())
	packet.SetOption('name_server', [192,168,168,100,127,0,0,1])
	
	#NTP timeservers to be used. Note that there are two IPs specified here.
	#This field is disabled by default since most every client just uses its own rules to pick a server.
	#packet.SetOption('time_server', [192,168,168,100,127,0,0,1])
	
	#Default Web server. All browsers seem to point at a search engine by default, so this is obsolete.
	#packet.SetOption('default_www_server', [74,125,53,104])
	