# -*- coding: windows-1252 -*- 
"""
    file:       loop.py
    
    project:    exam  -  python-test-runner
    
    subject:    this is the actual test-loop in exam for the TestRunner XML-RPC data distribution
    
    date:       22.03.2007

    author:     christoph menhorn

    department: MicroNova electronic GmbH

    phone:      0170 / 2980738

    e-mail:     Christoph.Menhorn@micronova.de

    history:

        22.03.2007    menhorn   start of programming
        20.02.2008    menhorn   add testAttributes to SystemDictionary
        03.04.2008    lemmerge  add sequenceList and parameterList to SystemDictionary
        15.05.2008    lemmerge  add additional runtime paths to windows search path
        20.11.2009    Schläfer  eliminated cTH from operation args

"""
# imports
import os.path, sys, time
import tracing
import teachAndReplay

# constants
STOP          = 0
INTERRUPT     = 1
RUN           = 2

TOPTESTCASEID = '00000000-0000-0000-0000-000000000000'

TYPE = 'pRunner.py'

# exceptions
interruptTestCase = 'interruptTestCase'

#*******************************************************************************
# function: mainLoop
#*******************************************************************************
def mainLoop():

    # append the python-search-path
    allPathes = cTH.server.TestRun.getRuntimePaths(sys.version_info[0], sys.version_info[1], sys.version_info[2])
    cTH.systemDictionary['runTimePathes'] = allPathes

    # loop reverse over found pathes
    for j in range (-len(allPathes),0):
        i=abs(j+1)
        # check the path existence
        if not(os.path.exists(allPathes[i])): raise IOError, 'the given run-time-path does not exist'
        # append operations-pathes to python-search-path
        sys.path.insert(0, str(allPathes[i]))
    
    # First we find the precise name of the path variable 
    sPath = "path"
    if "path" not in os.environ.keys():
        for sEnv in os.environ.keys():
            if sEnv.lower() == "path":
                sPath = sEnv
                break
        else:
            cTH.Print("No 'path' - environment variable found, we create one ourselves", "WARNING")

    # get exam defined code and module paths
    codePath = cTH.server.TestRun.getCodePath()
    coreModPath = cTH.server.TestRun.getCoreRuntimePath()
    stdModPath = cTH.server.TestRun.getStdRuntimePath()
    commonModPath = cTH.server.TestRun.getCommonRuntimePath()

    # detect additional user defined runtime paths and add them to windows search path
    for ap in allPathes:
        if ap[0:len(codePath)]      == codePath     or \
           ap[0:len(coreModPath)]   == coreModPath  or \
           ap[0:len(stdModPath)]    == stdModPath   or \
           ap[0:len(commonModPath)] == commonModPath:
            continue 
        # check if path is already in windows path, if not, add it to windows path
        if os.environ[sPath].find(ap) == -1:
            os.environ[sPath] = ap + ";" + os.environ[sPath]

    # get testState
    testState = cTH.server.TestRun.getTestRunState(TYPE)
        
    # loop over test-suites
    while ((testState != STOP) and (cTH.testRunState) ):
        try:
            commandLoop()
            testState = cTH.server.TestRun.getTestRunState(TYPE)
            while (testState == INTERRUPT):
                time.sleep(1)
                testState = cTH.server.TestRun.getTestRunState(TYPE)
        except:
            tracing.sendExceptionInfo()
        
    # reset existing plattform connections
    try:
        for key in cTH.systemDictionary['mappings'].keys():
            try:
                test = cTH.systemDictionary['mappings'][key].getAccess()
                cTH.systemDictionary['mappings'][key] = None
            except:
                pass
        cTH.rtp = None
    except:
        pass

