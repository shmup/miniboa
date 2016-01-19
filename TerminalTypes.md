#Responses of various clients to the Telnet "Terminal Type" Command (see RFC 779).

# Terminal Types #

Results of requesting a terminal type sub-negotiation sequence.  See RFC 779 at http://www.rfc-archive.org/getrfc.php?rfc=779

  * Linux Gnome-terminal Telnet = 'XTERM"
  * Linux Tinyfuge = "TINYFUGUE"
  * Linux Eterm = "ETERM"
  * Linux ROXterm = "XTERM"
  * Linux Terminal = "XTERM"
  * Linux RXVT = "RXVT"
  * Linux Aterm = "RXVT"
  * Linux mrxvt = "RXVT"
  * Linux URXVT-Unicode = "RXVT-UNICODE"
  * Linux PCMan X = Didn't work at all, ends entries with a CR and no LF.
  * Linux Putty = Failed,  no response to IAC DO TERMINAL TYPE

  * Windows 2000 Telnet = "ANSI"
  * Windows XP Telnet = "ANSI"
  * Windows WinTin++ = "TINTIN++"
  * Windows Putty = Failed,  no response to IAC DO TERMINAL TYPE
  * Windows GoSClient 1.7.2 = "gosclient"
  * Windows MudMagic = Failed, responded with IAC DONT TERMINAL-TYPE
  * Windows Genius = Failed, no response to IAC DO TERMINAL TYPE
  * Windows MUSHclient = "mushclient"
  * Windows Pueblo = "pueblo"
  * Ashavar's Legacy Mud Client = "ALCLIENT"
  * Zmud 7.21 = "zmud"
  * SimpleMU = "ANSI"
  * Portal GT = "VT100"
  * Windows Tinyfuge = "TINYFUGUE"