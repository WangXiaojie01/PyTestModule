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

etcPath = os.path.join(os.path.join(__file__, "../etc"))

class MyUnitTest(unittest.TestCase):
    def setUp(self):
        #初始化测试类
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

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(MyUnitTest('test_getJsonFromFile'))
    suite.addTest(MyUnitTest('test_getJsonFromStr'))
    suite.addTest(MyUnitTest('test_valueFromJsonFile'))
    suite.addTest(MyUnitTest('test_valeFromJsonStr'))
    suite.addTest(MyUnitTest('test_saveJsonFile'))

    runner = unittest.TextTestRunner()
    runner.run(suite)