#*******************************************************************************
# function: commandLoop
#*******************************************************************************
def commandLoop():
    # get next command
    command = cTH.server.TestRun.nextCommand(TYPE);
    try:
        if command[0] == "nextTestCase":
            # execute the test-case
                # get TestName and id
                cTH.systemDictionary['currentTestName'] = cTH.server.TestRun.getTestName()
                cTH.systemDictionary['currentTestCaseId'] = cTH.server.TestRun.getTestCaseId()
                cTH.systemDictionary['currentGroupName'] = cTH.server.TestRun.getTestGroup()
                
                #get TestAttributes
                cTH.systemDictionary['testAttributes'] = cTH.server.TestRun.getTestAttributes()
                
                # reset current test valuation
                cTH.systemDictionary['currentTestValuation']='info'

                # set Loglevel
                oldDefault = cTH.defaultLogLevel
                cTH.defaultLogLevel = cTH.server.TestRun.getLogLevel()
                
                # only change current level if default has changed
                if oldDefault <> cTH.defaultLogLevel:
                    cTH.logLevel = cTH.defaultLogLevel
                
                # update Teach and Replay mode for current testcase
                mode = cTH.server.TeachAndReplay.getMode()
                cTH.teachAndReplay.setMode(mode)
                
                # define the modul to be imported
                execFileName = command[1]
        
                # execute the module import
                exec('import ' + execFileName)
                
                # instance the class
                exec(execFileName + '.main()')
                
                # 50ms delay to let the TR finish logging
                # time.sleep(0.05)

        elif command[0] == "init":
            init()
        elif command[0] == "restart":
            lvl = "INFO"
            cTH.Print("*******************************************", lvl)
            cTH.Print("***          Restarting pRunner         ***", lvl)
            cTH.Print("*******************************************", lvl)
            cTH.testRunState = False
        elif command[0] == "exit":
            cTH.testRunState = False

    except interruptTestCase, type:
        pass
    except:
        tracing.sendExceptionInfo()
             
#*******************************************************************************
# function: init
#*******************************************************************************
def init():
    # check testrunState
    if cTH.server.TestRun.getTestRunState(TYPE)== STOP: return
    
    # set the SystemConfiguration
    cTH.setSystemConfiguration(cTH.server.TestRun.getSystemConfiguration())
    
    # set the Data
    cTH.systemDictionary['startTime'] = cTH.server.TestRun.getStartTime()
    cTH.systemDictionary['currentTestSuite'] = cTH.server.TestRun.getTestSuite()
    cTH.systemDictionary['currentCampaignName'] = cTH.server.TestRun.getTestCampaign()
    
    # Read all TestSuite attributes and store them in the system dictionary
    # the name of the sub-dictionary is "coverInformation" for backward compatibility 
    # (there used to be only the special attributes like project, title, operator, etc.  in there)
    cTH.systemDictionary['coverInformation'] = {}
    attributes = cTH.server.TestRun.getTestSuiteAttributes()
    for key, value in attributes.items():
        
        # translate the original names to the ones used in python to ensure backward compatibility
        if key == 'operator':
            key = 'coverOperatorName'
        elif key == 'comment':
            key = 'coverComment'
        elif key == 'subject':
            key = 'coverSubject'
        elif key == 'project':
            key = 'coverProject'
        elif key == 'department':
            key = 'coverOperatorDepartment'
        elif key == 'phone':
            key = 'coverOperatorPhone'
        elif key == 'mail':
            key = 'coverOperatorMail'
        elif key == 'title':
            key = 'coverTitle'
        
        cTH.systemDictionary['coverInformation'][key] = value
    
    # set the Report Pathes 
    cTH.systemDictionary['reportPath'] = cTH.server.TestRun.getReportPath()
    cTH.systemDictionary['reportName'] = cTH.server.TestRun.getReportName()
    # set working path to report-folder
    os.chdir(cTH.systemDictionary['reportPath'])
    
    # set Loglevel
    oldDefault = cTH.defaultLogLevel
    cTH.defaultLogLevel = cTH.server.TestRun.getLogLevel()
    
    # only change current level if default has changed
    if oldDefault <> cTH.defaultLogLevel:
        cTH.logLevel = cTH.defaultLogLevel

    cTH.systemDictionary['parameterList']   = []
    cTH.systemDictionary['sequenceList']    = []
    
    # register python version
    cTH.resultDataHandle.appendVersionDataItem('Python', sys.version, ['Versions', 'Environment', 'Python'])
    
    # print mode
    if cTH.server.TeachAndReplay.getGlobalMode() == teachAndReplay.REPLAY:
        cTH.Print('Teach and Replay mode: REPLAY', 'EXECUTION')
        cTH.resultDataHandle.appendMetaDataItem("Teach and Replay-Mode", "REPLAY", ["Testrun"])
    
    # print message if debug mode    
    if cTH.server.TestRun.getLaunchMode() == "debug":
        cTH.Print("DEBUG mode enabled", "EXECUTION")
        cTH.resultDataHandle.appendMetaDataItem("Debug-Mode", "enabled", ["Testrun"])
    
