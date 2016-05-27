ps aux|grep "/bin/sh -c echo"|cut -d " " -f6| while read line; do sudo kill -9 $line;done
ps aux|grep "/bin/sh -c echo"|cut -d " " -f7| while read line; do sudo kill -9 $line;done
ps aux|grep "/bin/sh -c echo"|cut -d " " -f8| while read line; do sudo kill -9 $line;done
ps aux|grep "/bin/sh -c echo"|cut -d " " -f9| while read line; do sudo kill -9 $line;done
ps aux|grep "timeout"|cut -d " " -f6| while read line; do sudo kill -9 $line;done
ps aux|grep "timeout"|cut -d " " -f7| while read line; do sudo kill -9 $line;done
ps aux|grep "timeout"|cut -d " " -f8| while read line; do sudo kill -9 $line;done
ps aux|grep "timeout"|cut -d " " -f9| while read line; do sudo kill -9 $line;done
ps aux|grep -E "\./.{10}"|cut -d " " -f6| while read line; do sudo kill -9 $line;done
ps aux|grep -E "\./.{10}"|cut -d " " -f7| while read line; do sudo kill -9 $line;done
ps aux|grep -E "\./.{10}"|cut -d " " -f8| while read line; do sudo kill -9 $line;done
ps aux|grep -E "\./.{10}"|cut -d " " -f9| while read line; do sudo kill -9 $line;done
