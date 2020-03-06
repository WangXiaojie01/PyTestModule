#!/usr/bin/env python
#-*- coding:utf8 -*-

import os, sys
import unittest

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
        pass

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
        
        testJsonFile = os.path.abspath(os.path.join(etcPath, "JsonUtil/None.json"))
        print(type(testJsonFile))
        ret = getJsonFromFile(testJsonFile)
        self.assertLogs(ret, "exception is [Errno 2] No such file or directory: '/Users/wxj/workplace/MyProject/github/PyTestModule/etc/JsonUtil/None.json")
        self.assertEqual(ret, (False, "[Errno 2] No such file or directory: '/Users/wxj/workplace/MyProject/github/PyTestModule/etc/JsonUtil/None.json'"))
        
        testJsonFile = os.path.abspath(os.path.join(etcPath, "JsonUtil/error.json"))
        ret = getJsonFromFile(testJsonFile)
        if sys.version_info.major == 3:
            self.assertLogs(ret, "exception is Expecting value: line 7 column 11 (char 66)")
            self.assertEqual(ret, (False, "Expecting value: line 7 column 11 (char 66)"))
        
    def test_getJsonFromStr(self):
        jsonStr = "{\"A\": \"a\",\"B\": \"b\",\"C\": 0,\"D\": \"d\",\"E\": {\"E1\": \"e1\",\"E2\": \"e2\",\"E3\": 1}}"
        ret = getJsonFromStr(jsonStr)
        self.assertEqual(ret, (True, {"A": "a","B": "b","C": 0,"D": "d","E": {"E1": "e1","E2": "e2","E3": 1}}))

        jsonStr = "[\"A\", \"B\", \"C\", \"D\", \"E\"]"
        ret = getJsonFromStr(jsonStr)
        self.assertEqual(ret, (True, [ "A", "B", "C", "D", "E"]))
        
        jsonStr = "{\"A\": \"a\",B\": \"b\",\"C\": 0,\"D\": \"d\",\"E\": {\"E1\": \"e1\",\"E2\": \"e2\",\"E3\": 1}}"
        ret = getJsonFromStr(jsonStr)
        self.assertEqual(ret, (False, "Expecting property name enclosed in double quotes: line 1 column 11 (char 10)"))
        
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

        result = getValueFromConf(confName, "Test3", "test55")
        self.assertEqual(result, (False, "get value from %s error, error is No option 'test55' in section: 'Test3'" % confName, None))
        
        result = getValueFromConf(confName, "Test2", "test6")
        self.assertEqual(result, (False, "get value from %s error, error is No option 'test6' in section: 'Test2'" % confName, None))

        result = getValueFromConf(None, "test", "test")
        self.assertEqual(result, (False, "confFileName is None", None))

        result = getValueFromConf(confName, None, "test")
        self.assertEqual(result, (False, "option is None", None))
        
        result = getValueFromConf(confName, "Test3", None)
        self.assertEqual(result, (False, "key is None", None))
        
        result = getValueFromConf("", "Test3", "test")
        self.assertEqual(result, (False, "confFileName is None", None))

        result = getValueFromConf("/Temp1/Temp2/Temp3", "Test3", "test")
        self.assertEqual(result, (False, "/Temp1/Temp2/Temp3 is not a file", None))
        
        errorConfName = os.path.abspath(os.path.join(etcPath, "ConfParser/error.conf"))
        result = getValueFromConf(errorConfName, "Test2", "test11")
        self.assertEqual(result, (False, "get value from %s error, error is Source contains parsing errors: '%s'\n\t[line 20]: '[Test4\\n'"%(errorConfName, errorConfName), None))

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
        parserResult = ConfParser("/Temp1/Temp2/Temp3")
        self.assertLogs(parserResult, "init ConfParser")
        
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
        
        errorConfPath = os.path.abspath(os.path.join(etcPath, "ConfParser/error.conf"))
        parserResult = ConfParser(errorConfPath)
        self.assertLogs(parserResult, "init ConfParser error, error is Source contains parsing errors: '/Users/wxj/workplace/MyProject/github/PyTestModule/etc/ConfParser/error.conf'\n[line 20]: '[Test4\n'")
        
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

    def test_sendEmail(self):
        attach1 = os.path.abspath(os.path.join(__file__, "../README.md"))
        result = sendEmail('smtp.qq.com', '***@qq.com', '***', ['***@qq.com', '***@qq.com'], '**<***@qq.com>, **<***@qq.com>', "测试邮件", "这是一封测试邮件", {attach1: "log1"})
        #self.assertLogs(result, "email send success.")
        self.assertLogs(result, "email send error:  (535, b'Login Fail. Please enter your authorization code to login. More information in http://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256')")

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(MyUnitTest('test_getJsonFromFile'))
    suite.addTest(MyUnitTest('test_getJsonFromStr'))
    suite.addTest(MyUnitTest('test_valueFromJsonFile'))
    suite.addTest(MyUnitTest('test_valeFromJsonStr'))
    suite.addTest(MyUnitTest('test_saveJsonFile'))

    suite.addTest(MyUnitTest('test_getValueFromConf'))
    suite.addTest(MyUnitTest('test_getValueWithDefault'))
    suite.addTest(MyUnitTest('test_Class_ConfParser_init'))
    suite.addTest(MyUnitTest('test_Class_ConfParser_getValue'))
    suite.addTest(MyUnitTest('test_Class_ConfParser_getValueWithDefault'))
    suite.addTest(MyUnitTest('test_Class_ConfParser_getIntWithDefault'))

    suite.addTest(MyUnitTest('test_sendEmail'))

    runner = unittest.TextTestRunner()
    runner.run(suite)