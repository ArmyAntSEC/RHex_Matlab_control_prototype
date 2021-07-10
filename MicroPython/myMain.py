from MotorController.MotorDriver import MotorDriver
from machine import Pin
from machine import PWM
from sys import exit
import utime
from TaskScheduler.TaskScheduler import TackScheduler
from TaskScheduler.IRecurringTask import IRecurringTask
from TaskScheduler.IFutureTask import IFutureTask
from NonBlockingRead import NonBlockingRead
from LogPrinter import LogPrinter

class Beacon(IRecurringTask):
    def __init__(self):
        IRecurringTask.__init__(self, 10000000)

    def run( self ):
        LogPrinter ( "Beacon!" )

class mainFunc:
    def __init__( self ):
        LogPrinter ( "Hello Again World!" )    
            
        m1ena = Pin(3, Pin.OUT )
        m1enb = Pin(4, Pin.OUT )
        m1pwm = PWM(Pin(5))
        m1pwm.freq(1000)    

        self.driver1 = MotorDriver()
        self.driver1.config ( m1ena, m1enb, m1pwm )

        self.taskScheduler = TackScheduler()   
        self.taskScheduler.addTask( Beacon() )
        
        self.commands = {
            "info": self.cmdInfo,
            "simpleMove": self.cmdSimpleMove,
            "stats": self.cmdStats,
            "exit": self.cmdExit            
        }

        # Start the infitine loop
        self.run()


    def commandParser( self, command: str ):
        """Parses a single input command. Should return immediately"""
        if  ( command in self.commands ):
            self.commands[command]()
        else:
            LogPrinter ( "Unknown command: ", command )
            LogPrinter ( "Supported commands:" )
            for key in self.commands.keys(): 
                LogPrinter ( "- ", key )
                
            

    def run(self): 
        LogPrinter ( "Running loop" )
        reader = NonBlockingRead( self.commandParser )

        while True:        
            reader()
            self.taskScheduler.run()            

    def cmdInfo(self):
        LogPrinter ( "This is the info" )
    
    def cmdSimpleMove(self):
        LogPrinter ( "Doing a simple move" ); 
        self.driver1.setMotorPWM(0.25)                
        
        def stopFun():
            self.driver1.setMotorPWM(0)            
            LogPrinter ( "Done with simple move" );         
        self.taskScheduler.addTask( IFutureTask(int(2e6),stopFun,self.taskScheduler) )

    def cmdStats(self):
        self.taskScheduler.printStats()

    def cmdExit(self):
        self.driver1.setMotorPWM(0)
        exit()

mainFunc()
