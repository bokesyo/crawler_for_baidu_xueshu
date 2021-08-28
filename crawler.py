import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)


class GetPaper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://xueshu.baidu.com/")

    def retrieve(self):

        title = '空'
        abstract = '空'
        keyword = '空'

        try:
            # 寻找搜到的标题
            have_title = self.driver.find_element_by_xpath('//*[@id="dtl_l"]/div[1]/h3/a')
            title = have_title.get_attribute('innerText')
            # print('title is', title)
        except:
            pass
            # print('No title')
        try:
            # 寻找摘要
            have_abs = self.driver.find_element_by_class_name('abstract')
            abstract = have_abs.get_attribute('innerHTML')
            # print('abstract is: ', abstract)
        except:
            # 没有摘要
            # print('No abstract.')
            pass

        try:
            # 寻找关键词
            a = self.driver.find_elements_by_class_name('kw_main')
            keyword = a[0].get_attribute('innerText')
            # print('keyword is: ', keyword)
        except:
            # 没有关键词
            # print('No keyword.')
            pass

        return [title, keyword, abstract]

    def controller(self, target):


        target.replace(' ', '')  # 去掉空格
        self.driver.find_element_by_id('kw').send_keys(target + Keys.RETURN)

        # 开始正常爬取
        try:
            self.driver.find_element_by_class_name('main-info')
            return self.retrieve()
        except:
            try:
                # 返回搜索列表
                a = self.driver.find_elements_by_class_name('t')
                b = a[0].get_attribute('innerHTML')
                c = b.split('"')
                paper_link = ''
                for i in c:
                    # 找到论文链接
                    if "https://xueshu.baidu.com/usercenter/paper/show?paperid" in i:
                        paper_link = i
                        break
                if paper_link == '':
                    print('ERROR, no paper link found.')
                    return ['错误', '错误', '错误']
                    # 完成
                else:
                    self.driver.get(paper_link)
                    return self.retrieve()
                    # 完成
            except:
                print('找不到这个论文的信息！')
                self.driver.get("https://xueshu.baidu.com/")
                return ['找不到该论文', '找不到该论文', '找不到该论文']
                pass

    def multiple_paper(self, target_list):
        total = len(target_list)
        count = 0
        result_list = []
        for i in target_list:

            # sleep_time = random.randint(5, 10)
            # time.sleep(sleep_time)

            fin = False
            while not fin:

                try:
                    begin = time.time()
                    result = [i] + self.controller(i)
                    print('result is:', result)
                    result_list.append(result)  # 加入结果
                    count += 1
                    print('%d / %d finished' % (count, total))
                    end = time.time()
                    time_delta = end - begin
                    print("time duration %d second" % time_delta)

                    fin = True

                except:

                    input('遇到反爬虫，人工验证后任意键继续，数据不会丢失。')

        return result_list

    def close(self):
        self.driver.close()


if __name__ == "__main__":
    # 创建爬虫类
    t = GetPaper()

    # 查询论文/专利名
    query = [
        "dc85be32318aad8960228af293a215c9ab5023396b3df8fc45b4ce0a221ecc50d881479053f74f37c97b3392f325d2fb",
        "基于数据挖掘的船舶航迹点生成算法",
        "TRUST和TPPA联合检测梅毒的临床应用价值",
        "结核分枝杆菌耐药表型与耐药基因型相关性研究进展",
        "A Virtual Reality Based Simulator for Training Surgical Skills in Procedure of Catheter Ablation",
        "Rational design of a super-contrast NIR-II fluorophore affords high-performance",
        "一种检测治具及检测设备",
        "一种用于绕制线圈的自动绕线机",
        "一种光电晶体管及其制作方法"
    ]

    # 多篇查询
    t.multiple_paper(query)

    # 全部查询好后，关闭爬虫
    t.close()

