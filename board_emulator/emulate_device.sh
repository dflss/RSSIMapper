# first run: socat -d -d pty,raw,echo=0,b9600 pty,raw,echo=0,b9600
# then: ./emulate_device.sh /dev/pts/3
for i in {1..100}
do
  printf "%b" '\x1b[?25l\x1b[H\x1b[6;0H\x1b[2K\x02Device Status: Sensor - Addr=0x0002, Timestamp=18, RSSI=-73 /\x03\x1b[?25l\x1b[H\x1b[7;0H\x1b[2K\x02Number of Joined Devices: 1\x03' > $1
  sleep 0.1s
done