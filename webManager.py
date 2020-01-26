import cherrypy
import Pyro4

class web:
    def __init__ ( self ):
        self.screens = list()
        #self.screens.append ( Pyro4.Proxy ( "PYRONAME:scoreboard1" ) )
        self.screens.append ( Pyro4.Proxy ( "PYRONAME:scoreboard2" ) )
        #self.screens.append ( Pyro4.Proxy ( "PYRONAME:scoreboard3" ) )
        #self.screens.append ( Pyro4.Proxy ( "PYRONAME:scoreboard4" ) )

        for screen in self.screens:
            screen.drawTitle()
            screen.update()

    @cherrypy.expose
    def index ( self ):
        html = """
           <head>
              <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.js"></script>
              <script>
                 function adjustScore ( screen )
                 {
                    obj = new Object();
                    obj.screen = screen;
                    obj.delta = $ ( "#scoreInput" + screen ).val();

                    $.post ( "adjustScore" , obj , function ( data ) {
                       $ ( "#scoreInput" + screen ).val( "" );
                    } );
                 }

                 function adjustTitle ( screen )
                 {
                    obj = new Object();
                    obj.screen = screen;
                    obj.name = $ ( "#titleInput" + screen ).val();

                    $.post ( "updateTitle" , obj , function ( data ) {
                       $ ( "#titleInput" + screen ).val( "" );
                    } );
                 }

                 function resetTitles()
                 {
                    obj = new Object();
                    obj.screen = 1;
                    obj.name = "LEADERS";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                    obj = new Object();
                    obj.screen = 2;
                    obj.name = "ARTS";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                    obj = new Object();
                    obj.screen = 4;
                    obj.name = "SPORTS";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                    obj = new Object();
                    obj.screen = 3;
                    obj.name = "PRE-K";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                 }

                 function caseyVince()
                 {
                    obj = new Object();
                    obj.screen = 1;
                    obj.name = "";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                    obj = new Object();
                    obj.screen = 2;
                    obj.name = "VINCE";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                    obj = new Object();
                    obj.screen = 4;
                    obj.name = "CASEY";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                    obj = new Object();
                    obj.screen = 3;
                    obj.name = "";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                 }

                 function vinceCasey()
                 {
                    obj = new Object();
                    obj.screen = 1;
                    obj.name = "";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                    obj = new Object();
                    obj.screen = 2;
                    obj.name = "CASEY";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                    obj = new Object();
                    obj.screen = 4;
                    obj.name = "VINCE";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                    obj = new Object();
                    obj.screen = 3;
                    obj.name = "";

                    $.post ( "updateTitle" , obj , function ( data ) {
                    } );

                 }

                 function startTimers()
                 {
                    $.post ( "startTimers" );
                 }
              </script>
           </head>

           <h3>Adjust Score</h3>
           <div>Leaders <input type='text' id='scoreInput1'><input type='button' onclick='adjustScore ( 1 )' value='Adjust'></div>
           <div>Arts <input type='text' id='scoreInput2'><input type='button' onclick='adjustScore ( 2 )' value='Adjust'></div>
           <div>Pre-K <input type='text' id='scoreInput3'><input type='button' onclick='adjustScore ( 3 )' value='Adjust'></div>
           <div>Sports <input type='text' id='scoreInput4'><input type='button' onclick='adjustScore ( 4 )' value='Adjust'></div>

           <h3>Adjust Title</h3>
           <div>Leaders <input type='text' [UCC:intervewer-intervewee][/UCC]
titleInput1'><input type='button' onclick='adjustTitle ( 1 )' value='Adjust'></div>
           <div>Arts <input type='text' id='titleInput2'><input type='button' onclick='adjustTitle ( 2 )' value='Adjust'></div>
           <div>Sports <input type='text' id='titleInput4'><input type='button' onclick='adjustTitle ( 4 )' value='Adjust'></div>
           <div>Pre-K <input type='text' id='titleInput3'><input type='button' onclick='adjustTitle ( 3 )' value='Adjust'></div>

           <div><input type='button' value='Reset Titles' onclick='resetTitles()'></div>
           <div><br><br><input type='button' value='Start Timers' onclick='startTimers()'></div>
           <div><br><br><input type='button' value='Vince Casey' onclick='vinceCasey()'></div>
           <div><br><br><input type='button' value='Casey Vince' onclick='caseyVince()'></div>


        """
        return html

    @cherrypy.expose
    def updateTitle ( self , screen , name ):
        self.screens [ int ( screen ) - 1 ].updateTitle ( str ( name ) )

    @cherrypy.expose
    def adjustScore ( self , screen , delta ):
        self.screens [ int ( screen ) - 1 ].updateScore ( int ( delta ) )

    @cherrypy.expose
    def startTimers ( self ):
        for screen in self.screens:
            screen.startTimer()

        firstPlace = False
        while firstPlace == False:
            for screen in self.screens:
                if screen.timerRunning() == False:
                    screen.updateTitle ( "WINNER" )
                    firstPlace = True


cherrypy.server.socket_host = "0.0.0.0"
cherrypy.quickstart ( web() , "/" )