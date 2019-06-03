on run {input, parameters}
	tell application "Finder"
		set myTarget to path to home folder
		my openTerminal(myTarget)
	end tell
end run

on openTerminal(location)
	tell application "iTerm"
		activate
		set myterm to (make new terminal)
		tell myterm
			launch session "Virtuoso"
			set number of columns to 144
			set number of rows to 73
			set _session1 to current session
			tell _session1
				write text "virtuoso-start"
			end tell
			
			tell i term application "System Events" to keystroke "h" using control down
			tell the last session to write text "redis-server"
			
			tell i term application "System Events" to keystroke "h" using control down
			tell the last session to write text "/Users/sestari/Documents/elasticsearch-7.1.0/bin/elasticsearch -s"
			
			tell i term application "System Events" to keystroke "h" using control down
                tell the last session to write text "/Users/sestari/Documents/apache-activemq-5.15.9/bin/macosx/activemq console"
			
		end tell
	end tell
end openTerminal
