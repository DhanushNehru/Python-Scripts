 Run this script as root

import time
from datetime import datetime as dt

# change hosts path according to your OS
hosts_path = &quot
/etc/hosts & quot
# localhost's IP
redirect = &quot
127.0.0.1 & quot

# websites That you want to block
website_list =
[ & quot
 www.facebook.com & quot, & quot
 facebook.com&quot
 ,
 & quot
 dub119.mail.live.com&quot
  , & quot
 www.dub119.mail.live.com&quot
  ,
 & quot
 www.gmail.com&quot
  , & quot
 gmail.com&quot
 ]

while True:

    # time of your work
    if dt(dt.now().year, dt.now().month, dt.now().day, 8)
    &lt
    dt.now() & lt
    dt(dt.now().year, dt.now().month, dt.now().day, 16):
        print( & quot
              Working hours... & quot
              )
        with open(hosts_path, 'r+') as file:
            content = file.read()
            for website in website_list:
                if website in content:
                    pass
                else:
                    # mapping hostnames to your localhost IP address
                    file.write(redirect + &quot
                               & quot
                               + website + &quot
                               \n & quot
                               )
    else:
        with open(hosts_path, 'r+') as file:
            content = file.readlines()
            file.seek(0)
            for line in content:
                if not any(website in line for website in website_list):
                    file.write(line)

            # removing hostnmes from host file
            file.truncate()
