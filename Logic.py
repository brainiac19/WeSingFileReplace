import os
import psutil
import xml.dom.minidom
from shutil import copyfile


class SongFileReplace:
    def __init__(self):
        self.xmlFileLocation=self.findXMLFile()
        self.weSingCacheLocations=self.findWeSingCache()
        self.outputFolderPath=self.weSingCacheLocations+r"\WeSingDL\Output"
        hFile=open(self.xmlFileLocation,encoding="utf-8")
        self.doc = xml.dom.minidom.parse(hFile)
        hFile.close()
        self.outputList = self.doc.getElementsByTagName('Outputs')

    def copyFileandChangeName(self,source,target):
        os.remove(target)
        self.copyFile(source,target)

    def changeName(self,srcFile,dstFile):
        try:
            os.rename(srcFile, dstFile)
        except Exception as e:
            print(e)
            print('rename file fail\r\n')
        else:
            print('rename file success\r\n')


    def finalPhase(self):
        self.copyFileandChangeName(self.sourceSongFilePath,
                                   self.outputFolderPath + "\\" + self.targetxmlNode.attributes[
                                       "OutputName"].value + ".m4a")

    def modDesiredScore(self,score):
        self.modifyScoreString(self.targetxmlNode,score)

    def modDesiredRank(self,rank):
        self.modifyScoreRank(self.targetxmlNode, rank)

    def setTargetxmlNode(self,index):
        self.targetxmlNode = self.outputList[index]

    def setSourceFilePath(self,pathString):
        if os.path.exists(pathString):
            self.sourceSongFilePath = pathString
        else:
            raise Exception("Invalid path")


    def copyFile(self,source,target):
        try:
            copyfile(source, target)
        except IOError as e:
            print("Unable to copy file. %s" % e)
        except:
            print("Unexpected error")

    def getFileSize(self,filePath):
        try:
            size = os.path.getsize(filePath)
            return size
        except Exception as err:
            print(err)

    def modifyFileSize(self,xmlNode):
        xmlNode.attributes["FileSize"].value = str(self.getFileSize(self.sourceSongFilePath))
        hFile = open(self.xmlFileLocation, "w", encoding="utf-8")
        self.doc.writexml(hFile, encoding='UTF-8')
        hFile.close()
        self.modifyFileHeader()

    def modifyFileHeader(self):
        hFile = open(self.xmlFileLocation, "r", encoding="utf-8")
        wholeFile = hFile.readlines()
        wholeFile[0] = "<UserInfo>\n"
        hFile.close()
        hFile = open(self.xmlFileLocation, "w", encoding="utf-8")
        hFile.writelines(wholeFile)
        hFile.close()

    def modifyScoreString(self,xmlNode,desiredScore):
        xmlNode.attributes["AllScores"].value = self.scoreStringGenerator(self.getMaxScore(xmlNode),desiredScore)
        xmlNode.attributes["Score"].value =str(desiredScore)
        hFile = open(self.xmlFileLocation, "w", encoding="utf-8")
        self.doc.writexml(hFile, encoding='UTF-8')
        hFile.close()
        self.modifyFileHeader()

    def modifyScoreRank(self,xmlNode,desiredRank):
        desiredRank=int(desiredRank)
        if desiredRank>6 or desiredRank<1:
            raise Exception("Rank input error, it should be between 1 to 6")
        desiredRank = str(desiredRank)
        xmlNode.attributes["ScoreRank"].value = desiredRank
        hFile = open(self.xmlFileLocation, "w", encoding="utf-8")
        self.doc.writexml(hFile, encoding='UTF-8')
        hFile.close()
        self.modifyFileHeader()

    def scoreStringGenerator(self,totalScore,desiredScore):
        desiredScore=int(desiredScore)
        if desiredScore>totalScore:
            raise Exception("Desired score shouldn't be bigger than max score")
        scoreString=""
        sub=totalScore-desiredScore
        zeroedCount=int(sub/100)
        res=sub%100
        hundredCount=totalScore/100-zeroedCount
        if res==0:
            scoreString="100,"*int(hundredCount)+"0,"*int(zeroedCount)
        else:
            singleScore=100-res
            scoreString = "100," * int(hundredCount-1) + str(singleScore)+","+"0," * int(zeroedCount)

        return scoreString

    def getMaxScore(self,xmlNode):
        scoreString=xmlNode.getAttribute("AllScores")
        commaCount=scoreString.count(",")
        maxScore=100*commaCount
        return maxScore


    def getOutputs(self):
        i=0
        li=[]
        for outputItem in self.outputList:
            i+=1
            li.append("NO."+str(i)+" "+outputItem.getAttribute("OutputName"))
        return li

    def outOfDepth(self,string):
        depth=string.count("\\")
        if depth>1:
            return True
        else:
            return False

    def findXMLFile(self):
        currentUser=os.getlogin()
        path=r"C:\Users\%s\AppData\Roaming\Tencent\WeSing\User Data\KSongsDataInfo.xml"%(currentUser)
        return path

    def findWeSingCache(self):
        deviceList=[]
        folderDevice=""
        folderPath=""
        for i in psutil.disk_partitions():
            deviceList.append(i.device)
        for d in deviceList:
            for root, dirs, files in os.walk(d,topdown=True):
                if self.outOfDepth(root):
                    break
                else:
                    try:
                        index=dirs.index("WeSingCache")
                        folderDevice=d
                    except:
                        pass

        if not folderDevice=="":
            folderPath=folderDevice+"WeSingCache"
        else:
            raise Exception("Cache folder not found")

        return folderPath
