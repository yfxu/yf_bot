import time

def format_str( t ):
	t = int( t )

	if t <= 60:		
		return time.strftime("%Ss", time.gmtime( t ))
	if t <= 3600:
		return time.strftime("%#Mmin %Ss", time.gmtime( t ))
	else:
		return time.strftime("%#Hhr %#Mmin %Ss", time.gmtime( t ))