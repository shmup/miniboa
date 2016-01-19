#Coloring Text Inline with Caret Codes (Optional)

# Introduction #

The following ANSI shortcuts are optional and only apply to text transmitted to the client with the **send\_cc()** and **send\_wrapped()** methods of the **TelnetClient** object.  The **TelnetClient.send()** method does not process them and you can easily implement your own system (or none at all) by using it for all outgoing text.

In order to make text decorating easier, you can use the following caret codes inside blocks of text.  If the client has turned off color, the tokens are simply stripped out.

You'll notice there is a pattern to the codes which should be easy to remember -- lower case = dark/mode off, uppercase = bright/mode on.  Black is 'k' as in CMYK, since Blue took the 'b'.

# Caret Codes #
```

  ^k   = black
  ^K   = bold black (grey)
  ^r   = red
  ^R   = bold red
  ^g   = green
  ^G   = bold green
  ^y   = yellow
  ^Y   = bold yellow
  ^b   = blue
  ^B   = bold blue
  ^m   = magenta
  ^M   = bold magenta
  ^c   = cyan
  ^C   = bold cyan
  ^w   = white
  ^W   = bold white
  ^!   = bold on (use within a block of non-bright text)
  ^.   = bold off 
  ^d   = default text colors, varies by client    
  ^0   = black background
  ^1   = red background
  ^2   = green background
  ^3   = yellow background
  ^4   = blue background
  ^5   = magenta background
  ^6   = cyan background
  ^I   = inverse text on  
  ^i   = inverse text off
  ^~   = reset all
  ^U   = underline on
  ^u   = underline off
  ^^   = escape a caret, ^^r = ^r

```

# Example #

The following would print in dim green with the word 'gold' bolded (brighter green) and 'Eugene Levy' in bright red text.  Then the text is reset to the terminal's default just before the exclamation point.

```
^gYou see a huge pile of ^!gold^. guarded by ^REugene Levy^~!
```