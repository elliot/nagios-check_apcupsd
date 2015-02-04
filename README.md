# APCUPSd Nagios Check

Simple checks that are apart of the PowerPi project (Raspberry Pi based power monitoring).

## Usage

#### Scope Usage
   ```check_apcupsd.py -m time -W 30 -C 15```

## Limitations

Only supports status, time remaining and battery percentage metrics at this time (APCUPSd support for our models of UPS is limited).
It is trivial to add additional checks. Pull requests welcome.

## Author

Elliot Anderson ([Email](mailto:elliot.a@gmail.com), [Twitter](http://www.twitter.com/elliotanderson))

## License

This project is licensed under the MIT license.