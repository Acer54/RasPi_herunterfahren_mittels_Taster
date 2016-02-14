#Video Anleitung zur Installation:
[![Youtube-Video](http://img.youtube.com/vi/adlGqnITYlA/0.jpg)](https://www.youtube.com/watch?v=adlGqnITYlA)
---
###WICHTIG: Vor dem ersten Gebrauch, solltet ihr das Script testen! Hierzu habe ich das Argument "--debug" eingefügt.
z.B.
```
python shutdown_daemon.py --debug
```
oder
```
python shutdown_daemon_interference_secure.py --debug
```
oder
```
python shutdown_daemon_multicommand.py --debug
```
---
#Erklärungen zu den Unterschieden:

<table style="undefined;table-layout: fixed; width: 864px">
<colgroup>
<col style="width: 199px">
<col style="width: 665px">
</colgroup>
  <tr>
    <th>Datei:</th>
    <th>Funktionsbeschreibung:</th>
  </tr>
  <tr>
    <td>shutdown_daemon.py</td>
    <td>Herunterfahren -/ Hochfahren mittels Taster zwischen GPIO3 (Pin5) und GND (Pin6)Eine Videobeschreibung zur Installation ist zu finden unter: YoutubeEine schriftliche Anleitung findet sich unter: my-darling.is-a-linux-user.org Das Script funktioniert bisher recht zuverlässig, kann allerdings bei größeren Interferenzen an den GPIOs dazu führen, dass der Pin5,heruntergefahren wird, obwohl man dies gar nicht will... falls dies der Fall ist, ist dieses Script "zu einfach gestrickt".Ihr solltet das Script "shutdown_daemon_interference_secure.py" nutzen</td>
  </tr>
  <tr>
    <td>shutdown_daemon_interference_secure.py</td>
    <td>Diese Script ist von der Funktion und Installation genau so wie "shutdown_daemon.py", jedoch mit der kleinen Änderung, dass der Tasternicht mehr durch einen "kurzen" Klick zu einem Herunterfahren führt, sondern für mindestens 1 Sekunde gedückt gehalten werden muss!</td>
  </tr>
  <tr>
    <td>shutdown_daemon_multicommand.py</td>
    <td>Dieses Script entstand auf Anfrage eines Nutzers, der gerne mehrere Befehle mittels unterschiedlicher Anzahl von Tastendrückenausgelöst haben möchte.Beschreibung und Einstellungen findet ihr in den ersten Zeilen des Scriptes selbst.Mir persönlich ist das allerdings zu viel "blindes gemorse..." :-)</td>
  </tr>
</table>