#!/usr/bin/env python
#-*- coding:utf8 -*-

import os, sys
import unittest
import logging

#在这里添加要进行单元测试的源码目录名
codeArray = ["ConfParser", "JsonUtil", "LoggerController", "MySqlUtil", "PublisherSubscriber", "EmailSender", "EmailController"]

rootPath = os.path.abspath(os.path.join(__file__, "../.."))
for codeName in codeArray:
    sourceCodeDir = os.path.abspath(os.path.join(rootPath, codeName, "Code"))
    if os.path.exists(sourceCodeDir):
        sys.path.append(sourceCodeDir)
        
#导入源码
from JsonUtil import *
from ConfParser import *
from EmailSender import *

etcPath = os.path.join(os.path.join(__file__, "../etc"))

class MyUnitTest(unittest.TestCase):
    def setUp(self):
        #初始化测试类
        confPath = os.path.abspath(os.path.join(etcPath, "ConfParser/test.conf"))
        self.testConfParser = ConfParser(confPath)

    def teardown(self):
        pass

    # JsonUtil的测试样例
    def test_getJsonFromFile(self):
        testJsonFile = os.path.abspath(os.path.join(etcPath, "JsonUtil/test1.json"))
        ret = getJsonFromFile(testJsonFile)
        self.assertEqual(ret, (True, {"A": "a","B": "b","C": 0,"D": "d","E": {"E1": "e1","E2": "e2","E3": 1}}))

        testJsonFile = os.path.abspath(os.path.join(etcPath, "JsonUtil/test2.json"))
        ret = getJsonFromFile(testJsonFile)
        self.assertEqual(ret, (True, [ "A", "B", "C", "D", "E"]))
        
        with self.assertLogs(jsonLogger) as log:
            testJsonFile = os.path.abspath(os.path.join(etcPath, "JsonUtil/None.json"))
            ret = getJsonFromFile(testJsonFile)
            self.assertFalse(ret[0])
            
            testJsonFile = os.path.abspath(os.path.join(etcPath, "JsonUtil/error.json"))
            ret = getJsonFromFile(testJsonFile)
            self.assertFalse(ret[0])

            errorStr1 = "exception is [Errno 2] No such file or directory: '/Users/wxj/workplace/MyProject/github/PyTestModule/etc/JsonUtil/None.json'"
            errorStr2 = "exception is Expecting value: line 7 column 11 (char 66)"
            self.assertEqual(log.output, ['ERROR:JsonUtil:%s'%errorStr1, 'ERROR:JsonUtil:%s'%errorStr2])
    
    def test_getJsonFromStr(self):
        jsonStr = "{\"A\": \"a\",\"B\": \"b\",\"C\": 0,\"D\": \"d\",\"E\": {\"E1\": \"e1\",\"E2\": \"e2\",\"E3\": 1}}"
        ret = getJsonFromStr(jsonStr)
        self.assertEqual(ret, (True, {"A": "a","B": "b","C": 0,"D": "d","E": {"E1": "e1","E2": "e2","E3": 1}}))

        jsonStr = "[\"A\", \"B\", \"C\", \"D\", \"E\"]"
        ret = getJsonFromStr(jsonStr)
        self.assertEqual(ret, (True, [ "A", "B", "C", "D", "E"]))
        
        with self.assertLogs(jsonLogger) as log:
            jsonStr = "{\"A\": \"a\",B\": \"b\",\"C\": 0,\"D\": \"d\",\"E\": {\"E1\": \"e1\",\"E2\": \"e2\",\"E3\": 1}}"
            ret = getJsonFromStr(jsonStr)
            self.assertFalse(ret[0])
            errorStr = "exception is Expecting property name enclosed in double quotes: line 1 column 11 (char 10)"
            self.assertEqual(log.output, ["ERROR:JsonUtil:%s"%errorStr])
        
    def test_valueFromJsonFile(self):
        testJsonFile = os.path.abspath(os.path.join(etcPath, "JsonUtil/test3.json"))
        ret = valueFromJsonFile("A", testJsonFile)
        self.assertEqual(ret, 'a')

        ret = valueFromJsonFile("C", testJsonFile)
        self.assertEqual(ret, 7)

        ret = valueFromJsonFile("A", testJsonFile)
        self.assertEqual(ret, 'a')

        ret = valueFromJsonFile('E', testJsonFile)
        self.assertEqual(ret, {"E1": 'e1', 'E2': 'e2', "E3": 1})

        ret = valueFromJsonFile('F', testJsonFile)
        self.assertEqual(ret, 8.10)

        ret = valueFromJsonFile('G', testJsonFile)
        self.assertEqual(ret, ["g1", "g2", "g3"])

        ret = valueFromJsonFile('K', testJsonFile)
        self.assertFalse(ret)
        
        ret = valueFromJsonFile('H', testJsonFile)
        self.assertEqual(ret, "H测试")

        ret = valueFromJsonFile('测试', testJsonFile)
        self.assertEqual(ret, "测试结果")

        testJsonFile = os.path.abspath(os.path.join(etcPath, "JsonUtil/error.json"))
        ret = valueFromJsonFile('D', testJsonFile)
        self.assertFalse(ret)
    
    def test_valeFromJsonStr(self):
        jsonStr = "{\"A\": \"a\", \"B\": \"b\", \"C\": 7, \"D\": \"d\", \"E\": {\"E1\": \"e1\", \"E2\": \"e2\", \"E3\": 1}, \"F\": 8.1, \"G\": [\"g1\", \"g2\", \"g3\"], \"测试\": \"中文测试\"}"

        ret = valueFromJsonStr("A", jsonStr)
        self.assertEqual(ret, 'a')

        ret = valueFromJsonStr("C", jsonStr)
        self.assertEqual(ret, 7)

        ret = valueFromJsonStr("A", jsonStr)
        self.assertEqual(ret, 'a')

        ret = valueFromJsonStr('E', jsonStr)
        self.assertEqual(ret, {"E1": 'e1', 'E2': 'e2', "E3": 1})

        ret = valueFromJsonStr('F', jsonStr)
        self.assertEqual(ret, 8.10)

        ret = valueFromJsonStr('G', jsonStr)
        self.assertEqual(ret, ["g1", "g2", "g3"])

        ret = valueFromJsonStr('K', jsonStr)
        self.assertFalse(ret)

        ret = valueFromJsonStr('测试', jsonStr)
        self.assertEqual(ret, "中文测试")

        jsonStr = "{\"A\": a\", \"B\": \"b\", \"C\": 7, \"D\": \"d\", \"E\": {\"E1\": \"e1\", \"E2\": \"e2\", \"E3\": 1}, \"F\": 8.1, \"G\": [\"g1\", \"g2\", \"g3\"]}"
        ret = valueFromJsonStr('B', jsonStr)
        self.assertFalse(ret)
    
    def test_saveJsonFile(self):
        saveFile1 = os.path.abspath(os.path.join(etcPath, "JsonUtil/save1.json"))
        jsonData = {"A": "a", "B": "b", "C": 7, "D": "d", "E": {"E1": "e1", "E2": "e2", "E3": 1}, "F": 8.1, "G": ["g1", "g2", "g3"], u"测试": u"中文测试"}
        ret = saveJsonFile(saveFile1, jsonData)
        self.assertEqual(ret, (True, "success"))
        
        ret = saveJsonFile(saveFile1, jsonData)
        self.assertEqual(ret, (True, "success"))

        saveFile3 = os.path.abspath(os.path.join(etcPath, "JsonUtil/save3.json"))
        ret = saveJsonFile(saveFile3, "测试一下")
        self.assertEqual(ret, (True, "success"))

        saveFile4 = os.path.abspath(os.path.join(etcPath, "JsonUtil/save4.json"))
        ret = saveJsonFile(saveFile4, 88)
        self.assertEqual(ret, (True, "success"))
    
    def test_getDefaultFromJsonObj(self):
        testJsonFile = os.path.abspath(os.path.join(etcPath, "JsonUtil/test4.json"))
        result, jsonObj = getJsonFromFile(testJsonFile)
        result = getDefaultFromJsonObj("A", jsonObj)
        self.assertEqual(result, ('a', 'success'))

        result = getDefaultFromJsonObj("B", jsonObj)
        self.assertEqual(result, ('b', 'success'))

        result = getDefaultFromJsonObj("E", jsonObj)
        self.assertEqual(result, ({"E1": "e1", "E2": "e2", "E3": 1}, 'success'))
        
        result = getDefaultFromJsonObj("测试", jsonObj)
        self.assertEqual(result, ("测试结果", 'success'))

        result = getDefaultFromJsonObj("H", jsonObj)
        self.assertEqual(result, ("H测试", 'success'))

        result = getDefaultFromJsonObj("default", jsonObj)
        self.assertEqual(result, ({"de1": "default1","默认": "默认1","默认2": "默认2"}, 'success'))
        
        result = getDefaultFromJsonObj("my test key", jsonObj)
        self.assertEqual(result, ("my test key", 'success'))
        
        result = getDefaultFromJsonObj(" ", jsonObj)
        self.assertEqual(result, ({"de1": "default1","默认": "默认1","默认2": "默认2"}, 'success'))
        
        result = getDefaultFromJsonObj("G", jsonObj)
        self.assertEqual(result, (["g1", "g2", "g3"], 'success'))
        
        with self.assertLogs(jsonLogger) as log:
            result = getDefaultFromJsonObj("test5", jsonObj)
            self.assertEqual(result, ({"test51": "333","test52": "444"}, 'success'))

            tempResult = getDefaultFromJsonObj("test53", result[0])
            self.assertEqual(tempResult, (None, "test53 is not found in jsonObj"))
            result = getDefaultFromJsonObj(None, jsonObj)
            self.assertEqual(result, (None, 'key or jsonObj is None'))

            result = getDefaultFromJsonObj("", jsonObj)
            self.assertEqual(result, (None, 'key or jsonObj is None'))
            
            result = getDefaultFromJsonObj("H", None)
            self.assertEqual(result, (None, 'key or jsonObj is None'))
            
            result = getDefaultFromJsonObj("H", "")
            self.assertEqual(result, (None, 'key or jsonObj is None'))

            self.assertEqual(log.output, ["ERROR:JsonUtil:test53 is not found in jsonObj", "ERROR:JsonUtil:key or jsonObj is None", "ERROR:JsonUtil:key or jsonObj is None", "ERROR:JsonUtil:key or jsonObj is None", "ERROR:JsonUtil:key or jsonObj is None"])
        
        result = getDefaultFromJsonObj("H", " ")
        self.assertEqual(result, (" ", "success"))

        result = getDefaultFromJsonObj('"\\"', jsonObj)
        self.assertEqual(result, ("特殊测试", "success"))

        result = getDefaultFromJsonObj('test', 33)
        self.assertEqual(result, (33, "success"))
        
        result = getDefaultFromJsonObj('test', "测试")
        self.assertEqual(result, ("测试", "success"))
        
        result = getDefaultFromJsonObj('test', "test a string")
        self.assertEqual(result, ("test a string", "success"))
        
        result = getDefaultFromJsonObj('test', 77.8)
        self.assertEqual(result, (77.8, "success"))
        
        result = getDefaultFromJsonObj('test', [33, 55, 88, 66])
        self.assertEqual(result, ([33, 55, 88, 66], "success"))
        
        result = getDefaultFromJsonObj('test', ("success", {"A": 1, "B": 2}, [22.7, 33.6, 55.4]))
        self.assertEqual(result, (("success", {"A": 1, "B": 2}, [22.7, 33.6, 55.4]), "success"))
    
    #ConfParser的测试样例
    def test_getValueFromConf(self):
        confName = os.path.abspath(os.path.join(etcPath, "ConfParser/test.conf"))
        result = getValueFromConf(confName, "Test1", "test1")
        self.assertEqual(result, (True, "success", "1"))

        result = getValueFromConf(confName, "Test2", "test12")
        self.assertEqual(result, (True, "success", "test222"))

        result = getValueFromConf(confName, "Test1", "test3")
        self.assertEqual(result, (True, "success", "测试样例"))

        result = getValueFromConf(confName, "Test1", "测试")
        self.assertEqual(result, (True, "success", "测试样例2"))

        result = getValueFromConf(confName, "Test1", "test4")
        self.assertEqual(result, (True, "success", "55.77"))

        result = getValueFromConf(confName, "Test3", "test33")
        self.assertEqual(result, (True, "success", ""))

        result = getValueFromConf(confName, "Test3", "test44")
        self.assertEqual(result, (True, "success", "=676"))

        with self.assertLogs(confLogger) as log:
            result = getValueFromConf(confName, "Test3", "test55")
            self.assertFalse(result[0])
            
            result = getValueFromConf(confName, "Test2", "test6")
            self.assertFalse(result[0])

            result = getValueFromConf(None, "test", "test")
            self.assertFalse(result[0])

            result = getValueFromConf(confName, None, "test")
            self.assertFalse(result[0])

            result = getValueFromConf(confName, "Test3", None)
            self.assertFalse(result[0])
            
            result = getValueFromConf("", "Test3", "test")
            self.assertFalse(result[0])

            result = getValueFromConf("/Temp1/Temp2/Temp3", "Test3", "test")
            self.assertFalse(result[0])
            
            errorConfName = os.path.abspath(os.path.join(etcPath, "ConfParser/error.conf"))
            result = getValueFromConf(errorConfName, "Test2", "test11")
            self.assertFalse(result[0])
            
            errorStr1 = "get value from %s error, error is No option 'test55' in section: 'Test3'" % confName
            errorStr2 = "get value from %s error, error is No option 'test6' in section: 'Test2'" % confName
            errorStr3 = "confFileName is None"
            errorStr4 = "option is None"
            errorStr5 = "key is None"
            errorStr6 = "confFileName is None"
            errorStr7 = "/Temp1/Temp2/Temp3 is not a file"
            errorStr8 = "get value from %s error, error is Source contains parsing errors: '%s'\n\t[line 20]: '[Test4\\n'"%(errorConfName, errorConfName)
            self.assertEqual(log.output, ['ERROR:ConfParser:%s'% errorStr1, 'ERROR:ConfParser:%s'% errorStr2, 'ERROR:ConfParser:%s'% errorStr3, 'ERROR:ConfParser:%s'% errorStr4, 'ERROR:ConfParser:%s'% errorStr5, 'ERROR:ConfParser:%s'% errorStr6, 'ERROR:ConfParser:%s'% errorStr7, 'ERROR:ConfParser:%s'% errorStr8])
            
    def test_getValueWithDefault(self):
        confName = os.path.abspath(os.path.join(etcPath, "ConfParser/test.conf"))
        result = getValueWithDefault(confName, "Test1", "test1", "2")
        self.assertEqual(result, "1")

        result = getValueWithDefault(confName, "Test2", "test12", "333")
        self.assertEqual(result, "test222")

        result = getValueWithDefault(confName, "Test1", "test3", "测试")
        self.assertEqual(result, "测试样例")

        result = getValueWithDefault(confName, "Test1", "测试", 333)
        self.assertEqual(result, "测试样例2")

        result = getValueWithDefault(confName, "Test1", "test4", 88.7)
        self.assertEqual(result, "55.77")

        result = getValueWithDefault(confName, "Test3", "test33", "test")
        self.assertEqual(result, "")

        result = getValueWithDefault(confName, "Test3", "test44", "nottest")
        self.assertEqual(result, "=676")

        result = getValueWithDefault(confName, "Test3", "test55", 8)
        self.assertEqual(result, 8)
        
        result = getValueWithDefault(confName, "Test2", "test6", "测试结果")
        self.assertEqual(result, "测试结果")

        result = getValueWithDefault(None, "test", "test", 37.8)
        self.assertEqual(result, 37.8)

        result = getValueWithDefault(confName, None, "test", "test2")
        self.assertEqual(result, "test2")
        
        result = getValueWithDefault(confName, "Test3", None, None)
        self.assertEqual(result, None)
        
        result = getValueWithDefault("", "Test3", "test", "testresult")
        self.assertEqual(result, "testresult")

        result = getValueWithDefault("/Temp1/Temp2/Temp3", "Test3", "test", None)
        self.assertEqual(result, None)

        errorConfName = os.path.abspath(os.path.join(etcPath, "ConfParser/error.conf"))
        result = getValueWithDefault(errorConfName, "Test2", "test11", "error")
        self.assertEqual(result, "error")
    
    def test_Class_ConfParser_init(self):
        with self.assertLogs(confLogger) as log:
            tempConfParser = ConfParser("/Temp1/Temp2/Temp3")
            self.assertEqual(log.output, ['ERROR:ConfParser:/Temp1/Temp2/Temp3 is not a file'])

    def test_Class_ConfParser_getValue(self):
        result = self.testConfParser.getValue("Test1", "test1")
        self.assertEqual(result, "1")

        result = self.testConfParser.getValue("Test2", "test12")
        self.assertEqual(result, "test222")

        result = self.testConfParser.getValue("Test1", "test3")
        self.assertEqual(result, "测试样例")

        result = self.testConfParser.getValue("Test1", "测试")
        self.assertEqual(result, "测试样例2")

        result = self.testConfParser.getValue("Test1", "test4")
        self.assertEqual(result, "55.77")

        result = self.testConfParser.getValue("Test3", "test33")
        self.assertEqual(result, "")

        result = self.testConfParser.getValue("Test3", "test44")
        self.assertEqual(result, "=676")

        result = self.testConfParser.getValue("Test3", "test55")
        self.assertEqual(result, None)
        
        result = self.testConfParser.getValue("Test2", "test6")
        self.assertEqual(result, None)

        result = self.testConfParser.getValue("test", "test")
        self.assertEqual(result, None)

        result = self.testConfParser.getValue(None, "test")
        self.assertEqual(result, None)
        
        result = self.testConfParser.getValue("Test3", None)
        self.assertEqual(result, None)
        
        result = self.testConfParser.getValue("Test3", "test")
        self.assertEqual(result, None)

        with self.assertLogs(confLogger) as log:
            errorConfPath = os.path.abspath(os.path.join(etcPath, "ConfParser/error.conf"))
            parserResult = ConfParser(errorConfPath)
            errorStr = "init ConfParser error, error is Source contains parsing errors: '/Users/wxj/workplace/MyProject/github/PyTestModule/etc/ConfParser/error.conf'\n\t[line 20]: '[Test4\\n'"
            self.assertEqual(log.output, ["ERROR:ConfParser:%s"%errorStr])
            
            result = parserResult.getValue("Test2", "test11")
            self.assertEqual(result, "11")
    
    def test_Class_ConfParser_getValueWithDefault(self):
        result = self.testConfParser.getValueWithDefault("Test1", "test1", 1)
        self.assertEqual(result, "1")

        result = self.testConfParser.getValueWithDefault("Test2", "test12", "test3")
        self.assertEqual(result, "test222")

        result = self.testConfParser.getValueWithDefault("Test1", "test3", 99.7)
        self.assertEqual(result, "测试样例")

        result = self.testConfParser.getValueWithDefault("Test1", "测试", "default")
        self.assertEqual(result, "测试样例2")

        result = self.testConfParser.getValueWithDefault("Test1", "test4", "55.88")
        self.assertEqual(result, "55.77")

        result = self.testConfParser.getValueWithDefault("Test3", "test33", 'abc')
        self.assertEqual(result, "abc")

        result = self.testConfParser.getValueWithDefault("Test3", "test44", 'test')
        self.assertEqual(result, "=676")

        result = self.testConfParser.getValueWithDefault("Test3", "test55", 'a')
        self.assertEqual(result, 'a')
        
        result = self.testConfParser.getValueWithDefault("Test2", "test6", "测试结果")
        self.assertEqual(result, "测试结果")

        result = self.testConfParser.getValueWithDefault("test", "test", 22)
        self.assertEqual(result, 22)

        result = self.testConfParser.getValueWithDefault(None, "test", "testresult")
        self.assertEqual(result, "testresult")
        
        result = self.testConfParser.getValueWithDefault("Test3", None, "temp")
        self.assertEqual(result, "temp")
        
        result = self.testConfParser.getValueWithDefault("Test3", "test", 66.7)
        self.assertEqual(result, 66.7)
        
        errorConfPath = os.path.abspath(os.path.join(etcPath, "ConfParser/error.conf"))
        parserResult = ConfParser(errorConfPath)
        result = parserResult.getValueWithDefault("Test2", "test11", "test33")
        self.assertEqual(result, "11")
        
    def test_Class_ConfParser_getIntWithDefault(self):
        result = self.testConfParser.getIntWithDefault("Test1", "test1", 1)
        self.assertEqual(result, 1)

        result = self.testConfParser.getIntWithDefault("Test2", "test12", "test3")
        self.assertEqual(result, None)

        result = self.testConfParser.getIntWithDefault("Test1", "test3", 99.7)
        self.assertEqual(result, None)

        result = self.testConfParser.getIntWithDefault("Test1", "测试", "default")
        self.assertEqual(result, None)

        result = self.testConfParser.getIntWithDefault("Test1", "test4", "55.88")
        self.assertEqual(result, 55)

        result = self.testConfParser.getIntWithDefault("Test3", "test33", 'abc')
        self.assertEqual(result, None)

        result = self.testConfParser.getIntWithDefault("Test3", "test44", 'test')
        self.assertEqual(result, None)

        result = self.testConfParser.getIntWithDefault("Test3", "test55", 'a')
        self.assertEqual(result, None)
        
        result = self.testConfParser.getIntWithDefault("Test2", "test6", "测试结果")
        self.assertEqual(result, None)

        result = self.testConfParser.getIntWithDefault("test", "test", 22)
        self.assertEqual(result, 22)

        result = self.testConfParser.getIntWithDefault("test", "test", -2)
        self.assertEqual(result, -2)

        result = self.testConfParser.getIntWithDefault(None, "test", "testresult")
        self.assertEqual(result, None)
        
        result = self.testConfParser.getIntWithDefault("Test3", None, "temp")
        self.assertEqual(result, None)
        
        result = self.testConfParser.getIntWithDefault("Test3", "test", 66.7)
        self.assertEqual(result, 66)

        result = self.testConfParser.getIntWithDefault("Test2", "test7", 66)
        self.assertEqual(result, -33)
        
        errorConfPath = os.path.abspath(os.path.join(etcPath, "ConfParser/error.conf"))
        parserResult = ConfParser(errorConfPath)
        result = parserResult.getIntWithDefault("Test2", "test11", "test33")
        self.assertEqual(result, 11)  
    
    #EmailSender的测试样例
    def test_sendEmail(self):
        attach1 = os.path.abspath(os.path.join(__file__, "../README.md"))
        result = sendEmail('smtp.qq.com', '***@qq.com', '***', ['***@qq.com', '***@qq.com'], '**<***@qq.com>, **<***@qq.com>', "测试邮件", "这是一封测试邮件", {attach1: "log1"})
        self.assertFalse(result)
        #result = sendEmail('smtp.qq.com', '***@qq.com', '***', ['***@qq.com', '***@qq.com'], '**<***@qq.com>, **<***@qq.com>', "测试邮件", "这是一封测试邮件", {attach1: "log1"})
        #self.assertTrue(result)
        
if __name__ == "__main__":
    unittest.main()
    '''
    suite = unittest.TestSuite()
    suite.addTest(MyUnitTest("test_sendEmail"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    '''