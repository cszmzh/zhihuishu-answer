from urllib import request
import urllib
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


# 本工具仅供交流学习使用，powered by 515code.com

class VALUE:
    # recruitId='25779'
    # studentExamId='5JRGGn34'
    # examId='yLZPY92e'
    # courseId='2072882'

    # 注意uuid一般不用换，Cookie若过期了在游览器F12中network随便找个请求，复制Header携带的Cookie信息替换掉下面的Cookie即可
    uuid = 'JvdlOOEx'
    Cookie = 'acw_tc=707c9f9815893551054928911e5072a620a170d347805793933701dd147fac; Hm_lvt_0a1b7151d8c580761c3aef32a3d501c6=1589530925,1589559228,1589597970,1589597982; showDescription=success; c_session_id=FD9D6E1E7FECE1ECD3ADDAD906C3C14D; isLogin=myschool; o_session_id=85FD917CCFF17E60E78D3770C68707CE; privateCloudSchoolInfo_45=",1,,https://image.zhihuishu.com/testzhs/ablecommons/demo/201605/98d2d89f44d3411db7490f359090314f.jpg,,4043,//school.zhihuishu.com/tgcep,"; Z_LOCALE=1; osm_session_id=5E827AEB03DD449FFB4EEBC8390EB29C; ZHSID=0B6E8C30CC66C5A8B596948DC8C94A42; exitRecod_XezvLNk2=2; exitRecod_JvdlOOEx=1; CASTGC=TGT-17478666-DzcpWSy2r902r2F3Z4gLhE29zyNdBLQnaggEvi5xc3lIIomelH-passport.zhihuishu.com; CASLOGC=%7B%22myuniRole%22%3A0%2C%22username%22%3A%22superadmin%22%2C%22mycuRole%22%3A0%2C%22userId%22%3A45%2C%22myinstRole%22%3A0%2C%22realName%22%3A%22%E8%B6%85%E7%BA%A7%E7%AE%A1%E7%90%86%E5%91%98%22%2C%22uuid%22%3A%22JvdlOOEx%22%2C%22headPic%22%3A%22https%3A%2F%2Fimage.zhihuishu.com%2Fuser%2Ffile%2F45%2F05e4728fa02c4f1eae55ce645e3dd9f6_s3.jpg%22%7D; SESSION=Y2NkODE1MjktNTIyMi00ZDFhLThjNDYtZGMzMTdkYWFiZGFm; Hm_lpvt_0a1b7151d8c580761c3aef32a3d501c6=1589624521; SERVERID=b1981271024e2ffaaf63c337b5db4f00|1589624521|1589621325'

    # 在这里输入你要查找的题号、选项ID，在游览器F12的network中找到doHomeWork这个请求，在里面获取即可
    # 注意！返回的答案代表的是你填入答案ID的位置，例如返回答案是BE，则正确答案ID为下列21342047和21342047，多选题的答案ID一定要写全
    questionId = '6497041'
    answerId = ['31342045', '21342047', '21342046', '21342046', '21342047']


class optionInfo:
    optionsIdStr = ""
    questionId = ""

    def obj2dict(obj):
        d = {}
        d.update(obj.__dict__)
        return d


class Spider:
    # url_getExam = "https://studentexam.zhihuishu.com/studentExam/student/doHomework?recruitId=25779&courseId
    # =2072882&examId=yLZPY92e&uuid=XezvLNk2&studentExamId=5JRGGn34"

    url_getAnswer = "https://studentexam.zhihuishu.com/studentExam/answer/getAnswerImgInfo"

    header = {
        'Cookie': VALUE.Cookie
    }

    exam_list_id = []

    answer_list = []

    def __fetch_content(self):
        # rq = request.Request(Spider.url_getExam,headers=Spider.header)
        # res=request.urlopen(rq)
        # result = res.read().decode("utf-8")
        # return result
        pass

    def go(self):
        self.__analysis(self.__fetch_content())
        self.__print_answer()

    # 数据处理
    def __analysis(self, anchors):
        # json_data = json.loads(anchors)

        # 打印当前试题信息
        # num = json_data['rt']['examBase']['workExamParts'][0]['questionCount'];
        # print('【试题】',json_data['rt']['examBase']['courseName'],json_data['rt']['examBase']['name'],'\n共',num,'道题')

        optionSortInfo = []

        # 获取试题ID与答案ID，封装optionSortInfo列表

        # 手动加入参数

        option = optionInfo()

        option.questionId = VALUE.questionId

        for i in range(0, VALUE.answerId.__len__()):
            option.optionsIdStr = VALUE.answerId[i]

            optionSortInfo.append(option)

            self.__fetch_content_getAnswer(optionSortInfo, i + 1)

    def __fetch_content_getAnswer(self, optionSortInfo, time):

        param = {
            'optionSortInfo': json.dumps(optionSortInfo, default=optionInfo.obj2dict),  # 序列化操作
            'uuid': VALUE.uuid
        }

        rq = request.Request(Spider.url_getAnswer, headers=Spider.header,
                             data=urllib.parse.urlencode(param).encode(encoding='UTF8'))
        res = request.urlopen(rq)
        result = res.read().decode("utf-8")
        self.__analysis_second(result, time);
        return result;

    # 取回答案后进行数据处理
    def __analysis_second(self, anchors, time):
        json_data = json.loads(anchors)

        for key in json_data['rt']:
            print('[题号]', key, '查到答案ID:', VALUE.answerId[time - 1])
            Spider.answer_list.append(chr(64 + time))

    def __print_answer(self):

        print('感谢使用515code查题助手，综上所述答案为:')

        for i in range(0, Spider.answer_list.__len__()):
            print(Spider.answer_list[i])

        print('本工具仅限交流学习使用，谢谢！')

spider = Spider()
spider.go()
