import os
from nose.plugins.base import Plugin

import traceback
import datetime
import cgi

class NoseHTML( Plugin ):
    """
    Styled HTML output plugin for nose.
    """

    def help(self):
        return "Output HML report of test status into reportfile (specifiable with --html-report-file"

    def add_options(self, parser, env=os.environ):
        Plugin.add_options(self, parser, env)
        parser.add_option("--html-report-file", action="store", default="nose_report.xml", dest="report_file", help="File to output XML report to")
    
    def configure(self, options, config):
        Plugin.configure(self, options, config)
        self.conf = config
        self.report_fname = options.report_file

    def begin(self):
        """ If a file already exists and --xml-accumulate is set, we add into that, otherwise, create a new one """
        self.counter = 0
        self.report_file = open( self.report_fname, "w" )
        print >> self.report_file, HTML_START
        self.report_file.flush()
        
    def finalize(self, result):
        """ Write out report as serialized XML """
        print >> self.report_file, HTML_END
        self.report_file.close()

    def print_test( self, status, test, error=None ):
        self.counter += 1
        print >> self.report_file, "<div class='test %s'>" % status
        if test.id():
            print >> self.report_file, "<div><span class='label'>ID:</span> %s</div>" % test.id()
        if test.shortDescription():
            print >> self.report_file, "<div><span class='label'>Description:</span> %s</div>" % test.shortDescription()
        if status:
            print >> self.report_file, "<div><span class='label'>Status:</span> %s</div>" % status
        if test.capturedOutput:
            print >> self.report_file, "<div><span class='label'>Output:</span> <a href=\"javascript:toggle('capture_%d')\">...</a></div>" % self.counter
            print >> self.report_file, "<div id='capture_%d' style='display: none'><pre class='capture'>%s</pre></div>" % ( self.counter, cgi.escape( test.capturedOutput ) )
        if hasattr( test, 'capturedLogging' ) and test.capturedLogging:
            print >> self.report_file, "<div><span class='label'>Log:</span> <a href=\"javascript:toggle('capture_%d')\">...</a></div>" % self.counter
            print >> self.report_file, "<div id='capture_%d' style='display: none'><pre class='capture'>%s</pre></div>" % ( self.counter, cgi.escape( "\n".join( test.capturedLogging ) ) )
        if error:
            print >> self.report_file, "<div><span class='label'>Exception:</span> <a href=\"javascript:toggle('exception_%d')\">...</a></div>" % self.counter
            print >> self.report_file, "<div id='exception_%d' style='display: none'><pre class='exception'>%s</pre></div>" % ( self.counter, cgi.escape( error ) )
        print >> self.report_file, "</div>"
        self.report_file.flush()

    def addSkip(self, test):
        """
        Test was skipped
        """
        self.print_test( 'skipped', test )
        
    def addSuccess(self, test ):
        """
        Test was successful
        """
        self.print_test( 'success', test )
            
    def addFailure(self, test, error ):
        """
        Test failed
        """
        self.print_test( 'failure', test, '\n'.join( traceback.format_exception( *error ) ) )

    def addError(self, test, error ):
        """
        Test errored.
        """
        capture = test.capturedOutput
        self.print_test( 'error', test, '\n'.join( traceback.format_exception( *error ) ) )
    
    def addDeprecated(self, test):
        """
        Test is deprecated
        """
        capture = test.capturedOutput
        self.print_test( 'deprecated', test )

HTML_START = """
<html>
<head>
<style>

body
{
  font: 12px verdana, "Bitstream Vera Sans", geneva, arial, helvetica, helve, sans-serif;
  line-height: 160%;
}

div.test
{
  margin: 5px;
  padding: 5px;
  border: solid black 1px;
  background: lightgray;
}

div.success
{
  background: #CCFFCC;
  border: solid #66AA66 1px;
}

div.error, div.failure
{
  background: #FFCCCC;
  border: solid #AA6666 1px;
}

span.label
{
  font-weight: bold;
}

pre
{
  background: white;
  padding: 5px;
  border:  solid black 1px;
  display: block;
  overflow: auto;
}
</style>

<script>
function toggle(name){
	var elem = document.getElementById(name)
	if (elem) {
		if (elem.style.display=="none"){
			elem.style.display="block"
		} else {
			elem.style.display="none"
		}
	}
}
</script>
</head>
<body>
"""

HTML_END = """
</body>
</html>
"""
